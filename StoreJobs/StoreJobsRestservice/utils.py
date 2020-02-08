from bs4 import BeautifulSoup
import re
class Levenshtein:
    @staticmethod
    def get_similarty_percentage(seq1, seq2):
        seq1=seq1.lower()
        seq2=seq2.lower()
        n,m=len(seq1),len(seq2)
        if n==0:
            return m
        elif m==0:
            return n
        if n>m:
            seq1,seq2=seq2,seq1
            m,n=n,m
        p=list()
        i=int()
        j=int()
        upper_left=int()
        upper=int()
        rightJ=str()
        cost=int()
        for i in range(n+1):
            p.insert(i,i)
        for j in range(1,m+1):
            upper_left=p[0]
            rightJ=seq2[j-1]
            p[0]=j
            for i in range(1,n+1):
                upper=p[i]
                cost= 0 if seq1[i-1]==rightJ else 1
                p[i]=min(min(p[i-1]+1,p[i]+1),upper_left+cost)
                upper_left=upper
                
        lev=p[n]
        tot=n+m
        res=float((tot-lev)/tot)
        result=res*100
        return result
class Soup:
    @staticmethod
    def text(data):       
        return re.sub('\s+',' ',BeautifulSoup(data,"html.parser").getText())
