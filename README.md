# AQS_API_readin
Python code to read in AQS data from the EPA API (https://aqs.epa.gov/aqsweb/documents/data_api.html#cbdate)

**Before Using you need a login and key**
## Getting Started: 
**1.** Get a login and key <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; https\://aqs\.epa\.gov/data/api/signup?email=myemail@example&#46;com  <br/>
&nbsp;&nbsp;&nbsp;&nbsp;a.) Update myemail@example.com to your email  <br/>
&nbsp;&nbsp;&nbsp;&nbsp;b.) Past updated link in address bar of your browser <br/>

**2.** Update **user_info.py** with: 
 - login
 - key
 - preferred directory to save files
 <br/>
 <a/>
 
**3.** Make a **input.py** file (or update an example file) for the data you would like to retrieve <br /> 
&nbsp;&nbsp;&nbsp;&nbsp; Info needed:
 - param
 - bdate (starting date in YYYYMMDD)
 - edate (ending date in YYYYMMDD)
 - state code or abbreviation
 <br/>
 <a/>
 
**4.** Run input.py <br/>
