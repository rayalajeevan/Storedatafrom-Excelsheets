from bs4 import BeautifulSoup
from copy import copy,deepcopy
from .models import BeautifyCompanyJobs
from fuzzywuzzy import fuzz
import re
import json
from copy import deepcopy
class Instructions():
    def __init__(self,instruction_id,html_data):
        self.instructions_dictionary={
        36:self.rule_no_36,
        35:self.rule_no_35,
        30:self.rule_no_30,
        28:self.rule_no_28,
        26:self.rule_no_26,
        1:self.rule_no_1,
        2:self.rule_no_2,
        3:self.rule_no_3,
        4:self.rule_no_4,
        5:self.rule_no_5,
        6:self.rule_no_6,
        8:self.rule_no_8,
        9:self.rule_no_9,
        10:self.rule_no_10,
        7:self.rule_no_7,
        11:self.rule_no_11,
        12:self.rule_no_12,
        13:self.rule_no_13,
        14:self.rule_no_14,
        15:self.rule_no_15,
        16:self.rule_no_16,
        17:self.rule_no_17,
        18:self.rule_no_18,
        19:self.rule_no_19,
        20:self.rule_no_20,
        21:self.rule_no_21,
        22:self.rule_no_22,
        23:self.rule_no_23,
        24:self.rule_no_24,
        25:self.rule_no_25,
        27:self.rule_no_27,
        29:self.rule_no_29,
        31:self.rule_no_31,
        32:self.rule_no_32,
        33:self.rule_no_33,
        34:self.rule_no_34,
        37:self.rule_no_37,
        38:self.rule_no_38,
        39:self.rule_no_39,
        }
        self.instruction_id=instruction_id
        self.html_data=html_data
    def method_caller(self):
        return self.instructions_dictionary.get(self.instruction_id)()
    def rule_no_1(self):
        """
        companies Under This Function--
            Hill And Knowlton Strategies Llc
        """
        soup=None
        values=["JOBTITLE:","LOCATION:","REPORT TO:","CONTRACT:","JOBDESCRIPTION",'title','REPORT','LOCATION',"ROLE:"]
        for key in ['job_description']:
            html_dct_val=self.html_data.get(key)
            if html_dct_val!=None:
                soup=BeautifulSoup(html_dct_val,'html.parser')
                for strong in soup.findAll(['strong','h1','h2','h3','h4','p']):
                    for val in values:
                        if strong.name=="strong":
                            if val.lower() in  strong.getText().lower():
                                if strong.parent!=None and len(strong.parent.getText())<=100:
                                    strong.parent.decompose()
                                else:
                                    strong.decompose()
                # for em in soup.findAll('em'):
                #     if em.parent!=None:
                #         em.parent.decompose()
                #     else:
                #         em.decompose()
            self.html_data[key]=str(soup)
        return self.html_data
    def rule_no_2(self):
        """
        companies Under This Function--
                    Google
        """
        Note_tag=None
        for key in ['job_description']:
            html_dct_val=self.html_data.get(key)
            if html_dct_val!=None:
                soup=BeautifulSoup(html_dct_val,'html.parser')
                for strong in [soup.find('p',{'class':'gc-job-detail__instruction-description'})]:
                    if strong!=None:
                        if 'Note:' in strong.getText().strip():
                            Note_tag=copy(str(strong).split('Note:')[1])
                for strong in [soup.find('div',{'id':'location'}),soup.find('div',{'class':'gc-job-detail__section gc-job-detail__instruction'}),soup.find('div',{'class':'gc-office-map'}),soup.find('a',{'class':'gc-button gc-button--primary gc-button--raised gc-button--icon gc-job-detail__floating-cta gc-sticky-button'})]:
                    if strong!=None:
                        strong.decompose()
                for strong in soup.findAll('svg'):
                    if strong!=None:
                        strong.decompose()
            if Note_tag==None:
                self.html_data[key]=str(soup)
            else:
                self.html_data[key]=str(soup)+"<strong>Note:"+str(Note_tag)+"<strong>"
        return self.html_data
    def rule_no_3(self):
        """
        companies Under This Function--
                    Toyota
        """
        for key in ['job_location']:
            html_dct_val=self.html_data.get(key)
            if html_dct_val!=None:
                html_dct_val=html_dct_val.split('-')
                if len(html_dct_val)>1:
                    html_dct_val=html_dct_val[2]
                    if '/' in html_dct_val:
                        html_dct_val=html_dct_val.split('/')
                        html_dct_val=html_dct_val[0]
                    if len(html_dct_val)==2:
                        html_dct_val=self.html_data.get(key).split('-')
                        html_dct_val=html_dct_val[3]
            self.html_data[key]=html_dct_val
        return self.html_data
    def rule_no_4(self):
        """
        companies Under This Function--
                    owens corning
        """
        values=['Job Title:','Department:','Reports to:','FLSA Status','HR Rep','Hiring Manager','Job Band','Date','Supervises','OC Business Title:',"Location:",'Shift:','Pay rate:','Overtime Status:']
        for key in ['job_description']:
            html_dct_val=self.html_data.get(key)
            if html_dct_val!=None:
                soup=BeautifulSoup(html_dct_val,'html.parser')
                for span in soup.findAll(['span','strong']):
                    if 'location' in span.getText().lower():
                        if span.parent!='[document]':
                            if span.parent!=None:
                                span.parent.decompose()
                for span in soup.findAll(['p']):
                    if 'Shift:' in span.getText():
                        if span.findNext('p')!=None:
                            if span.findNext('p').getText().strip() not in values:
                                span.findNext('p').decompose()
                for span in soup.findAll(['p']):
                    for val in values:
                        if val in span.getText():
                            if val!='Job Band':
                                if len(span.getText().lower().strip())>len(val)+3:
                                    for child in span.findChildren(recursive=False):
                                        child.decompose()
                                else:
                                    if span.findNext('p')!=None:
                                        for child in span.findNext('p').findChildren(recursive=False):
                                            child.decompose()
                                span.decompose()
                            else:
                                if len(span.getText().lower().strip())>len(val)+1:
                                    for child in span.findChildren(recursive=False):
                                        child.decompose()
                                else:
                                    if span.findNext('p')!=None:
                                        for child in span.findNext('p').findChildren(recursive=False):
                                            child.decompose()
                                            span.findNext('p').decompose()
                                span.decompose()
                for span in soup.findAll(['span']):
                    for val in values:
                        if val!='Job Band':
                            if val in span.getText():
                                if len(span.getText().lower().strip())>len(val)+3:
                                    for child in span.findChildren(recursive=False):
                                        child.decompose()
                                else:
                                    if span.findNext('p')!=None:
                                        for child in span.findNext('p').findChildren(recursive=False):
                                            child.decompose()
                                span.decompose()
                        else:
                            if val in span.getText():
                                if len(span.getText().lower().strip())>len(val)+1:
                                    for child in span.findChildren(recursive=False):
                                        child.decompose()
                                else:
                                    if span.findNext('span')!=None:
                                        for child in span.findNext('span').findChildren(recursive=False):
                                            child.decompose()
                                        span.findNext('span').decompose()
                                span.decompose()
            self.html_data[key]=str(soup).replace('&lt;_x00C_ont&gt;&lt;_x00C_ont&gt;','')
            self.html_data[key]=self.html_data[key].replace('&lt;ont&gt;&lt;ont&gt;','')
            self.html_data[key]=self.html_data[key].replace(self.html_data.get('job_title').replace('/',' '),'')
            self.html_data[key]=self.html_data[key].replace(self.html_data.get('job_title').replace('/',' ').upper(),'')
            self.html_data[key]=self.html_data[key].replace('&lt;_x00C_ont&gt;&lt;_x00C_ont&gt;','')
        return self.html_data
    def rule_no_5(self):
        """
        companies Under This Function--
                    roche
        """
        for key in ['job_description']:
            data=self.html_data[key]
            soup=BeautifulSoup(str(data),"html.parser")
            for bold in soup.findAll('b'):
                matchcase=0
                for x in str(self.html_data.get('job_title')).strip().split():
                    for y in bold.getText().strip().split():
                        if x.strip()==y.strip():
                            matchcase+=1
                if matchcase > len(str(self.html_data.get('job_title')).strip().split())-4:
                    bold.decompose()
            for bold in soup.findAll(['b','p']):
                for val in ['job title','travel','start date','duration','workload','travel requirement','Territory','work schedule','primary location']:
                    if val.lower() in bold.getText().strip().lower():
                        if bold.findNext('span')!=None:
                            bold.findNext('span').decompose()
                            bold.decompose()
                    if 'location' in bold.getText().strip().lower():
                        if 'miles'  in bold.findNext('p').getText().strip().lower():
                            bold.findNext('p').decompose()
                        bold.decompose()
                    if val.lower() in bold.getText().strip().lower():
                        bold.decompose()
            self.html_data[key]=str(soup)
        return self.html_data
    def rule_no_6(self):
        location=self.html_data['job_location'].split('-')
        if len(location)==4:
            location='-'.join(location[0:3])
            self.html_data['job_location']=location
        return self.html_data
    def rule_no_8(self):
        for key in ['job_description']:
            data=self.html_data[key]
            soup=BeautifulSoup(str(data),"html.parser")
            for strong in soup.findAll('strong'):
                if 'location' in strong.get_text().lower():
                    if strong.parent.name=='p':
                        if len(strong.parent.get_text().strip())>9:
                            strong.parent.decompose()
                            break
                        else:
                            if strong.parent.findNext('p')!=None:
                                strong.parent.findNext('p').decompose()
                                strong.parent.decompose()
                                break
            self.html_data[key]=str(soup)
        return self.html_data
    def rule_no_9(self):
        """
        Siemines
        """
        for key in ['job_description']:
            data=self.html_data[key]
            data=re.sub('\s+',' ',str(data))
            soup=BeautifulSoup(str(data),"html.parser")
            for p in soup.findAll(['P','article']):
                if "Job ID:" in p.get_text().strip() or 'Location:' in p.get_text().strip() or 'Organization:' in p.get_text().strip() or 'Job Type:' in p.get_text().strip() or 'Department:' in p.getText().strip() or 'Position' in p.getText().strip() or 'Job Family:' in p.getText().strip() or 'Position Title:' in p.getText().strip():
                    if p.name=='p':
                        if 'Position Title:' in p.getText().strip():
                            print("hello")
                        if len(p.getText.strip())<=100:
                            p.decompose()
                    else:
                        child=p.findChildren('div')
                        if len(child)!=0:
                            for ch in child:
                                if ch.name=='div':
                                    p=re.findall('(?<=<article)(.+?)<div',str(p))
                                    if len(p)!=0:
                                        soup=str(soup).replace(p[0],'').replace('<article<p style="MARGIN: 0in 0in 10pt">','').replace('<article','')
                                        break


                        p=re.findall('(?<=<article)(.+?)<p',str(p))
                        if len(p)!=0:
                            soup=str(soup).replace(p[0],'').replace('<article<p style="MARGIN: 0in 0in 10pt">','').replace('<article','')
                            break
            soup=BeautifulSoup(str(soup),"html.parser")
            for div in soup.findAll(['div','p']):
                if "Job ID:" in div.get_text().strip() or 'Location:' in div.get_text().strip() or 'Organization:' in div.get_text().strip() or 'Company:' in div.get_text().strip() or 'Experience Level:' in div.get_text().strip() or 'Job Type:' in div.get_text().strip() or 'Department:' in div.getText().strip() or 'Position' in div.getText().strip() or 'Job Family:' in div.getText().strip():
                    if len(div.getText().strip())<=100:
                        div.decompose()
                    else:
                        for chdiv in div.findChildren():
                            if "Job ID:" in chdiv.get_text().strip() or 'Location:' in chdiv.get_text().strip() or 'Organization:' in chdiv.get_text().strip() or 'Company:' in chdiv.get_text().strip() or 'Experience Level:' in chdiv.get_text().strip() or 'Job Type:' in chdiv.get_text().strip() or 'Department:' in chdiv.getText().strip() or 'Position' in chdiv.getText().strip() or 'Job Family:' in chdiv.getText().strip():
                                if len(chdiv.getText().strip())<=100:
                                    div.decompose()

            self.html_data[key]=str(soup)
        return self.html_data
    def rule_no_10(self):
        """
        Volkswagon
        """
        for key in ['job_description']:
            data=self.html_data[key]
            data=re.sub('\s+',' ',str(data))
            soup=BeautifulSoup(str(data),"html.parser")
            for h in soup.findAll(['h2','span','p','span','b']):
                if 'Primary Location' in h.get_text().strip():
                    if h.parent('div')!=None:
                        if len(h.parent.get_text().strip())<=100:
                            h.parent.decompose()
                            continue
                data=re.findall(r'\((.+?)\)',h.getText().strip().lower())
                if len(data)>0:
                    data=data[0]
                else:
                    data=''
                if fuzz.ratio(h.getText().strip().lower().replace(data,''),self.html_data.get('job_title','qwertyuiopasdfghjklzxcvbnm').lower())>50:
                    if h.parent('div')!=None:
                        if len(h.parent.get_text().strip())<=100:
                            h.parent.decompose()
                            continue
                        else:
                            h.decompose()
                    elif h.name=='p':
                        if len(h.get_text().strip())<=100:
                            h.decompose()
                            continue
                if (h.name=='p' or h.name=='b') and 'Start Date:' in h.getText().strip():
                    if len(h.get_text().strip())<=100:
                        h.decompose()
                if (h.name=='p' or h.name=='b') and 'months' in h.getText().strip().lower() and  'time' in h.getText().strip().lower():
                    if len(h.get_text().strip())<=60:
                        h.decompose()
                if (h.name=='p' or h.name=='b') and 'year' in h.getText().strip().lower() and  'time' in h.getText().strip().lower():
                    if len(h.get_text().strip())<=60:
                        h.decompose()
            self.html_data[key]=str(soup).replace('Description','')
        return self.html_data
    def rule_no_7(self):
        """
        sas
        """
        for key in ['job_description']:
            data=self.html_data[key]
            data=re.sub('\s+',' ',str(data))
            soup=BeautifulSoup(str(data),"html.parser")
            for h in soup.findAll():
                if h.name=='em':
                    h.decompose()
                if fuzz.ratio(h.getText().strip().lower(),self.html_data.get('job_title','').lower())>45:
                    if h.parent('div')!=None:
                        if len(h.parent.get_text().strip())<=100:
                            h.parent.decompose()
                            continue
                        else:
                            h.decompose()
                    elif h.name=='p':
                        if len(h.get_text().strip())<=100:
                            h.decompose()
                            continue
                if fuzz.ratio(h.getText().strip().lower(),'Company Overview')>80:
                    h.decompose()
            for data in [soup.find('div',{'role':'list'}),soup.find('div',{'class':'iCIMS_JobOptions'}),soup.find('div',{'class':'iCIMS_PageFooter'}),soup.find('div',{'class':'iCIMS_Logo'})]:
                if data!=None:
                    data.decompose()
            for p in soup.findAll('p'):
                if 'Job Title:' in p.getText().strip():
                    if len(p.getText().strip())<=200:
                        p.decompose()
                elif 'Department:'  in p.getText().strip():
                    if len(p.getText().strip())<=200:
                        p.decompose()
                elif 'Location:' in p.getText().strip():
                    if len(p.getText().strip())<=200:
                        p.decompose()
                elif  'Reports To:' in p.getText().strip():
                    if len(p.getText().strip())<=200:
                        p.decompose()
            self.html_data[key]=str(soup)
        return self.html_data
    def rule_no_11(self):
        """
        Anthem
        """
        for key in ['job_description']:
            data=self.html_data[key]
            data=re.sub('\s+',' ',str(data))
            soup=BeautifulSoup(str(data),"html.parser")
            for div in soup.findAll(['div','p']):
                if 'Location:' in div.getText().strip() or  'Work location:' in div.getText().strip():
                    if len(div.getText().strip())<=70:
                        div.decompose()
                elif 'Work Hours:' in div.getText().strip() or 'Internal Job Title:'  in div.getText().strip():
                     if len(div.getText().strip())<=70:
                         div.decompose()

            for div in soup.findAll():
                if str(self.html_data.get('job_title')) in div.getText().strip():
                    if fuzz.ratio(div.getText().strip(),self.html_data.get('job_title'))>30:
                        div.decompose()
            self.html_data[key]=str(soup)
        return self.html_data
    def rule_no_12(self):
        """
        Cap Gemini
        """
        for key in ['job_description']:
            data=self.html_data[key]
            data=re.sub('\s+',' ',str(data))
            soup=BeautifulSoup(str(data),"html.parser")
            for div in soup.findAll(['p','div','span']):
                if 'Location:' in div.getText().strip() or 'Job Title' in div.getText().strip() or 'Job Type:' in div.getText().strip() or 'Experience:' in div.getText().strip() or 'Job Role:' in div.getText().strip()  or 'Salary:' in div.getText().strip() or 'Closing Date:' in div.getText().strip() or 'Intake:' in div.getText().strip()or 'Intakes:' in div.getText().strip()or 'Role:' in div.getText().strip()  or 'Location' in div.getText().strip() or 'Learn more about' in div.getText().strip() or 'Business Area:' in div.getText().strip() or 'Reporting to:' in div.getText().strip() or 'Duration' in div.getText().strip() or 'Title' in div.getText().strip() or 'Primary skill:' in div.getText().strip() or 'Position:' in div.getText().strip():
                    if len(div.getText().strip())<100:
                        div.decompose()
                    else:
                        for chdiv in div.findChildren():
                            if 'Location:' in chdiv.getText().strip() or 'Job Title' in chdiv.getText().strip() or 'Job Type:' in chdiv.getText().strip() or 'Experience:' in chdiv.getText().strip() or 'Job Role:' in chdiv.getText().strip()  or 'Salary:' in chdiv.getText().strip() or 'Closing Date:' in chdiv.getText().strip() or  'Intake:' in chdiv.getText().strip() or 'Intakes:' in chdiv.getText().strip() or 'Role:' in chdiv.getText().strip() or 'Location' in chdiv.getText().strip() or  'Learn more about' in chdiv.getText().strip() or 'Business Area:' in chdiv.getText().strip() or 'Reporting to:' in chdiv.getText().strip() or 'Duration' in chdiv.getText().strip() or 'Title' in chdiv.getText().strip()   or 'Primary skill:' in chdiv.getText().strip() or 'Position:' in chdiv.getText().strip():
                                if len(chdiv.getText().strip())<100:
                                    chdiv.decompose()
                if 'Experience Required' in div.getText().strip() or 'Contact Person' in div.getText().strip():
                    if len(div.getText().strip())<100:
                        div.decompose()
                    else:
                        for chdiv in div.findChildren():
                            if 'Experience Required' in chdiv.getText().strip() or 'Contact Person' in chdiv.getText().strip():
                                if len(chdiv.getText().strip())<100:
                                    chdiv.decompose()
                if 'may be required' in div.getText().strip() and '-' in div.getText().strip():
                    if len(div.getText().strip())<100:
                        div.decompose()
                    else:
                        for chdiv in div.findChildren():
                            if 'may be required' in chdiv.getText().strip() and '-' in chdiv.getText().strip():
                                if len(chdiv.getText().strip())<100:
                                    chdiv.decompose()
                if fuzz.ratio(div.getText().strip(),self.html_data.get('job_location',''))>=50 or fuzz.ratio(div.getText().strip(),self.html_data.get('job_title'))>50:
                    div.decompose()
            for span in soup.findAll('span'):
                if 'Accounts Payable' in span.getText().strip():
                    if len(span.getText().strip())<100:
                        span.decompose()
                    else:
                        for chdiv in div.findChildren():
                            if 'may be required' in chdiv.getText().strip() and '-' in chdiv.getText().strip():
                                if len(chdiv.getText().strip())<100:
                                    chdiv.decompose()
            if 'About Capgemini' in str(soup):
                self.html_data[key]=str(soup).replace('Role description:-','').replace('Short Description','').replace("JD",'')
            else:
                self.html_data[key]=str(soup).replace('Job Description:','').replace('Role description:-','').replace('Job Description','').replace('Short Description','').replace("JD",'').replace('JOB DISCRIPTION:','').replace('Job description','')
        return self.html_data
    def rule_no_13(self):
        """
        geico
        """
        for key in ['job_description']:
            data=self.html_data[key]
            data=re.sub('\s+',' ',str(data))
            soup=BeautifulSoup(str(data),"html.parser")
            for strong in [soup.find('p',{'class':'info_box_fields'})]:
                if strong!=None:
                    strong.decompose()
            for div in soup.findAll('div'):
                if 'Salary-' in div.getText() or 'Part Time-' in div.getText():
                    if len(div.getText().strip())<80:
                        div.decompose()
                    else:
                        for chdiv in div.findChildren():
                            if 'Salary:' in chdiv.getText().strip() or 'Part Time-' in div.getText():
                                if len(chdiv.getText().strip())<80:
                                    chdiv.decompose()
            for div in soup.findAll():
                if 'How to Apply' in div.getText():
                    if len(div.getText().strip())<600:
                        div.decompose()
                    else:
                        for chdiv in div.findChildren():
                            if 'How to Apply' in chdiv.getText() or 'Apply for Job' in chdiv.getText():
                                if len(chdiv.getText().strip())<600:
                                    chdiv.decompose()
            self.html_data[key]=str(soup)
        return self.html_data
    def rule_no_14(self):
        """
        Amazon.com Inc
        """
        for key in ['job_description']:
            replacer_data=[]
            data=self.html_data[key]
            data=re.sub('\s+',' ',str(data))
            soup=BeautifulSoup(str(data),"html.parser")
            for span in soup.findAll(['p']):
                if "**" in span.getText().strip():
                    replacer=re.findall(r'\*\*(.+?)</p>',str(span))
                    if replacer!=None:
                        replacer_data.append(replacer[0])
                if "Have questions about this role?" in span.getText().strip():
                    replacer=re.findall(r'Have questions about(.+?)today!',str(span))
                    if replacer!=[]:
                        replacer_data.append("Have questions about"+replacer[0]+"today!")
            for b in soup.findAll(['b','span']):
                if 'Shifts:' in b.getText():
                    if len(b.getText().strip())<=25:
                        b.decompose()
                if 'night' in b.getText().strip() or 'Morning' in b.getText().strip() or 'Evening' in b.getText().strip() or 'Weekend' in b.getText().strip():
                    if len(b.getText().strip())<=100:
                        b.decompose()
                if 'Location' in b.getText().strip() and b.name=='b':
                    if b.findNext('br')!=None:
                        if b.findNext('br').findNext('span')!=None:
                            if len( b.findNext('br').findNext('span')) <=100:
                                   b.findNext('br').findNext('span').decompose()
                            if len(b.getText().strip())<=50:
                                b.decompose()
                if 'Salary' in b.getText().strip() and b.name=='b':
                    if b.findNext('br')!=None:
                        if b.findNext('br').findNext('span')!=None:
                            if len( b.findNext('br').findNext('span')) <=100:
                                   b.findNext('br').findNext('span').decompose()
                            if len(b.getText().strip())<=50:
                                b.decompose()
            for title in soup.findAll():
                if fuzz.ratio(title.getText().strip(),self.html_data.get('job_title',''))>=50:
                    title.decompose()
                # if title.name=='br':
                #     if title.findNext().name=='br':
                #         title.findNext().decompose()
                #         title.decompose()

            if len(replacer_data)>0:
                for x in replacer_data:
                    soup=str(soup).replace(x,'').replace("**",'').replace('https://bit.ly/2RzuuZW','')
            self.html_data[key]=str(soup)
            job_id=self.html_data.get('job_id','')
            if "CLOSE" not in job_id:
                job_id =job_id+"CLOSE"
            id=re.findall(r'\|(.+?)CLOSE',job_id)
            if id!=[]:
                self.html_data['job_id']=job_id.replace(id[0],'')
            self.html_data['job_id']=self.html_data['job_id'].replace('|','').replace("CLOSE",'')
        return self.html_data
    def rule_no_15(self):
        """
        Morgan Staneley
        """
        for key in ['job_description']:
            replacer_data=[]
            data=self.html_data[key]
            data=re.sub('\s+',' ',str(data))
            soup=BeautifulSoup(str(data),"html.parser")
            for span in soup.findAll('div'):
                if 'LOCATION' in span.getText().strip().upper() or 'POSTING DATE' in span.getText().strip().upper() or 'JOB' in span.getText().strip().upper() or 'EMPLOYMENT TYPE' in span.getText().strip().upper() or 'JOB LEVEL:' in span.getText().strip().upper() or 'EDUCATION LEVEL' in span.getText().strip().upper() or 'JOB NUMBER' in span.getText().strip().upper():
                    if len(span.getText().strip())<80:
                        span.decompose()
            self.html_data[key]=str(soup)
        return self.html_data
    def rule_no_16(self):
        """
        American Rivers
        """
        for key in ['job_description']:
            data=self.html_data[key]
            data=re.sub('\s+',' ',str(data))
            soup=BeautifulSoup(str(data),"html.parser")
            for x in soup.findAll('p'):
                if 'CLASSIFICATION:' in  x.getText().strip():
                    if len(x.getText())<600:
                        x.decompose()
            self.html_data[key]=str(soup)
        return self.html_data
    def rule_no_17(self):
        """
        Thermo fisher scientific inc
        """
        for key in ['job_description']:
            data=self.html_data[key]
            data=re.sub('\s+',' ',str(data))
            soup=BeautifulSoup(str(data),"html.parser")
            for x in soup.findAll():
                if "Location" in x.getText().strip() or "Objective" in x.getText().strip() or ('Job' in x.getText().strip() and 'Title' in x.getText().strip())  or  ('Requisition' in x.getText().strip() and 'ID' in x.getText().strip()) or ('Job' in x.getText().strip() and 'ID' in x.getText().strip()) :
                    if len(x.parent.getText().strip())>3 and len(x.parent.getText().strip())<=200:
                        x.parent.decompose()
                    else:
                        if len(x.getText().strip())>3 and len(x.getText().strip())<=100:
                            x.decompose()
            self.html_data[key]=str(soup).replace('Requisition ID','').replace(self.html_data['job_id'],'').replace(self.html_data['job_title'],'').replace(':',' ').replace('-',' ')
        return self.html_data
    def rule_no_18(self):
        """
        Asurion
        """
        for key in ['job_description']:
            data=self.html_data[key]
            data=re.sub('\s+',' ',str(data))
            soup=BeautifulSoup(str(data),"html.parser")
            for x in soup.findAll():
                if 'Location' in x.getText().strip() or 'Regular Priority Jobs' in x.getText().strip() or 'Job Title' in x.getText().strip() or 'Department:' in x.getText().strip() or 'Reports To:' in x.getText().strip() or 'FLSA Status:' in x.getText().strip() or 'Market starting pay' in x.getText().strip():
                    if x.parent!=None:
                        if len(x.parent.getText().strip())<=200:
                            x.parent.decompose()
                    else:
                        if len(x.getText().strip())<=200:
                            x.decompose()
            if len(str(soup).strip().split('|'))>=3:
                soup=str(soup)+" CLOSE"
                id=re.findall(r'{id}(.+?)CLOSE'.format(id=self.html_data['job_id'].upper()),soup)
                if id!=[]:
                    for x in id[0].split('|'):
                        if x.strip()!='':
                            soup=soup.replace(x,'')
                    self.html_data[key]=soup.replace(id[0].strip().replace("</div>",''),'')
            self.html_data[key]=str(soup).replace('CLOSE','').replace(self.html_data['job_id'].upper(),'').replace('|',' ')
        return self.html_data
    def rule_no_19(self):
        """
        Nielsan company usa inc
        """
        for key in ['job_description']:
            data=self.html_data[key]
            data=re.sub('\s+',' ',str(data))
            soup=BeautifulSoup(str(data),"html.parser")
            for x in soup.findAll():
                if 'Role Description:'  in x.getText().strip() or  'Designation:'in  x.getText().strip() or 'Unit:' in x.getText().strip() or 'Job Type' in x.getText().strip() or 'Location' in x.getText().strip() or 'Travel' in x.getText().strip():
                    if x.parent!=None:
                        if len(x.parent.getText().strip())<=200:
                            x.parent.decompose()
                        else:
                            if len(x.getText().strip())<=150:
                                x.decompose()
                    else:
                        if len(x.getText().strip())<=150:
                            x.decompose()
            for x in soup.findAll('p'):
                if fuzz.ratio(x.getText().strip().lower(),self.html_data['job_title'])>45:
                    if len(x.getText().strip())<=150:
                        x.decompose()
                if fuzz.ratio(x.getText().strip().lower(),self.html_data['job_location'])>50:
                    if len(x.getText().strip())<=150:
                        x.decompose()
            self.html_data[key]=str(soup)
        return self.html_data
    def rule_no_20(self):
        """
        ABC NEWS
        """
        for key in ['job_description']:
            data=self.html_data[key]
            data=re.sub('\s+',' ',str(data))
            soup=BeautifulSoup(str(data),"html.parser")
            for x in soup.findAll(['p']):
                if 'Job no:' in x.getText().strip() or 'Work type:' in x.getText().strip() or 'Location:' in x.getText().strip() or 'Categories:' in x.getText().strip() or 'Advertised:' in x.getText().strip() or 'Applications close:' in x.getText().strip() or 'Apply now' in x.getText().strip() or 'Back to search results' in x.getText().strip() or 'Employee Referral' in x.getText().strip() :
                    if len(x.getText().strip())<=400:
                        x.decompose()
            self.html_data[key]=str(soup)
        return self.html_data
    def rule_no_21(self):
        """
        THE MIAMI HEARALD
        """
        for key in ['job_description']:
            data=self.html_data[key]
            data=re.sub('\s+',' ',str(data))
            soup=BeautifulSoup(str(data),"html.parser")
            for x in soup.findAll(['p']):
                if 'Classification:' in x.getText().strip() or 'Reports to:' in x.getText().strip() or 'Mission Statement:' in x.getText().strip() or 'Vision Statement:' in x.getText().strip() or 'Core Values:' in x.getText().strip() or 'General:' in x.getText().strip() or 'Hours:' in x.getText().strip() or 'Title:' in x.getText().strip() or 'Fort Lauderdale Marriott North' in x.getText().strip():
                    if len(x.getText().strip())<=400:
                        x.decompose()
                if 'Monday' in x.getText().strip() or 'Tuesday' in x.getText().strip() or 'Wednesday' in x.getText().strip() or 'Thursday' in x.getText().strip() or 'Friday' in x.getText().strip() or "Saturday" in x.getText().strip() or 'Sunday' in x.getText().strip():
                    if len(x.getText().strip())<=200:
                        x.decompose()
            self.html_data[key]=str(soup)
        return self.html_data
    def rule_no_22(self):
        """
        NPR
        """
        for key in ['job_location']:
            data=self.html_data[key]
            if 'not specified' in data.lower():
                data='Washington D.C, United States'
            self.html_data[key]=str(data)
        return self.html_data
    def rule_no_23(self):
        """
        The Baltimore Sun
        """
        for key in ['job_description']:
            data=self.html_data[key]
            data=re.sub('\s+',' ',str(data))
            soup=BeautifulSoup(str(data),"html.parser")
            for x in soup.findAll(['p','a']):
                if 'Apply now' in x.getText().strip() or 'Job no:' in x.getText().strip() or 'Work type:' in x.getText().strip() or 'Location:' in x.getText().strip()  or 'Categories:' in x.getText().strip():
                    if len(x.getText().strip())<=200:
                        x.decompose()
            for x in soup.findAll('span'):
                if 'LOCATION' in x.getText().strip():
                    if len(x.getText().strip())<=500:
                        x.decompose()
            for x in soup.findAll('p'):
                if 'Department' in x.getText().strip():
                    if x.parent!=None and x.parent.name=='p' and len(x.getText().strip())==10:
                        x.parent.decompose()
            self.html_data[key]=str(data)
        return self.html_data
    def rule_no_24(self):
        """
        The prinicipal Financial group
        """
        for key in ['job_location']:
            data=self.html_data[key]
            if len(data.split(','))>3:
                data=data.split(',')[1]
            self.html_data[key]=str(data)
        return self.html_data
    def rule_no_25(self):
        """
        Praxair
        """
        for key in ['job_description']:
            data=self.html_data[key]
            data=re.sub('\s+',' ',str(data))
            soup=BeautifulSoup(str(data),"html.parser")
            for x in soup.findAll():
                if 'Position will be filled at a level' in x.getText().strip():
                    if len(x.getText().strip())<=200:
                        x.decompose()
            for x in soup.findAll('p'):
                if 'Location:' in x.getText().strip():
                    if x.findNext('font')!=None:
                        if len(x.findNext('font').getText().strip()) <=50:
                            x.findNext('font').decompose()
                            x.decompose()
            self.html_data[key]=str(data)
        return self.html_data
    def rule_no_26(self):
        """
        Supervalu Inc
        """
        for key in ['job_location']:
            location=self.html_data[key]
            if len(location.split(','))>=2:
                data=''
                for k in range(1,len(location.split(','))):
                    data=data+" "+location.split(',')[k]
                self.html_data[key]=str(data).strip()
        return self.html_data
    def rule_no_27(self):
        """
        sehlumberger limited
        """
        for key in ['job_description']:
            data=self.html_data[key]
            data=re.sub('\s+',' ',str(data))
            soup=BeautifulSoup(str(data),"html.parser")
            for div in soup.findAll(['div','p']):
                if 'location:' in div.getText().strip().lower() or 'job title:' in div.getText().strip().lower() :
                    if len(div.getText().strip())<=200:
                        div.decompose()
            self.html_data[key]=str(soup)
        return self.html_data
    def rule_no_28(self):
        """
        Long Wood Gardens
        """
        for key in ['apply_link']:
            if '? ' in self.html_data[key]:
                self.html_data[key]=self.html_data[key]+"&ATSPopupJob="+str(self.html_data['job_id'])
            else:
                self.html_data[key]=self.html_data[key]+"?ATSPopupJob="+str(self.html_data['job_id'])
        return self.html_data
    def rule_no_29(self):
        """
        Library of congress
        """
        for key in ['job_description']:
            data=self.html_data[key]
            data=re.sub('\s+',' ',str(data))
            soup=BeautifulSoup(str(data),"html.parser")
            for div in soup.findAll(['li','p','span']):
                if 'availability:' in div.getText().strip().lower() or 'tour of duty:' in div.getText().strip().lower() :
                    if len(div.getText().strip())<=250:
                        div.decompose()
                if 'duties:'  in div.getText().strip().lower():
                    div.decompose()
            self.html_data[key]=str(soup)
        return self.html_data
    def rule_no_30(self):
        """
        new well brands
        """
        for key in ['job_description']:
            data=self.html_data[key]
            data=re.sub('\s+',' ',str(data))
            soup=BeautifulSoup(str(data),"html.parser")
            for div in soup.findAll(['p','div']):
                if 'Position Title:' in div.getText().strip() or 'Reports to:' in div.getText().strip() or 'Location:' in div.getText().strip() :
                    if len(div.getText().strip())<=200:
                        div.decompose()
            self.html_data[key]=str(soup)
        return self.html_data
    def rule_no_31(self):
        """
        Northeast Utilities Service Company
        """
        for key in ['job_location']:
            value=self.html_data.get(key)
            if len(value.split(','))>2:
                if len(value.split(','))==3:
                    value=' '.join(value.split(',')[-1:-3:-1])
                elif len(value.split(','))>3:
                    value=' '.join(value.split(',')[-1:-4:-1])
            self.html_data[key]=str(value)
        return self.html_data
    def rule_no_32(self):
        """
        Navigant
        """
        for key in ['apply_link']:
            if '? ' in self.html_data[key]:
                self.html_data[key]=self.html_data[key]+"&JobOpeningId="+str(self.html_data['job_id'])
            else:
                self.html_data[key]=self.html_data[key]+"?JobOpeningId="+str(self.html_data['job_id'])
        return self.html_data
    def rule_no_33(self):
        """
        ING
        """
        for key in ['job_location']:
            location=self.html_data[key]
            modified_location=None
            if len(location.split('|'))==5:
                modified_location=location.split('|')[-2]
            if modified_location==None:
                if len(location.split('|'))==6:
                    modified_location=location.split('|')[-2]
            else:
                if len(location.split('|'))==6:
                    modified_location=modified_location+", "+location.split('|')[-2]
            self.html_data[key]=modified_location

        return self.html_data
    def rule_no_34(self):
        """
        American airlines
        """
        for key in ['job_description']:
            data=self.html_data[key]
            data=re.sub('\s+',' ',str(data))
            soup=BeautifulSoup(str(data),"html.parser")
            for div in soup.findAll(['p']):
                if 'location'.lower() in div.getText().lower():
                    div.decompose()
            self.html_data[key]=str(soup)
        return self.html_data
    def rule_no_35(self):
        """
        korn Ferry
        """
        removed_elemnts=[]
        for key in ['job_description']:
            data=self.html_data[key]
            data=re.sub('\s+',' ',str(data))
            soup=BeautifulSoup(str(data),"html.parser")
            for div in soup.findAll(['p']):
                for item in ['Position','Organization','Location','Reporting Relationship','Direct reports','Website','Company','Direct Reports']:
                    if item in div.getText():
                        removed_elemnts.append(str(div))
                        div.decompose()
            for ele in soup.findAll():
                if fuzz.ratio(self.html_data.get('job_id'),ele.getText()) >85:
                    ele.decompose()
            for x in removed_elemnts:
                soup=str(soup)+str(x)
            self.html_data[key]=str(soup).replace('APPLY NOW','')
        return self.html_data
    def rule_no_36(self):
        """
        Timber,
        Williamson-Dickie Mfg Co
        """
        for key in ['job_location']:
            location=self.html_data[key]
            modified_location=None
            location=location.split('>')
            if len(location)>1 and len(location)>2:
                modified_location=location[2]
            else:
                modified_location=self.html_data[key]
            self.html_data[key]=modified_location

        return self.html_data
    def rule_no_37(self):
        """
        Avis Budget Froup
        """
        for key in ['job_location']:
            location=self.html_data[key]
            modified_location=None
            location=location.split('-')
            if len(location)>1 and len(location)>2:
                modified_location=' ,'.join(location[0:2])
            else:
                modified_location=location[0]
            self.html_data[key]=modified_location

        return self.html_data
    def rule_no_38(self):
        """
        Paytm
        """
        for key in ['job_description']:    
            html=self.html_data[key]
            soup=BeautifulSoup(html,"html.parser")
            for x in soup.find_all('div'):
                for a in ("Ø" ,'·'):
                    if a in x.getText() and len(x.findChildren())<6:
                        text=x.getText().strip().replace(a,'')
                        if len(text)!=0:
                            for y in x.findChildren():
                                y.decompose()
                            x.string="<li>"+text+"</li>"
                            x.name="ul" 
            self.html_data[key]=str(soup)
        return self.html_data 
    def rule_no_39(self):
        """
        Paytm
        """
        for key in ['job_description']:    
            html=self.html_data[key]
            soup=BeautifulSoup(html,"html.parser")
            for x in soup.find_all('div'):
                for a in ("•",):
                    if a in x.getText() and len(x.findChildren())<6:
                        text=x.getText().strip().replace(a,'')
                        if len(text)!=0:
                            for y in x.findChildren():
                                y.decompose()
                            x.string="<li>"+text+"</li>"
                            x.name="ul" 
            self.html_data[key]=str(soup)
        return self.html_data                    


class InstructionsForAll():
    def __init__(self,job):
        self.html_data=job
    def check_break_tags(self,object_list):
        for x in object_list:
            if x.name!='br':
                return False
        return True        
    def rule_for_all(self,html_tags=None,keywords=None,attrs=None,apply_link=None,ul_li_tags=None):
        """
        removing elements
        """
        removed_elemnts=[]
        for key_h in ['job_description','qualifications','job_roles_responsibilities']:
            data=self.html_data.get(key_h)
            soup=None
            if data!=None:
                data=re.sub('\s+',' ',str(data))
                soup=BeautifulSoup(str(data),"html.parser")
                if html_tags!=None and keywords!=None:
                    for tag in soup.findAll([html_tags.split(',')]):
                        for item in keywords.split(','):
                            if tag!=None and  item.lower() in tag.getText().lower():
                                if tag.parent!=None and len(tag.parent.getText().strip())<=150:
                                    tag.parent.decompose()
                                    removed_elemnts.append(str(tag))
                                else:
                                    if len(tag.getText())<=50:
                                        tag.decompose()
                                        removed_elemnts.append(str(tag))
                if attrs!=None:
                    for tag,attr in attrs.items():
                        if soup.find(tag,attr)!=None:
                            if attrs.get("append"):
                                removed_elemnts.append(deepcopy(str(soup.find(tag,attr))))
                            soup.find(tag,attr).decompose()
                if ul_li_tags!=None:
                    for x in soup.findAll(ul_li_tags['tags']):
                        text=x.getText()
                        if len(x.findChildren())==0 and  len(x.getText().strip())>0:
                            for key in ul_li_tags.get('li_keys'):
                                for y in text.split(key):
                                    if text.split(key).index(y)> ul_li_tags.get('index_remover'):
                                        new_string=new_string+"<ul><li>"+y+"</li></ul>"
                                    else:
                                        new_string=y
                            x.string=""
                            new_soup=BeautifulSoup(new_string,"html.parser")
                            x.insert(1,new_soup)
                        elif  len(x.findChildren())>0 and  len(x.getText().strip())>0:
                            for a in ul_li_tags.get('li_keys'):
                                if a in x.getText() and len(x.findChildren())<ul_li_tags.get('index_remover'):
                                    text=x.getText().strip().replace(a,'')
                                    if len(text)!=0:
                                        for y in x.findChildren():
                                            y.decompose()
                                        if text.strip()!='':    
                                            x.string="<li>"+text+"</li>"
                                        x.name="ul"
                    for x in soup.findAll(ul_li_tags['tags']):
                        text=x.getText()
                        for key in ul_li_tags.get('li_keys'):
                            if key in text and self.check_break_tags(x.findChildren()):
                                new_string=""
                                for text_str in text.split(key):
                                    if text_str.strip()!='':
                                        new_string=new_string+"<ul><li>"+text_str+"</li></ul>"
                                x.string=''    
                                for child_tag in x.findChildren():
                                    tag.decompose()
                                new_soup=BeautifulSoup(new_string,"html.parser")
                                x.insert(1,new_soup)            

                if soup!=None:                               
                    self.html_data[key_h]=str(soup)
        if apply_link!=None and self.html_data.get('job_id')!=None:
            if '?' in self.html_data.get('apply_link'):
                self.html_data['apply_link']=self.html_data.get('apply_link')+"&"+apply_link+"="+str(self.html_data.get('job_id'))
            else:
                self.html_data['apply_link']=self.html_data.get('apply_link')+"?"+apply_link+"="+str(self.html_data.get('job_id'))
        return self.html_data



# data=""""""
# job={'job_description':data}
# incobj=Instructions(1000,job)
# opr=open(r'D:\web.html','w')
# opr.write(incobj.rule_for_all(tags='tr,',keywords='Division:,Project Location(s):,Minimum Years Experience:,Travel Involved:,Job Type:,Job Classification:,Education:,Job Family:,Compensation:',attrs=None)['job_description'])
# opr.close()
