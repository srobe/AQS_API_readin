__all__ = ['dates_to1year','check_services','check_filters','check_params','drop_unused_params','get_api_service_info','is_lpyr','last_day_in_month','valid_day','valid_aqsdate','valid_code']

import datetime as dt
import requests
import pandas as pd


def dates_to_1year(bdate,edate):
    """
    Description: takes in date range and makes lists of dates corresponding to a single calendar year
    
    Functions used:
    ----------
    datetime (as dt)
    
    Parameters
    ----------
    bdate: str, first date to retrieve data for
    edate: str, final date to retrieve data for
    
    Returns
    ----------
    bdates: list, first date of each calendar year in date range
    edates: list, final data of each calendar year in date range
    """
    start = dt.datetime.strptime(bdate, '%Y%m%d')
    end = dt.datetime.strptime(edate, '%Y%m%d')
    print('AQS only allows input with bdate and edate of the same year')
    print('Looping through years {0} - {1}'.format(start.year,end.year))
    bdates, edates = [], []
    year = start.year
    while year <= end.year:
        bdates.append('{0}0101'.format(year))
        edates.append('{0}1231'.format(year))
        year += 1
    bdates[0] = bdate
    edates[-1] = edate
    return bdates, edates    
    
    
# 
    
def check_services(service):
    """
    Description: checks input service if valid
    
    Functions used
    ----------
    get_api_service_info()    
    
    Parameters
    ----------
    service: str, the name of the service of the type of data to retrieve
    
    Returns
    ----------
    Boolean: True (valid) or False (not valid)
    Prints list of valid services if False 
    """
    service_list = get_api_service_info()
    if service in service_list:
        return True
    else:
        print(service_list)
        return False
    
def check_filters(service,filterservice):
    """
    Description: checks input filterservice if valid
    
    Functions used
    ----------
    get_api_service_info()    
    
    Parameters
    ----------
    service: str, the name of the service of the type of data to retrieve
    filterservice: str, the name of the filterservice of data to retrieve
    
    Returns
    ----------
    Boolean: True (valid) or False (not valid)
    Prints list of valid filterservices if False 
    """
    filter_list = get_api_service_info(service)
    if filterservice in filter_list:
        return True
    else:
        print(filter_list)
        return False
    
def check_params(service,filterservice,**kwargs):
    """
    Description: checks if all required input parameters are defined
    
    Functions used
    ----------
    get_api_service_info()    
    
    Parameters
    ----------
    service: str, the name of the service of the type of data to retrieve
    filterservice: str, the name of the filterservice of data to retrieve
    kwargs: dict, parameters for data retrieval
    
    Returns
    ----------
    Boolean: True (valid) or False (not valid)
    Prints list of required input for filterservice if False
    """
    filter_list = get_api_service_info(service)
    if filterservice in filter_list:
        return True
    else:
        print(filter_list)
        return False
    param_list = get_api_service_info(service, filterservice)
    required_list = param_list['required']
    bad_params = {}
    for required in required_list:
        if required not in kwargs.keys():
            print('Warning: required input missing: {0}'.format(required))
            bad_params[required] = 'Missing'
    if len(bad_params) > 0:
        return False
    else:
        return True
    
def drop_unused_params(service,filterservice,**kwargs):
    """
    Description: checks if all input parameters can be used with filterservice, drops unused parameters
    
    Functions used
    ----------
    get_api_service_info()    
    
    Parameters
    ----------
    service: str, the name of the service of the type of data to retrieve
    filterservice: str, the name of the filterservice of data to retrieve
    kwargs: dict, parameters for data retrieval
    
    Returns
    ----------
    Dict: parameters that can be used for input
    """
    param_list = get_api_service_info(service, filterservice)
    required_list, optional_list = param_list['required'], param_list['optional']
    good_params = kwargs
    if check_params(service,filterservice,**kwargs)==False:
        return None
    keys_in = list(kwargs.keys())
    for key in keys_in:
        if (key not in required_list) and (key not in optional_list):
            print('Warning: {0} initialized, but is unused'.format(key))
            del good_params[key]
    return good_params
    
    
def get_api_service_info(service = None, filterservice = None):
    """
    Description: Basically a library of input information for AQS API website
    gives valid input for API inquiries
    
    Functions used
    ----------
    get_api_service_info()    
    
    Parameters
    ----------
    service: str, the name of the service of the type of data to retrieve
    filterservice: str, the name of the filterservice of data to retrieve
    
    Returns
    ----------
    list: 
    No input: service list
    service input: filterservice list for service
    service and filterservice input: parameter list for filterservice
    """
    
    meta_filter = ['isAvailable', 'revisionHistory', 'fieldsByService', 'issues']
    list_filter = ['states', 'countiesByState', 'sitesByCounty', 'cbsas', 'classes', 'parametersByClass', 'pqaos', 'mas']
    data_filter = ['bySite', 'byCounty', 'byState', 'byBox', 'byCBSA']
    qa_filter = ['bySite', 'byCounty', 'byState', 'byMA', 'byPQAO']
    services = {'metaData':{'filters': meta_filter, 'optional':[]},
                'list':{'filters': list_filter, 'optional':[]},
                'monitors':{'filters': data_filter, 'optional':[]},
                'sampleData':{'filters': data_filter, 'optional':['duration','cbdate','cedate']},
                'dailyData':{'filters': data_filter, 'optional':['cbdate','cedate']},
                'quarterlyData':{'filters': data_filter, 'optional':['cbdate','cedate']},
                'annualData':{'filters': data_filter, 'optional':['cbdate','cedate']},
                'qaAnnualPerformanceEvaluations':{'filters': qa_filter, 'optional':[]},
                'qaBlanks':{'filters': qa_filter, 'optional':[]},
                'qaCollocatedAssessments':{'filters': qa_filter, 'optional':[]},
                'qaFlowRateVerifications':{'filters': qa_filter, 'optional':[]},
                'qaFlowRateAudits':{'filters': qa_filter, 'optional':[]},
                'qaOnePointQcRawData':{'filters': qa_filter, 'optional':[]},
                'qaPepAudits':{'filters': qa_filter, 'optional':[]},
                'transactionsSample':{'filters': qa_filter[:-1], 'optional':['cbdate','cedate']},
                'transactionsQaAnnualPerformanceEvaluations':{'filters': qa_filter, 'optional':[]},
               }
    
    filters =  {'fieldsByService':['service'],
                'countiesByState':['state'],
                'sitesByCounty':['state','county'],
                'parametersByClass':['pc'],
                'bySite':['state','county','site','param','bdate','edate'],
                'byCounty':['state','county','param','bdate','edate'],
                'byState':['state','param','bdate','edate','param','bdate','edate'],
                'byBox':['minlat', 'maxlat', 'minlon', 'maxlon','param','bdate','edate'],
                'byCBSA':['cbsa','param','bdate','edate'],
                'byPQAO':['pqao','param','bdate','edate'],
                'byMA':['ma','param','bdate','edate'],
                'isAvailable': [],
                'revisionHistory': [],
                'issues': [],
                'states': [],
                'cbsas': [],
                'classes': [],
                'pqaos': [],
                'mas': [],
                }
    if (service not in list(services.keys())) and (service != None):
        print('Error: {0} not in available services'.format(service))
        return_var = list(services.keys())
    elif (filterservice not in list(filters.keys())) and (filterservice != None):
        print('Error: {0} is not an available servicefilter for {1}'.format(filterservice, service))
        return_var = list(services[service]['filters'])
    elif filterservice !=None:
        return_var = {'required': filters[filterservice],
                      'optional': services[service]['optional']}   
    elif service != None:
        return_var = list(services[service]['filters'])
    else:
        return_var = list(services.keys())
    return return_var

def is_lpyr(year):
    """
    Description: Checks to see if year is a leap year
    
    Parameters
    ----------
    year: str or int (converts to int just in case)
    
    Returns
    ----------
    boolean: True if leap year, False if not
    """        
    yr = int(year)
    if (yr % 4 == 0) and (((yr % 100)!=0) or ((yr % 400)==0)):
        return True
    else:
        return False
    
def last_day_in_month(year,month,*arg):
    """
    Description: Finds the last valid day for each month
    
    Functions used
    ----------
    is_lpyr()
    
    Parameters
    ----------
    year: str or int (converts to int just in case)
    month: str or int (converts to int just in case)
    *arg: not used, but placed here if I accidentally include another argument (like day)
    
    Returns
    ----------
    int: Last valid day in the given month/year
    """        
    yr, mn  = int(year), int(month)
    long_months = [1, 3, 5, 7, 8, 10, 12]
    if (mn > 12) or (mn < 1):
        print('Invalid Month: {0:02d}'.format(mn))
        return bool(False)
    elif mn==2:
        last_day = 28 + int(is_lpyr(yr))
    elif mn in long_months:
        last_day = 31
    else:
        last_day = 30
    return last_day

def valid_day(year,month,day):
    """
    Description: Finds if the given month or day in month is a valid date 
    
    Functions used
    ----------
    last_day_in_month()
    
    Parameters
    ----------
    year: str or int (converts to int just in case)
    month: str or int (converts to int just in case)
    day: str or int (converts to int just in case)
    
    Returns
    ----------
    Boolean : True if valid, False if not
    """       
    yr, mn, dy = int(year), int(month), int(day)
    long_months = [1, 3, 5, 7, 8, 10, 12]
    last_day = last_day_in_month(yr, mn)
    if (mn > 12) or (mn < 1):
        return bool(False)
    if dy <= last_day:
        return True
    else:
        print('Invalid Day: {0:02d} for given month: {1:02d} and year: {2}'.format(dy,mn,yr))
        return False


def valid_aqsdate(date_val):
    """
    Description: Checks if input date is within the valid time limits for AQS
    Not valid:
    date < 1970, data unlikely available 
    date > today, data isn't not available
    
    Valid but with Warnings:
    1970-1980, data is not recommended (if available)
    within last ~18 months, data may not be available or validated
    
    Valid:
    1980 - (current date - 18 months)
    
    Libraries used
    ----------
    datetime (as dt) 
    
    Functions used
    ----------
    valid_day()
    
    Parameters
    ----------
    date_val: the string of given date 
    
    Returns
    ----------
    Valid date: date_val (value in, used for api code)
    Not valid: None
    """        
    date_in =  dt.datetime.strptime(date_val, '%Y%m%d')
    yr, mn, dy = date_in.year, date_in.month, date_in.day
    current_date = dt.datetime.today()
    current_year = current_date.year
    if valid_day(yr,mn,dy) == 0:
        return None
    if (yr < 1970) or (date_in > (current_date)):
        print('Given year: {0} is not in available dates for data'.format(yr))
        return None
    if ((yr > (current_year-2)) and (mn >= 6)) or ((yr > (current_year-1)) and (mn < 6)):
        print('Warning: Given date {0}{1:02d}{2:02d} is within last 18 months. Data may not be available or validated yet.'.format(yr,mn,dy))
    elif (yr > 1970) & (yr < 1980):
        print('Warning: given year {0} is before 1980, data may not be available'.format(yr))
    return date_val    
    

def valid_code(key_in, value_in,**kwargs):
    """
    Description: checks required input parameters value is defined
    
    Functions used
    ----------
    find_code()    
    
    Parameters
    ----------
    key_in: str, parameter key
    value_in: str, value for inputer parameter key
    kwargs: dict, parameters needed for data retrieval
    
    Returns
    ----------
    str: code for chosen parameter. 
    Prints list of valid input for parameter key if False
    """
    vals = find_code(key_in,**kwargs)
    code_find = vals[(vals['code']==value_in)|(vals['value_represented']==value_in)]
    try:
        print('returning code: {0} for {1} = {2}'.format((code_find.code.values[0]),key_in,(code_find.value_represented.values)))
        return (code_find.code.values[0])
    except:
        print('Incorrect input for: {0} ,available options:'.format(key_in))
        return print(vals.to_dict('split')['data'])            
            
            
