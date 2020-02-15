from bs4 import BeautifulSoup
import re
from fuzzywuzzy import fuzz
import copy as cp
class Levenshtein:
    @staticmethod
    def get_similarty_percentage(seq1, seq2):
        seq1=seq1.lower()
        seq2=seq2.lower()
        j12=cp.copy(seq1)
        j13=cp.copy(seq2)
        return fuzz.WRatio(j12,j13)
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
        return result,fuzz.WRatio(j12,j13)
class Soup:
    @staticmethod
    def text(data):       
        return re.sub('\s+',' ',BeautifulSoup(data,"html.parser").getText())
seq1="""<span>
</span>

<span>
 Role Designation- Technology Analyst
</span>
<br>
<br>
<span>
 Responsibilities-
 <ul>
<li>
   Ensure effective Design, Development, Validation and Support activities in line with client needs and architectural requirements.,
  </li>
</ul>
<ul>
<li>
   Ensure continual knowledge management.,
  </li>
</ul>
<ul>
<li>
   Adherence to the organizational guidelines and processes
  </li>
</ul>
</span>
<br>
<br>
<span>
 Technical and Professional Requirements- Minimum experience of 4 years required in java.,Should have worked on java development/implementation project.,Knowledge of Spring is an absolute must.,Location of posting is subjected to business requirements.
</span>
<br>
<br>
<p>
<b>
  Educational Requirements:
 </b>
<span>
  BE
 </span>
<br>
<b>
  Service Line:
 </b>
<span>
  Enterprise Package Application Services
 </span>
</p>"""
seq2="""<span>
</span>

<span>
 Role Designation- Technology Analyst
</span>
<br>
<br>
<span>
 Responsibilities-
 <ul>
<li>
   Ensure effective Design, Development, Validation and Support activities in line with client needs and architectural requirements.,
  </li>
</ul>
<ul>
<li>
   Ensure continual knowledge management.,
  </li>
</ul>
<ul>
<li>
   Adherence to the organizational guidelines and processes
  </li>
</ul>
</span>
<br>
<br>
<span>
 Technical and Professional Requirements-
 <ul>
<li>
   Required minimum 4 years of experience in Java, J2EE, Spring, Springboot, Hibernate,Microservices, Webservices, full stack developer,
  </li>
</ul>
<ul>
<li>
   Able to understand SDLC process,
  </li>
</ul>
<ul>
<li>
   Extensive experience designing and,developing RESTful APIs,
  </li>
</ul>
<ul>
<li>
   Extensive coding experience with either Java/J2EE/Spring or Node JS,
  </li>
</ul>
<ul>
<li>
   Location of posting is driven by business requirements
  </li>
</ul>
</span>
<br>
<br>
<p>
<b>
  Educational Requirements:
 </b>
<span>
  BE , BTech , MCA , MTech , MSc
 </span>
<br>
<b>
  Service Line:
 </b>
<span>
  Unit-Engineering services
 </span>
</p>"""
print(Levenshtein.get_similarty_percentage(Soup.text(seq1),Soup.text(seq2)))