# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 14:20:20 2021

@author: Aaron Zambrano
"""
from rake_nltk import Rake
from getpass import getpass
import requests
import json
import urllib3
import inflect

##CONFIGURATIONS
_URL ='http://129.108.18.45:5000/swim-recommender/recommender/db/item/'
_ITEM_URL = 'http://129.108.18.45:5000/swim-recommender/recommender/db/item-keyword/'


'''
Returns a string that contains varDescriptions combined and 
contains a dictionary where they keys are the variables ID and the values are the descriptions
'''
def json_to_python(path = ''):
    data = None
    if path != '':
        with open(path) as f:
            data = json.load(f)
    
    output_string = ''
    #varinfo -list - index 0-> english index 1->spanish
    #each object in varinfo[0] is a dictionary in python
    output_var = dict()
    for obj in data:
        
        output_string += obj['varinfo'][0]['varDescription'] + ' '
        
        #dictionary where keys are $oid and values are the descriptions
        output_var[obj['_id']['$oid']] = obj['varinfo'][0]['varDescription']
        
        
    return output_string, output_var

def json_to_python_db(acc_token):
    urllib3.disable_warnings()
    output_string = ''
    #varinfo -list - index 0-> english index 1->spanish
    #each object in varinfo[0] is a dictionary in python
    output_var = dict()
    
    h= {"Accept": 'application/json',"Content-Type" : 'application/json', 'Authorization' : 'Bearer ' + acc_token}
    r = requests.get('https://services.cybershare.utep.edu/swim-api/swim-api/outputs/' ,headers=h,verify = False)
    data = r.json()['result']
 
    for obj in data:
        
        output_string += obj['varinfo'][0]['varDescription'] + ' '
        
        #dictionary where keys are the id and values are the descriptions
        output_var[obj['_id']] = obj['varinfo'][0]['varDescription']
        
    
    
    return output_string, output_var
    
    

#Returns a stopword text file to a list of words given a stopwords.txt file
def list_stopwords(file):
    stop_words = open(file,"r")
    l = []
    
    for w in stop_words:
        #used in case of multiple words in same line
        #w = w.split()
        w = w.strip()
        l.append(w)
    return l

'''             
Returns a dictionary where keys are the GUID of each output variable and the values are the 
list of associated keywords.
keyword_dict refers a dictionary with keys as keywords and weights as the values.
output_dict refers a dictionary with GUID as keys and output descriptions as values.
'''
def output_dictionary(keyword_dict,output_dict):
    infl = inflect.engine()
    
    if keyword_dict is None:
        print("Keyword dictionary is empty")
        return None
    
    if output_dict is None or len(output_dict) == 0:
        print("Output Dictionary is empty")
        return None
        
    new_dictionary = output_dict.copy()
    
    for key in new_dictionary:
        new_dictionary[key] = []
        
    for w in keyword_dict:
        for output in output_dict:
            if w in output_dict[output].lower() and not infl.singular_noun(w):
                new_dictionary[output] += [(w,keyword_dict[w])]
    
    return new_dictionary

    
#prints a dictionary in the format "Key: Value: "
def print_dict(dictionary):
    for key in dictionary:
        print("Key: ",key , "Value: ", dictionary[key])
    
'''   
Manualy computes keyword weights by word_degree/word_frequency
given a frequency directory and degree directory returned by rake_nltk
Returns a keyword dictionary containing keywords with weights as values.
'''
def keyword_frequency(freq_dic, degree_dic):
    
    keyword = dict()
    
    for w in degree_dic:
        keyword[w] = degree_dic[w] / freq_dic[w]
        
    return keyword

def insert_keywords(url, payload, headers, outputs, items):
    #Items contains a list of dictionarys in keyword data
    item_list = items['data']
    
    r = None
    for item in item_list:
        if item["guid"] in outputs:
            for words in outputs[item["guid"]]:
                payload["keyword"] = words[0]
                payload["item_id"]= item["id"]
                payload["weight"] = int(words[1])
                r =  requests.post(url,headers = headers, data=json.dumps(payload,indent = 4))
                print(r.text)

#Asks user for credentials to connect with Recommendor API    
def credentials():
    print('Welcome! \nPlease enter SWIM Credentials')
    print('--------------------------------------------------------------')
    print('Username is your email address used to register for SWIM 2.4')
    print('Password is the one used to register for SWIM 2.4')
    print('--------------------------------------------------------------')
    valid = False
    r = None
    while(not valid):
        username = input("Username: ")
        password = getpass("Password: ")
        
        payload = {'username' : username,'password' : password}
        headers = {'Accept' : 'application/json', "Content-Type" : 'application/json'}
        
        r =  requests.post("http://129.108.18.45:5000/auth",headers = headers, data=json.dumps(payload))
        
        #json string format
        #print(r.text)
        
        if "Invalid credentials" in r.text:
            print("Username or password not valid")
        else:
            valid = True
        
    r_info = r.json()
    return r_info['access_token']

def output_data(acc_token):
    print("Select option: ")
    print("1. Enter JSON file directory name")
    print("2. Connect to database")
    choice = int(input())
   
    if choice == 1:
        directory = input("Enter JSON file name. Make sure it is saved under the same directory as this script. Do not include .json: ")
        text, outputs = json_to_python(directory + ".json")
        return text, outputs
    if choice == 2:
        text, outputs = json_to_python_db(acc_token)
        return text, outputs
    else:
        print("Invalid choice. Log in and try again")
                
    

if __name__ == "__main__":
    stop_dir = list_stopwords("SmartStoplist.txt")
    acc_token = credentials()
    text, outputs = output_data(acc_token)

    #print(len(outputs))
    
    r = Rake(stop_dir)
    r.extract_keywords_from_text(text)
   
    #returns frequency and degree for each word in a dictionary format
    freq = r.get_word_frequency_distribution()
    degree = r.get_word_degrees()

    keywords = keyword_frequency(freq,degree)
    
    outputs = output_dictionary(keywords, outputs)
    
    #Uncomment to print output dictionary with keywords
    #print_dict(outputs)
    
    head = {'Authorization' : 'Bearer ' + acc_token}
    recommender = requests.get(_URL,headers=head)
    
    #Uncomment to print out output of GET request
    #print(recommender.text)
    
    items = recommender.json()
        
    item_payload =  {"keyword" : "","item_id" : "", "weight" : ""}
    item_head = {'Accept' : 'application/json', "Content-Type" : 'application/json', 'Authorization' : 'Bearer ' + acc_token}
    insert_keywords(_ITEM_URL, item_payload, item_head, outputs, items)
    
    


