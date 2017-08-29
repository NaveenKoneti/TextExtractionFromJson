import re
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import pandas as pd

companyProject = pd.read_csv("company-project.csv")

def get_mail(text):
    match = re.search(u"([a-z0-9!#$%&'*+\/=?^_`{|.}~-]+@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)", text)
    return match.group(0)

def get_names(text):   
    st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz',
                           'stanford-ner.jar',
                           encoding='utf-8')

    tokenized_text = word_tokenize(text)
    classified_text = st.tag(tokenized_text)
    Names = [tup[0] for tup in classified_text if tup[1] == "PERSON"]
    Names = [str(name) for name in Names]
    return Names
def get_names_from_to(text):
    nameList = text.split()
    return nameList

def GetPhoneNumber(text):
    match = re.search(u'''((?:(?<![\d-])(?:\+?\d{1,3}[-.\s*]?)?(?:\(?\d{3}\)?[-.\s*]?)?\d{3}[-.\s*]?\d{4}(?![\d-]))|(?:(?<![\d-])(?:(?:\(\+?\d{2}\))|(?:\+?\d{2}))\s*\d{2}\s*\d{3}\s*\d{4}(?![\d-])))''', text)
    return match.group(0)

def get_ngrams(text, n ):
    n_grams = ngrams(word_tokenize(text), n)
    return [ ' '.join(grams) for grams in n_grams]

allCompanyGrams = []
for myString in companyProject['COMPANY NAME']:
    myString = myString.lower()
    strlen = len(myString.split())
    grams = []
    n = 1
    while(n<= strlen):
        gram = get_ngrams(myString,n)
        grams = grams+([gram[0]])
        n = n+1
    grams = grams[::-1]
    allCompanyGrams = allCompanyGrams+grams   
    allCompanyGrams = list(set(allCompanyGrams))
    allCompanyGrams.sort(lambda x,y: cmp(len(x), len(y)),reverse=True)


    
allProjectGrams = []
for myString in companyProject['PROJECT NAME']:
    myString = myString.lower()
    strlen = len(myString.split())
    grams = []
    n = 1
    while(n<= strlen):
        gram = get_ngrams(myString,n)
        grams = grams+([gram[0]])
        n = n+1
    grams = grams[::-1]
    allProjectGrams = allProjectGrams+grams    
    allProjectGrams = list(set(allProjectGrams))
    allProjectGrams.sort(lambda x,y: cmp(len(x), len(y)),reverse=True)
#print(allCompanyGrams)

def getResponse(myDict):
    Subresponses = {} 
    response = {"email_tokens":Subresponses}
    
    Subresponses['to'] = []
    if("to" in myDict.keys()):
        to_data = { k:v for k,v in myDict.items() if 'to' in k }
        to_value = to_data.values()[0]
        try:
            if(get_mail(to_value) is not None):
                to_mail = get_mail(to_value)
                start_to_mail = to_value.find(to_mail)
                end_to_value = start_to_mail + len(to_mail)
                to_mail_response = {"Start" : start_to_mail,"End":end_to_value,"Mail":to_mail}
                Subresponses['to'].append(to_mail_response)
        except AttributeError:
            pass
        if(len(get_names_from_to(to_value)) != 0):
            allNames = get_names_from_to(to_value)
            if(len(allNames) > 1):
                FirstName = allNames[0]
                FirstNameStart = to_value.find(FirstName)
                FirstNameEnd = FirstNameStart + len(FirstName)
                LastName = allNames[1]
                LastNameStart = to_value.find(LastName)
                LastNameEnd = LastNameStart+len(LastName)
                FirstNameJson = {"FirstName":FirstName,"Start":FirstNameStart,"End":FirstNameEnd}
                LastNameJson = {"LastName":LastName,"Start":LastNameStart,"End":LastNameEnd}
                Subresponses['to'].append(FirstNameJson)
                Subresponses['to'].append(LastNameJson)


            elif(len(allNames) == 1):
                FirstName = allNames[0]
                FirstNameStart = to_value.find(FirstName)
                FirstNameEnd = FirstNameStart + len(FirstName)
                FirstNameJson = {"FirstName":FirstName,"Start":FirstNameStart,"End":FirstNameEnd}
                Subresponses['to'].append(FirstNameJson)
            
            
        
    Subresponses['from'] = []
    if("from" in myDict.keys()):
        from_data = { k:v for k,v in myDict.items() if 'from' in k }
        from_value = from_data.values()[0]
        try:
            if(get_mail(from_value) is not None):
                from_mail = get_mail(from_value)
                start_from_mail = from_value.find(from_mail)
                end_from_value = start_from_mail + len(from_mail)
                from_mail_response = {"Start" : start_from_mail,"End":end_from_value,"Mail":from_mail}
                Subresponses['from'].append(from_mail_response)
        except AttributeError:
            pass
        if(len(get_names_from_to(from_value)) != 0):
            allNames = get_names_from_to(from_value)
            if(len(allNames) > 1):
                FirstName = allNames[0]
                FirstNameStart = from_value.find(FirstName)
                FirstNameEnd = FirstNameStart + len(FirstName)
                LastName = allNames[1]
                LastNameStart = from_value.find(LastName)
                LastNameEnd = LastNameStart+len(LastName)
                FirstNameJson = {"FirstName":FirstName,"Start":FirstNameStart,"End":FirstNameEnd}
                LastNameJson = {"LastName":LastName,"Start":LastNameStart,"End":LastNameEnd}
                Subresponses['from'].append(FirstNameJson)
                Subresponses['from'].append(LastNameJson)


            elif(len(allNames) == 1):
                FirstName = allNames[0]
                FirstNameStart = from_value.find(FirstName)
                FirstNameEnd = FirstNameStart + len(FirstName)
                FirstNameJson = {"FirstName":FirstName,"Start":FirstNameStart,"End":FirstNameEnd}
                Subresponses['from'].append(FirstNameJson)
                
                
    Subresponses['fetcher_mail_signature'] = []
    if("fetcher_mail_signature" in myDict.keys()):
        fet_mail_sign = { k:v for k,v in myDict.items() if 'fetcher_mail_signature' in k }
        sign_value = fet_mail_sign.values()[0]
        try:
            if(get_mail(sign_value) is not None):
                sign_mail = get_mail(sign_value)
                start_sign_mail = sign_value.find(sign_mail)
                end_sign_value = start_sign_mail + len(sign_mail)
                Sign_mail_response = {"Start" : start_sign_mail,"End":end_sign_value,"Mail":sign_mail}
                Subresponses['fetcher_mail_signature'].append(Sign_mail_response)
        except AttributeError:
            pass
        if(len(get_names(sign_value)) != 0):
            allNames = get_names(sign_value)
            if(len(allNames) > 1):
                FirstName = allNames[0]
                FirstNameStart = sign_value.find(FirstName)
                FirstNameEnd = FirstNameStart + len(FirstName)
                LastName = allNames[1]
                LastNameStart = sign_value.find(LastName)
                LastNameEnd = LastNameStart+len(LastName)
                FirstNameJson = {"FirstName":FirstName,"Start":FirstNameStart,"End":FirstNameEnd}
                LastNameJson = {"LastName":LastName,"Start":LastNameStart,"End":LastNameEnd}
                Subresponses['fetcher_mail_signature'].append(FirstNameJson)
                Subresponses['fetcher_mail_signature'].append(LastNameJson)


            elif(len(allNames) == 1):
                FirstName = allNames[0]
                FirstNameStart = FirstName.find(sign_value)
                FirstNameEnd = FirstNameStart + len(FirstName)
                FirstNameJson = {"FirstName":FirstName,"Start":FirstNameStart,"End":FirstNameEnd}
                Subresponses['fetcher_mail_signature'].append(FirstNameJson)
            #MaxInteger = GetIntegers(sign_value)
            #if (len(str(MaxInteger))>=5):
            try:
                PhoneNumber = GetPhoneNumber(sign_value)
                PhoneNumberStart = sign_value.find(str(PhoneNumber))
                PhoneNumberEnd = PhoneNumberStart +  len(str(PhoneNumber))
                PhoneNumberJson = {"Phone":PhoneNumber,"Start":PhoneNumberStart,"End":PhoneNumberEnd}
                Subresponses['fetcher_mail_signature'].append(PhoneNumberJson)
            except AttributeError:
                pass
            
            
    Subresponses['fetcher_messagebody_text'] = []
    if("fetcher_messagebody_text" in myDict.keys()):
        fetcher_body = { k:v for k,v in myDict.items() if 'fetcher_messagebody_text' in k }
        
        body_value = fetcher_body.values()[0]
        
        #print(body_value)
        try:
            if(get_mail(body_value) is not None):
                body_mail = get_mail(body_value)
                start_body_mail = body_value.find(body_mail)
                end_body_value = start_body_mail + len(body_mail)
                Sign_body_response = {"Start" : start_body_mail,"End":end_body_value,"Mail":body_mail}
                Subresponses['fetcher_messagebody_text'].append(Sign_body_response)
        except AttributeError:
            pass
        if(len(get_names(body_value)) != 0):
            allNames = get_names(body_value)
            if(len(allNames) > 1):
                FirstName = allNames[0]
                FirstNameStart = body_value.find(FirstName)
                FirstNameEnd = FirstNameStart + len(FirstName)
                LastName = allNames[1]
                LastNameStart = body_value.find(LastName)
                LastNameEnd = LastNameStart+len(LastName)
                FirstNameJson = {"FirstName":FirstName,"Start":FirstNameStart,"End":FirstNameEnd}
                LastNameJson = {"LastName":LastName,"Start":LastNameStart,"End":LastNameEnd}
                Subresponses['fetcher_messagebody_text'].append(FirstNameJson)
                Subresponses['fetcher_messagebody_text'].append(LastNameJson)


            elif(len(allNames) == 1):
                FirstName = allNames[0]
                FirstNameStart = body_value.find(FirstName)
                FirstNameEnd = FirstNameStart + len(FirstName)
                FirstNameJson = {"FirstName":FirstName,"Start":FirstNameStart,"End":FirstNameEnd}
                Subresponses['fetcher_messagebody_text'].append(FirstNameJson)
           
        try:
            #print(body_value)
            PhoneNumber = GetPhoneNumber(body_value)

            PhoneNumberStart = body_value.find(str(PhoneNumber))
            PhoneNumberEnd = PhoneNumberStart +  len(str(PhoneNumber))
            PhoneNumberJson = {"Phone":PhoneNumber,"Start":PhoneNumberStart,"End":PhoneNumberEnd}
            Subresponses['fetcher_messagebody_text'].append(PhoneNumberJson)
        except AttributeError:
            pass
            
        body_string = body_value.lower()
        #print(body_string)
        #print('k-org' in body_string)
        
        
        companyMatch = [word for word in allCompanyGrams if word in body_string]
        #print(companyMatch)
        try:
            if(companyMatch != []):
                bestCompanyMatch = companyMatch[0]
                #print(bestCompanyMatch)
                companyStart = body_string.find(bestCompanyMatch)
                
                companyEnd = companyStart+len(bestCompanyMatch)
                companyJson = {'Start': companyStart,'End':companyEnd,'Company':bestCompanyMatch}
                #print(companyJson)
                
                Subresponses['fetcher_messagebody_text'].append(companyJson)
        except:
            pass
        
       
        projectMatch = [word for word in allProjectGrams if word in body_string]
        try:
            if(projectMatch != []):
                bestProjectMatch = projectMatch[0]
                projectStart = body_string.find(bestProjectMatch)
                projectEnd = projectStart+len(bestProjectMatch)
                projectJson = {'Start': projectStart,'End':projectEnd,'Project':bestProjectMatch}
                Subresponses['fetcher_messagebody_text'].append(projectJson)
        except:
            pass
        
                

    
    Subresponses['fetcher_subject'] = []
    if("fetcher_subject" in myDict.keys()):
        fet_mail_sign = { k:v for k,v in myDict.items() if 'fetcher_subject' in k }
        sign_value = fet_mail_sign.values()[0]
        try:
            if(get_mail(sign_value) is not None):
                sign_mail = get_mail(sign_value)
                start_sign_mail = sign_value.find(sign_mail)
                end_sign_value = start_sign_mail + len(sign_mail)
                Sign_mail_response = {"Start" : start_sign_mail,"End":end_sign_value,"Mail":sign_mail}
                Subresponses['fetcher_subject'].append(Sign_mail_response)
        except AttributeError:
            pass
        if(len(get_names(sign_value)) != 0):
            allNames = get_names(sign_value)
            if(len(allNames) > 1):
                FirstName = allNames[0]
                FirstNameStart = sign_value.find(FirstName)
                FirstNameEnd = FirstNameStart + len(FirstName)
                LastName = allNames[1]
                LastNameStart = sign_value.find(LastName)
                LastNameEnd = LastNameStart+len(LastName)
                FirstNameJson = {"FirstName":FirstName,"Start":FirstNameStart,"End":FirstNameEnd}
                LastNameJson = {"LastName":LastName,"Start":LastNameStart,"End":LastNameEnd}
                Subresponses['fetcher_subject'].append(FirstNameJson)
                Subresponses['fetcher_subject'].append(LastNameJson)


            elif(len(allNames) == 1):
                FirstName = allNames[0]
                FirstNameStart = FirstName.find(sign_value)
                FirstNameEnd = FirstNameStart + len(FirstName)
                FirstNameJson = {"FirstName":FirstName,"Start":FirstNameStart,"End":FirstNameEnd}
                Subresponses['fetcher_subject'].append(FirstNameJson)
            #MaxInteger = GetIntegers(sign_value)
            #if (len(str(MaxInteger))>=5):
            try:
                PhoneNumber = GetPhoneNumber(sign_value)
                PhoneNumberStart = sign_value.find(str(PhoneNumber))
                PhoneNumberEnd = PhoneNumberStart +  len(str(PhoneNumber))
                PhoneNumberJson = {"Phone":PhoneNumber,"Start":PhoneNumberStart,"End":PhoneNumberEnd}
                Subresponses['fetcher_subject'].append(PhoneNumberJson)
            except AttributeError:
                pass
    return response
    #print response


MyJsonFile ={ 
              
      "to":"David Letterman <david_letterman@xmail.com>",
    "from":"Mark Spencer <info@dvdsonline.com >",
    "fetcher_messagebody_text":"If you have any question, call us at +2348272850957 or email me personally at mark_spencer@xmail.com.",
    "fetcher_mail_signature":"Regards, Mark Spencer,  +917039198547, DvDs Online, email: mark_spencer@xmail.com",
    "fetcher_subject":"Order Details - DVDs Online with Pattern Recognition"
 
 
}
print(getResponse(MyJsonFile))
