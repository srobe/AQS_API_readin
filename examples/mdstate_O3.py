## Uncomment lines below if you've updated the aqs_api modules
#import sys
#for k in list(sys.modules):
#    if k.startswith('aqs_api'):
#        del sys.modules[k]

import aqs_api
from aqs_api import *
from aqs_api.readin import get_aqs_data


args_in = { 
    'param':'44201', # Ozone
    'bdate':'20100101', #Start Date
    'edate':'20121231', #End Date
    'state':'24', # Maryland
  }

file_out = get_aqs_data('sampleData','byState',**args_in)


