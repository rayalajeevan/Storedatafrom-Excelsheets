from bs4 import BeautifulSoup
import re
from fuzzywuzzy import fuzz
import copy as cp
from Levenshtein import ratio

class Levenshtein:
    @staticmethod
    def get_similarty_percentage(seq1, seq2):
        seq1=seq1.lower()
        seq2=seq2.lower()
        res=ratio(seq1,seq2)
        result=res*100
        return result
class Soup:
    @staticmethod
    def text(data):       
        return re.sub('\s+',' ',BeautifulSoup(data,"html.parser").getText())
