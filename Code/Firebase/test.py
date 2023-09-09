import pandas as pd
import requests 
import random
import io
import re
import json


namenode= 'https://project-dsci-551-default-rtdb.firebaseio.com/Namenode/'
struct='https://project-dsci-551-default-rtdb.firebaseio.com/structure/root/'
datanode='https://project-dsci-551-default-rtdb.firebaseio.com/Datanode/'
partition='https://project-dsci-551-default-rtdb.firebaseio.com/'

def mkdir(directory):
    chck_path='/'.join(directory.split('/')[:-1])
    name=directory.split('/')[-1]
    print(name)
    data_values='{"'+directory.split('/')[-1]+'":""}'
    path = namenode+name+'.json'
    print(str(path))
    lst_nd=int(list(requests.get('https://project-dsci-551-default-rtdb.firebaseio.com/Namenode/.json?orderBy="id"&print=pretty&limitToLast=1').json().values())[0]['id']) 
    requests.patch(namenode+name+'.json',data='{"id":'+str(lst_nd+1)+',"type":"DIRECTORY","path":"'+path+'"}').json()
    return "A New Folder '{}' has been created".format(name)

def ls(directory):
    data_val=requests.get(namenode+directory+'.json').json()
    return list(data_val.keys())


print(ls('hashtag'))
def cat(directory):

    val=requests.get(datanode+directory+'.json').json()
    return list(val.values())
#print(cat('Project_Dataset_copy'))

def getPartitionLoc(directory):
    val=requests.get(datanode+directory+'.json').json()
    val_namenode=requests.get(namenode+directory+'.json').json()
    id_value=val_namenode['id']
    x=list(val.keys())
    dict={"id_value":id_value,"parts":x}
    return dict
    
#print(getPartitionLoc('Project_Dataset_copy'))



def readPartitionLocations(directory,part_no):
    k=int(part_no)
    data_output=requests.get(datanode+directory+'/part'+str(k)+'.json').json()
    return data_output

#print(readPartitionLocations('Project_Dataset_copy',2))



def rm(directory):
    None


def put(filename,k):
    if filename.split('.')[-1]=='csv' or filename.split('.')[-1]=='json':
        file=filename.split('.')[0]
    df=pd.read_csv(filename)
    size=int(len(df)/k)
    # print(df)
    # print(size)
    col_list=df.columns
    for i in range(0,k):
        df1=df.iloc[(i)*size:(i+1)*size]
        list_of_jsons= df1.to_dict(orient='records')
        fnl_list=list_of_jsons

        #URL="https://project-dsci-551-default-rtdb.firebaseio.com/Namenode/.json"
        
        print(fnl_list)
        #Make a dict and directly pass as the data-->json
        data_values=fnl_list
        requests.put(url = 'https://project-dsci-551-default-rtdb.firebaseio.com/Datanode/'+file+'/part'+str(i+1)+'/.json', json = data_values)

    path_datanode=datanode+file+'.json'
    lst_nd=int(list(requests.get('https://project-dsci-551-default-rtdb.firebaseio.com/Namenode/.json?orderBy="id"&print=pretty&limitToLast=1').json().values())[0]['id']) 
    requests.patch(namenode+file+'.json',data='{"id":'+str(lst_nd+1)+',"type":"File","path":"'+path_datanode+'"}').json()
    return "A New Folder '{}' has been created".format(file)

