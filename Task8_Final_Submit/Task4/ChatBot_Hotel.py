# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 19:56:12 2023

@author: Sabari
"""

import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
import spacy
import en_core_web_sm
from tabulate import tabulate


r=sr.Recognizer()
spacy_model = en_core_web_sm.load()

def speak(text):
    tts=gTTS(text=text,lang='en')
    filename='voice.mp3'
    tts.save(filename)
    playsound(filename)
    os.remove('voice.mp3')

def get_audio():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print('\nSay Now:')
        audio=r.listen(source,10)
        said=""
        try :
            said=r.recognize_google(audio,language='en')
            #print(said)    
        except Exception as e:
            print("{0}".format(e))       
    return said

print('\t\t\t\t\t\tChatBot - Hotel Management\n','\t\t\t\t\t\t##########################')

print('\nDo you want to book a room ? [ Yes / No ]')
speak('Do you want to book a room?')
    
res=get_audio()

if 'yes' or 'i want' or 'yeah' or 'yea' or 'ya' in res:
    #name
    def get_name():
        global name_final,name
        print('\nok, whats your good name?')
        speak('ok, whats your good name?')
        name=get_audio()
        entity_doc = spacy_model(name)
        name_val=[(entity.text, entity .label_) for entity in entity_doc.ents]

        if len(name_val)==0:
            get_name()
        elif len(name_val)>0:
            name_final=name_val[0][0]
            print(f'\nName is {name_final}')
    get_name()
    if name.isnumeric() :
        print('Could you please tell your name correctly')
        speak('could you please tell your name correctly')
        get_name()
        
    #mobile number    
    print('Ok '+name_final+', please tell me your mobile number.')
    speak('ok '+name_final+', please tell me your mobile number.')
    mob=get_audio()
    mob_rep=mob.replace(' ','')
    if len(mob_rep)==10 and mob_rep.isnumeric():
        print(f'Mobile Number is {mob_rep}')
    elif len(mob_rep) < 10:
        print(('I need a 10 digit mobile number, can you please repeat it?'))
        speak('I need a 10 digit mobile number, can you please repeat it?')
        mob=get_audio()
        mob_rep=mob.replace(' ','')
        print(f'Mobile Number is {mob_rep}')
    
    #Address 
    print(f'Ok {name_final}, please tell me your address')
    speak(f'ok {name_final}, please tell me your address')
    address=get_audio()
    print(f'Address is :\n{address}')
    speak('address will be evaluate')
    #ID proof
    print((f'ok {name_final}, Provide your identity proof number like Aadhaar or Passport'))
    speak(f'ok {name_final}, Provide your identity proof number like Aadhaar, or, Passport')
    def ID_proofs():
        global ID_proof
        ID_proof=get_audio()
        i=1
        while len(ID_proof)<5 and i < 3:
            print('Your ID number is less than 5, please provide valid proof, you cannot book a room without ID proof, you have only one chance now.')
            speak('Your ID number is less than 5, please provide valid proof, you cannot book a room without ID proof, you have only one chance now.')
            ID_proofs()
            i=i+1
        if len(ID_proof)>5:
            print(f'ID_proof is {ID_proof}')
    ID_proofs()
    
    #Room Type
    print('which type of room do you want AC or NON-AC?')
    speak('which type of room do you want AC or NON-AC?')
    room_AC=get_audio()
    
    print(' Ok, single room or double room ? ')
    speak(' ok, single room, or, double room ? ')
    room_type=get_audio()
     
    #date of arrival 
    print('Give me your visit date')
    speak('Give me your visit date')
    doa=get_audio()

    #and departure date     
    print('Please give me your departure time')
    speak('Please give me your departure time')
    dep_time=get_audio()
    
    speak('Per day rent is Rs.1200')
    print('Per day rent is Rs.1200')
    print(tabulate([[name_final,mob_rep,address,ID_proof,room_AC,room_type,doa,dep_time]],headers=['Name','Mobile','Address','ID','Room_AC','Room_Type','Arrival','Departure'],tablefmt='grid'))
    speak('Thank you {name_final} , You will happily enjoy your booking date at our hotel, bye')
else:
    speak('Thank you for your interest in our hotel, bye')
 
