import re
def detect_experince(data):
    split_data=[x.lower().replace(',','').replace('.','').replace(':','') for x in data.split() if x.strip()!='']
    keywords=('years','year')
    notMatchedKeywords=('age','started','ended','salary','we have achieved four straight',
    'ranking','within the Vault Consulting','Some may think were old')
    index=list()
    replcers=(',','.',':')
    string=None
    
    for x in range(len(split_data)):
        for y in keywords:
            if y in split_data[x].strip():
                for z in split_data[x:x+20]:
                    if x not in index:
                        index.append(x)
                        break
    exp=None
    indexer=None
    print(index)
    count=0
    for  x in index:
        count+=1
        if count>10:
            break
        if indexer==None:
            indexer=7
        try:
            if x==1:
                string=" ".join(y for y in split_data[0:x+indexer:] if y!='')+" "
                enabled=True
                for y in notMatchedKeywords:
                    if y in string:
                        enabled=False                       
            if x>1:
                string=" ".join(y for y in split_data[x-indexer:x+indexer:] if y!='')+" "
                enabled=True
                for y in notMatchedKeywords:
                    if y in string:
                        enabled=False
                string=" ".join(y for y in split_data[x-indexer:x+1:] if y!='')+" "
                if len(string.strip().split())<3:
                    exp=None
                    indexer=indexer-1
                    index.append(x)
                    continue
            if enabled==True:
                expression=re.compile(r'\d+-\d+')
                search=re.search(expression,string)
                if search!=None:
                    exp=search.group()
                else:
                    expression=re.compile(r'\d+')
                    search=re.search(expression,string)
                    if search!=None:
                        exp=search.group()
                        if int(exp)>25:
                            exp=None
                            indexer=indexer-1
                            index.append(x)
                            continue
                        elif int(exp)<=2:
                            exp="0-"+str(exp)

        except :pass
    if exp==None:
        return None
    return str(exp)+" year(s)"                                    
def detect_experience_level(experience,data):
    detected_experience_level=None
    if experience==None:
        experience_level_items=({'Senior Level':('senior','manager','senior developer')},{'Entry Level':('fresher',)})
        NegtiveMatches=(' no ',' not ',' non '," don't "," aren't "," isn't " ," wasn't "," weren't "," haven't ","hasn't",
        "hadn't","doesn't","didn't","can't","couldn't","mustn't","needn't","won't","wouldn't","shan't","shouldn't",
        "oughtn't ")
        split_data=[x for x in str(data).split(',') if x!='' ]
        matched_list=list()
        for x  in range(len(split_data)):
            for  y in [item  for obj in experience_level_items for items in obj.values() for item in items]:
                if y in split_data[x]:
                    for not_item in NegtiveMatches:
                       if not_item not in split_data[x].split(y)[0][-20::]:
                           matched_list.append(y)
                           break
        for x in matched_list:
            for obj in experience_level_items:
                for key,values in obj.items():
                    if x in values:
                        detected_experience_level=key
                        break
        return    detected_experience_level
    else:
        numbers=[]
        for x in experience:
            if x.isdigit():
                numbers.append(int(x))
        if len(numbers)!=0:
            if max(numbers)>0 and max(numbers)<3:
                detected_experience_level='Entry level'
            elif  max(numbers)>=3 and max(numbers)<7:
                detected_experience_level='Mid Level'
            elif  max(numbers)>=7:
                detected_experience_level='Senior Level'
        return  detected_experience_level    