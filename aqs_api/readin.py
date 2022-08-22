__all__ = ['get_login','get_aqs_lists','get_url','aqs_df_out','get_pc_params','check_input','valid_params','find_code']

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import datetime as dt
import re

from .aqs_login import account_setup
from .utils import dates_to_1year, check_services, check_filters, check_params
from .utils import valid_code, valid_aqsdate,drop_unused_params
from .user_info import info

def get_login():
    """
    Description: grabs login information for aqs api: Should be updated by user.
    If no email login is defined, will prompt to enter login or account signup via account_setup function 
    To get ekey for an email, follow this link:
    https://aqs.epa.gov/data/api/signup?email=myemail@example.com
    
    Functions used
    ----------
    account_setup() 
    
    Parameters
    ----------
    (None)
    
    Returns
    ----------
    email, key for aqs login 
    """   
    
    email = info['email']
    key = info['key']
    try: email
    except:
        email, ekey = account_setup()
        if email == None: return False
    return email, key

def get_aqs_lists(filterservice, **kwargs):
    """
    Description: grabs lists of valid parameters from the AQS API 
    
    Libraries used
    ----------
    requests
    pandas (as pd)
    
    Functions used
    ----------
    get_login()    
    
    Parameters
    ----------
    filterservice: str, the name of the filterservice to get a list of
    **kwargs: dict, necessary parameters for filterservices with required parameters for list
    
    Returns
    ----------
    df: a dataframe of possible codes/names
    """
    HOST = "https://aqs.epa.gov/data/api"
    service = 'list'
    base_url = "/".join([HOST, service, filterservice])
    if ('email' not in list(kwargs.keys())) or ('key' not in list(kwargs.keys())):
        email, key = get_login()
    predicates = {"email":email, "key": key}
    for key, value in kwargs.items():
        predicates[key] = value
    r = requests.get(base_url, params=predicates)
    df = pd.read_json(r.url,typ='series')
    data = pd.DataFrame(df['Data'])
    return data

def get_url(service, filterservice, **kwargs):
    """
    Description: gets data from API website based on user-defined services/parameters 
    
    Libraries used
    ----------
    requests
    pandas (as pd)
    
    Functions used
    ----------
    get_login()    
    aqs_df_out()
    check_input()
    drop_unused_params()
    
    Parameters
    ----------
    service: str, the name of the service of the type of data to retrieve
    filterservice: str, the name of the filterservice to get a list of
    **kwargs: dict, necessary parameters for filterservices with required parameters for list
    
    Returns
    ----------
    df: a dataframe of possible codes/names
    """
    if 'count' in kwargs.keys():
        count = kwargs.pop('count')
        
    HOST = "https://aqs.epa.gov/data/api"
    base_url = "/".join([HOST, service, filterservice])
    if ('email' not in list(kwargs.keys())) or ('key' not in list(kwargs.keys())):
        email, key = get_login()
    predicates = {"email":email, "key": key}
    if service != 'list' and count == 0:
        if check_input(service, filterservice, **kwargs) == 0:
            return print(':( '*10,'Failed: check input',':( '*10)
        kwargs = drop_unused_params(service, filterservice, **kwargs)
    for key, value in kwargs.items():
        predicates[key] = value
    r = requests.get(base_url, params=predicates)
    print('*'*20,'Success!','*'*20)
    df = pd.read_json(r.url,typ='series')
    data=pd.DataFrame(df['Data'])
    print('Link to site with json for final file is:\n {0}'.format(r.url))
    # data = aqs_df_out(pd.DataFrame(df['Data']))
    return data, kwargs

def aqs_df_out(df):
    """
    Description: Filters obtained AQS data for missing/bad data
    Keeps relevant columns for sample measurement
    Converts date/time columns to single datetime type column
    Converts site code info to a single code
    
    Libraries used
    ----------
    pandas (as pd)
    
    
    Parameters
    ----------
    df: dataframe- complete dataframe of data pulled from AQS API
    
    Returns
    ----------
    df: a simplified/filtered datafram with AQS info
    """
    cols_out = ['dtvar','siteid','parameter_code','sample_measurement',
                # 'units_of_measure_code',
                'method_code','sample_duration_code']
    df[['date_local','time_local']].apply(lambda s: ' '.join(s.values.astype(str)), axis="columns")
    df['dtvar'] = pd.to_datetime(df[['date_local','time_local']]
                                  .apply(lambda s: ' '.join(s.values.astype(str))
                                         , axis="columns"), format='%Y-%m-%d %H:%S')
    # df['siteid'] = (df[['state_code','county_code','site_number','poc']]
    #                               .apply(lambda s: ''.join(s.values.astype(str))
    #                                      , axis="columns")) 
    df['siteid'] = (df[['state_code','county_code','site_number','poc']]
                                  .apply(lambda s: '{0:02d}{1:03d}{2:04d}'.format(
                                      s['state_code'],s['county_code'],s['site_number'])
                                         , axis="columns")) 
    ppm2ppb = (df.loc[(df.units_of_measure_code == '007')|(df.units_of_measure_code == 7)].index)
    df.loc[ppm2ppb,'sample_measurement'] = df.loc[ppm2ppb,'sample_measurement']*1000 
    val_filter = ((df.qualifier[0]=='V')|(df.qualifier.isna()))
    meas_filter = (df.sample_measurement.notna())
    df_out = df.loc[meas_filter&val_filter][cols_out]
    df_out = df_out.sort_values(by='dtvar',ignore_index=True)
    return df_out


def get_aqs_data(service, filterservice, **kwargs):
    """
    Description: takes in user-defined parameters to retrieve AQS data
    Allows for AQS class to retrieve all parameters in pc
    Allows for multiple years of data- API limits to single calendar year
    
    Libraries used
    ----------
    pandas (as pd)
    
    Functions used
    ----------
    get_pc_params()    
    dates_to_1year()
    get_url()
    
    Parameters
    ----------
    service: str, the name of the service of the type of data to retrieve
    filterservice: str, the name of the filterservice to get a list of
    **kwargs: dict, necessary parameters for filterservices with required parameters for list
    
    Returns
    ----------
    df: a dataframe with all defined years/parameters
    """
    from aqs_api.user_info import info
    directory = info['directory']
    from aqs_api.aqs_codes import param, state
    paramin = param
    file_names = {'param':paramin,
                 'state':state}

    param = file_names.get('param', {}).get(kwargs['param'])
    state = file_names.get('state', {}).get(kwargs['state'])
    if ('pc' in kwargs.keys()):
        params = get_pc_params(kwargs['pc'])
        kwargs['param'] = params[0]
    bdates, edates = dates_to_1year(kwargs['bdate'],kwargs['edate'])
    count = 0
    for start, end in zip(list(bdates), list(edates)):
        #print(start, end)
        kwargs['bdate'],kwargs['edate'] = start, end
        df_temp, kwargs = get_url(service, filterservice, count=count, **kwargs)
        file_out = '{0}{1}_{2}_{3}.csv'.format(directory,start[:4],param,state)
        df_temp.to_csv(file_out,
                sep = ',', doublequote = False, index=False,
                  )

        count += 1

def get_pc_params(pc):
    """
    Description: gets parameters from API website based on user-defined parameter class (pc)
    
    Libraries used
    ----------
    requests
    pandas (as pd)
    
    Functions used
    ----------
    get_aqs_lists()
    
    Parameters
    ----------
    pc: str parameter class
    
    Returns
    ----------
    df: a dataframe of possible codes/names
    """
    pc_list = list(get_aqs_lists('classes')['code'])
    if pc not in pc_list:
        print(':( '*10,'Failed: check parameter class input',':( '*10)
        return print(pc_list)
    return list(get_aqs_lists('parametersByClass',pc =kwargs['pc'])['code'])
        
    
def check_input(service, filterservice, **kwargs):
    """
    Description: checks to see if aqs input names are valid
     
    Functions used
    ----------
    check_services()    
    check_filters()
    check_params()
    valid_params()
    
    Parameters
    ----------
    service: str, the name of the service of the type of data to retrieve
    filterservice: str, the name of the filterservice to get a list of
    **kwargs: dict, necessary parameters for filterservices with required parameters for list
    
    Returns
    ----------
    Boolean: if input is valid (True) or incorrect (False)
    """
    a = check_services(service)
    b = check_filters(service, filterservice)
    c = check_params(service, filterservice, **kwargs)
    d = 1#valid_params(**kwargs)
    if (a+b+c+d) < 4:
        print('Input check failed')
        return False
    else: return True    
    
def valid_params(**kwargs):
    
    """
    Description: checks if parameters are valid input
    
    Functions used
    ----------
    valid_code()
    valid_aqsdate()
    
    Parameters
    ----------
    kwargs: dict, parameters for data retrieval
    
    Returns
    ----------
    Boolean: True (valid) or False (not valid)
    Prints list of required input for parameters if False
    """
    
    bad_params = {}
    good_params = {}
    coded_params = ['param','state','county','site','cbsa','pqao','ma','class']
    date_params = ['bdate','edate','cbdate','cedate']
    geo_params = ['minlat', 'maxlat', 'minlon', 'maxlon']
    check_geo = geo_params
    for key, value in kwargs.items():
        code = None
        if key in coded_params:
            if key == 'county':
                code = valid_code(key, value, state = kwargs['state'])
            elif key == 'site':
                code = valid_code(key, value, state = kwargs['state'], county = kwargs['county'])
            else:
                code = valid_code(key, value)
            if code == None:
                bad_params[key] = value
        if key in date_params:
            if len(value) !=8:
                bad_params[key] = value
            else:
                code = valid_aqsdate(value)
        if key in geo_params:
            #Pull for lat or lon for checking box boundaries
            if key[-3:]=='lat': maxv = 90
            elif key[-3:]=='lon': maxv = 180
            if (float(value) > maxv) and (float(value) <= maxv*2):
                print('Input value: {1} for {0} is out of bounds (-180-180)'.format(key,value))
                code = None
            elif (((key == 'minlat') and (float(value) < 20)) or ((key == 'maxlat') and (float(value) > 75)) or
                ((key == 'maxlon') and (float(value) < -60))):
                print('Warning: value {0} for {1} is outside of North America bounding box (lat: (20:75), lon: (-180:-60))'.format(key,value))
                code = value
                check_geo.remove(key)
            else:
                code = value
                check_geo.remove(key)
        if code == None:
            bad_params[key]=value
        else:
            good_params[key]=value
    if len(bad_params) > 0:
        print('The following parameters do not fit required values:')
        print(bad_params)
        return False
    return True

def find_code(key_in,*arg, **kwargs):
    """
    Description: retrieves codes from AQS API list for given parameter
    
    Functions used
    ----------
    get_aqs_lists()    
    
    Parameters
    ----------
    key_in: str, parameter key
    arg: str, not used, just a backup
    kwargs: dict, parameters needed for data retrieval
    
    Returns
    ----------
    list: list of valid AQS code for given parameter
    """
    dict_check = {}
    if key_in == 'param':
        listfilter = 'parametersByClass'
        dict_check['pc'] = 'ALL'
    elif key_in == 'state':
        listfilter = 'states'
    elif key_in == 'county':
        listfilter = 'countiesByState'
        dict_check['state'] = kwargs['state']
#         vals = get_aqs_lists('list',listfilter,state=kwargs['state'])
    elif key_in == 'site':
        listfilter = 'sitesByCounty'
        dict_check['state'] = kwargs['state']
        dict_check['county'] = kwargs['county']
    elif key_in == 'cbsa':
        listfilter= 'cbsas'
    elif key_in == 'pqao':
        listfilter = 'pqaos'
    elif key_in == 'ma':
        listfilter = 'mas'
    elif key_in == 'class':
        listfilter = 'classes'
    else:
        return print(key_in,' has no predefined code to check')
    
    vals = get_aqs_lists(listfilter,**dict_check)
    return vals
