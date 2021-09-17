# Keyword Harvester 1.0
The Keyword Harvester is a python script that is built upon the python modules RAKE, Requests, and JSON. This scripts uses SWIM output catalog JSON metadata and focuses on extracting variable descriptions important keyowrds, computing weights for each, associating keywords with their GUID and giving requests to the SWIM Recommender system. 

To try it out:
1) Make sure output-catalog.json and SmartStartlist.txt is in the same directory in this folder
2) Use a command line or terminal to enter SWIM credentials to connect to SWIM Recommender API

## Native Installation

### General Dependencies:
+ Python > 3
+ pip packages from Request, RAKE, and Inflect  recommended to install on python virtual enviroment.
    >> pip install requests
    >> pip install rake-nltk
    >> pip install inflect==0.2.4
    
## Acknowledgements
This material is based upon work supported by NSF Award# XXX-XXXX.

Kenneth Reitz - Author of the Request library code base.
Vishwas B Sharma - Author of the RAKE libary code base.
Gerad Saltion - Author of SMART stop word list
Alex Gronholm - Author of Inflect library code base

## Authors
Developer - XXXX

## License 
GNU GENERAL PUBLIC LICENSE

## References:
+ RAKE : Python implementation of the Rapid Automatic Keyword Extraction algorithm using NLTK https://pypi.org/project/rake-nltk/
+ Requests: Non-GMO HTTP library for Python, safe for human consumption: https://docs.python-requests.org/en/master/
+ JSON: lightweight data interchange format inspired by JavaScript object literal syntax : https://docs.python.org/3/library/json.html
+ Inflect: Correctly generate plurals, singular nouns, ordinals, indefinite articles; convert numbers to words: https://pypi.org/project/inflect/0.2.4/
+ SmartStartList.txt: Listing of stop words from SMART : https://raw.githubusercontent.com/zelandiya/RAKE-tutorial/master/data/stoplists/SmartStoplist.txt
