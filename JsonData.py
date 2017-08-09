import re
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

def getNameOrMail(text):
    if("@" in text):
        mail = get_mail(text)
        startMail = text.find(mail)
        endMail = startMail+len(mail)
        return {"Start":startMail,"End": endMail,"Mail":mail}
    else:
        to_value_list = text.split()
        FirstName = to_value_list[0]
        LastName = to_value_list[1]
        FirstNameStart = 0
        FirstNameEnd = len(FirstName)-1
        LastNameStart = len(FirstName)+1
        LastNameEnd = LastNameStart+len(LastName)
        return [{"FirstName":FirstName,"Start":FirstNameStart,"End":FirstNameEnd},{"LastName":LastName,"Start":LastNameStart,"End":LastNameEnd}]
def get_mail(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0)

def get_names(text):
    
    st = StanfordNERTagger('./english.all.3class.distsim.crf.ser.gz',
                           './stanford-ner.jar',
                           encoding='utf-8')

    tokenized_text = word_tokenize(text)
    classified_text = st.tag(tokenized_text)
    Names = [tup[0] for tup in classified_text if tup[1] == "PERSON"]
    Names = [str(name) for name in Names]
    return Names
    
     
def getResponse(myDict):
    Subresponses = {} 
    response = {"email_tokens":Subresponses}

    if("to" in myDict.keys()):
        to_data = { k:v for k,v in myDict.items() if 'to' in k }
        to_value = to_data.values()[0]
        Subresponses['to'] = getNameOrMail(to_value)
    if("from" in myDict.keys()):
        from_data = { k:v for k,v in myDict.items() if 'from' in k }
        from_value = from_data.values()[0]
        Subresponses['from'] = getNameOrMail(from_value)
    if("fetcher_mail_signature" in myDict.keys()):
        fet_mail_sign = { k:v for k,v in myDict.items() if 'fetcher_mail_signature' in k }
        sign_value = fet_mail_sign.values()[0]
        if(get_mail(sign_value) is not None):
            sign_mail = get_mail(sign_value)
            start_sign_mail = sign_value.find(sign_mail)
            end_sign_value = start_sign_mail + len(sign_mail)
            Sign_mail_response = {"Start" : start_sign_mail,"End":end_sign_value,"Mail":sign_mail}
        if(len(get_names(sign_value)) != 0):
            allNames = get_names(sign_value)
            if(len(allNames) >= 1):
                FirstName = allNames[0]
                FirstNameStart = sign_value.find(FirstName)
                FirstNameEnd = FirstNameStart + len(FirstName)
                LastName = allNames[1]
                LastNameStart = sign_value.find(LastName)
                LastNameEnd = LastNameStart+len(LastName)
                FirstNameJson = {"FirstName":FirstName,"Start":FirstNameStart,"End":FirstNameEnd}
                LastNameJson = {"LastName":LastName,"Start":LastNameStart,"End":LastNameEnd}

            if(len(allNames) == 1):
                FirstName = allNames[0]
                FirstNameStart = FirstName.find(sign_value)
                FirstNameEnd = FirstNameStart + len(FirstName)
                FirstNameJson = {"FirstName":FirstName,"Start":FirstNameStart,"End":FirstNameEnd}        

        Subresponses['fetcher_mail_signature'] = [Sign_mail_response,FirstNameJson,LastNameJson]

    if("fetcher_subject" in myDict.keys()):
        from_data = { k:v for k,v in myDict.items() if 'fetcher_subject' in k }
        from_value = from_data.values()[0]
    return response
    


MyJsonFile = {   
  "to":"David Letterman ",  
     "from":"Mark Spencer  ",  
     "fetcher_messagebody_text":" my name is Akhilesh yadav I am working in A-Consultancy.",    
     "fetcher_mail_signature":"Regards, Mark Spencer, 400701, DvDs Online, email: mark_spencer@xmail.com ",   
     "fetcher_subject":"abhishek tiwari"
 
}
print(getResponse(MyJsonFile))
