# Keyword Harvester 1.0
The Keyword Harvester is a python script that is built upon the python modules RAKE, Requests, and JSON. This scripts uses SWIM output catalog JSON metadata and focuses on extracting variable descriptions important keyowrds, computing weights for each, associating keywords with their GUID and giving requests to the SWIM Recommender system. 

To try it out:
1) Make sure output-catalog.json and SmartStartlist.txt is in the same directory in this folder. (pending to include catalog sample)
2) Use a command line or terminal to enter SWIM credentials to connect to SWIM Recommender API

## Native Installation

### General Dependencies:
+ Python > 3
+ pip packages from Request, RAKE, and Inflect  recommended to install on python virtual enviroment.
    >> pip install requests
    >> pip install rake-nltk
    >> pip install inflect==0.2.4
    
## Acknowledgements
This material is based upon work supported by the National Science Foundation (NSF) under Grant No. 1835897.   

Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.    

Kenneth Reitz - Author of the Request library code base.
Vishwas B Sharma - Author of the RAKE libary code base.
Gerad Saltion - Author of SMART stop word list
Alex Gronholm - Author of Inflect library code base

## Contributors
Aaron Zambrano

## References:
+ SmartStartList.txt: Listing of stop words from SMART : https://raw.githubusercontent.com/zelandiya/RAKE-tutorial/master/data/stoplists/SmartStoplist.txt

## License 
This software code is licensed under the [GNU GENERAL PUBLIC LICENSE v3.0](./../LICENSE) and uses third party libraries that are distributed under their own terms (see [LICENSE-3RD-PARTY.md](./LICENSE-3RD-PARTY.md)).

## Copyright
© 2019-2023 - University of Texas at El Paso (SWIM Project).


