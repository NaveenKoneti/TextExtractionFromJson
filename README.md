Documentation for Text Extraction:

requirements:

-Python
-nltk
-english.all.3class.distsim.crf.ser.gz (Find the file in project folder)
-stanford-ner.jar (Find the file in project folder)

How to Install:
- pip install nltk

How to run the code:
- after the nltk installation is done, go to the directory of the project folder and run `python JsonData.py` 
- If you want to check on another Json file, Replace the variable `MyJsonFile` in the code

Test Cases:

 {   

  "to":"David Letterman ",  
     "from":"Mark Spencer  ",  
     "fetcher_messagebody_text":"I am working in A-Consultancysadfghjklmnb company.",    
     "fetcher_mail_signature":"Regards, Mark Spencer, 400701, DvDs Online, email: mark_spencer@xmail.com ",   
     "fetcher_subject":"abhishek tiwari"
 
}

{   
  "to":"David Letterman ",  
     "from":"Mark Spencer  ",  
     "fetcher_messagebody_text":"In T-consultacy.pvt company I am working on Banking project.",    
     "fetcher_mail_signature":"Regards, Mark Spencer, 400701, DvDs Online, email: mark_spencer@xmail.com ",   
     "fetcher_subject":"abhishek tiwari"
 
}


