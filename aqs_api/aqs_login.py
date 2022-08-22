_all__ = ['account_setup','check_response']


def account_setup():
    """
    Description: 
    Prompts to enter login or account signup via account_setup function 
    To get key for an email, follow this link:
    https://aqs.epa.gov/data/api/signup?email=myemail@example.com
    
    Functions used
    ----------
    check_response() 
    
    Parameters
    ----------
    (None)
    
    Returns
    ----------
    email, key for aqs login
    or None, None if no login acquired
    """
    question = 'No email defined, do you have an email and key to access the AQS API? (Y or N):'
    affirmative = ['yes','y']
    negative = ['no','n']
    response = check_response(question, affirmative, negative)
    if response != None:
        if response.lower() in affirmative:
            global email
            global key
            email = input('Enter email for AQS API account:')
            key = input('Enter key for AQS API account with email {0}:'.format(email))
            print('For future use, you can update get_login() function with email and key.')
            return email, key
        else:
            question = 'Would you like to set up an AQS API account or update the key to your account? (Y or N):' 
            response = check_response(question, affirmative, negative)
            if response != None:
                if response.lower() in affirmative:
                    email = input('Enter email you would like to use for AQS API account:')
                    r = requests.get('https://aqs.epa.gov/data/api/signup', params={'email':email})
                    print('Follow this link {0} to activate your account for email: {1}'.format(r.url,email))
                    print('After clicking on the above link, a verification email will be sent to {0}.'.format(email))
                    return None, None 
    print('An email and key are needed to access data. More info here: https://aqs.epa.gov/aqsweb/documents/data_api.html#signup')
    return None, None 

                

def check_response(question, ans = ['yes','y','no','n'], *args):
    """
    Description: Checks input from question prompt. Gives 3 tries to enter an interpretable answer. 
    
    
    Parameters
    ----------
    Question: String of question to ask user
    ans: (list of strings, optional)- Default is a yes/no answer. 
    *args: any extra lists of possible answers
    
    Returns
    ----------
    str: response to the questions
    (None if uninterpretable)
    """
    for arg in args:
        ans = ans + arg
    answer = 0
    tryanswer = 0
    while answer == 0:
        response = input(question)
        if response.lower() in ans:
            answer = 1
        else: 
            if tryanswer >= 3:
                print('Response not recognized, we give up.')
                return None
            else:
                tryanswer += 1
                print('Attempt {0}/3: Response not recogized, try again'.format(tryanswer))
    return response
