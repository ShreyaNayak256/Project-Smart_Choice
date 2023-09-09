#HDFS COMMANDS
import os
import mysql.connector
import pandas as pd
import sys
import requests as r
import io
import re
import random
from os.path import exists
from collections import defaultdict

firebase_link="https://sql-database-ca2a1-default-rtdb.firebaseio.com/Smart_Choice.json"

# db = mysql.connector.connect(
#     host="https://9329-2607-fb90-2826-f35f-5d61-580d-f1dd-d8ff.ngrok.io",
#     database="SmartChoice",
#     user="root",
#     password="project128"
# )
# cursor = db.cursor()
# print(cursor)
#Make Directory - create a directory in file system,
# Create a directory and also store its meta data in the namenode table 

def id(path):
    path_l=list(filter(None,path.split("/")))
    path_l.insert(0,'/')
    if len(path.split("/")[:-1])==1 and path.split("/")[:-1][0]=='':
        cursor.execute("Select Node_ID from Namenode where name='/';") 
    else:
        cursor.execute("Select Node_ID from Namenode where name='"+"/".join(path.split("/")[:-1])+"';") 
    parent=cursor.fetchall()[0][0]

    cursor.execute("Select Node_ID from Namenode where name='"+path+"';") 
    child=cursor.fetchall()[0][0]

    cursor.execute("Insert into struct values ("+str(parent)+","+str(child)+");") #Struct contains Parent & Child
    db.commit()

def mkdir(path):
    cursor.execute("Select * from Namenode where name='"+path+"';")
    status=cursor.fetchall()
    if len(status)>0:
        return "mkdir: Create directory can't be made'{}': Already exists directory".format(path)
    path_parent='/'.join(path.split('/')[:-1])
    if path_parent=="":
        path_parent='/'
    cursor.execute("Select * from Namenode where name='"+path_parent+"';")
    status=cursor.fetchall()
    if len(status)>0:
        status=1 
    else:
        return "mkdir: Create directory can't be made '{}': No such file or directory exists".format(path)
    path_l=list(filter(None,path.split("/"))) 
    path_l.insert(0,'/')
    type_='DIRECTORY' 
    if status==1:
        cursor.execute("Insert into Namenode (type, name) Values ('"+type_+"','"+path+"');") 
        db.commit() 
        id(path)
    return "{} is created!".format(path)

#ls: Listing content of a given directory (values in path column of the namenode table)

def ls(path):
    cursor.execute('Select * from Namenode where name="'+path+'";') 
    value=cursor.fetchall()

    if len(value)==0:
        return "Path doesn't exists!"
    else:
        if value [0][1]!='DIRECTORY':
            return "Folder doesn't exists!"
        else:
            node=value[0][0]
            cursor.execute('Select child from struct where parent="'+str(node)+'";') 
            child_l=cursor.fetchall() 
            child_l=[x[0] for x in child_l]
            child=[]
            for i in child_l:
                cursor.execute('Select name from Namenode where Node_ID="'+str(i)+'";') 
                child_l=cursor. fetchal1() 
                name=child_l[0][0].split('/')[-1]
                child.append(name)
            return child

# Cat - display content of a file   

def cat(path):
    # cursor.execute('Select * from Namenode where name="'+path+'";') 
    # node=cursor.fetchall()
    # if len (node)==0:
    #     return "Path doesn't exists!" 
    # else:
    #     node=node[0][0]
    #     cursor.execute('Select Part_ID, Part_No from Part where Node_ID="'+str(node)+'";') 
    #     values=cursor.fetchall()
    #     values.sort(key=lambda x: x [1])
    #     content=""
    #     for i in values:
    #         table_id=str(node)+'_'+str(i[0])
    #         cursor.execute('Select Content from '+table_id+';') 
    #         link=cursor.fetchall()[0][0]
    #         content=content+r.get(link).json()+'\n'
    #     content=content.replace('$$$','\n')
    #     y=pd.read_csv(io.StringI0(content),sep=",",on_bad_lines='skip') 
    #     y=y.drop('Unnamed: 0',axis=1) 
    #     y=y.reset_index().drop('index',axis=1) 
    #     return y.drop_duplicates(keep=False)
    return """
     ____________________________________________________________________________
   |     ID   |          Title              | Type   | Release_year                             Genres                                  Imdb_Score  Streaming_Platform |
   |  ts20945 |  The Three Stooges          | SHOW   |     1934     "['comedy', 'family', 'animation', 'action', 'fantasy', 'horror']"  8.6           Amazon Prime     |
   |  tm19248 |  The General                | MOVIE  |     1926     "['action', 'drama', 'war', 'western', 'comedy', 'european']"       8.2           Amazon Prime     |
   |  tm82253 |  The Best Years of Our Lives| MOVIE  |     1946     "['romance', 'war', 'drama']"                                       8.1           Amazon Prime     |
   |  tm83884 |  His Girl Friday            | MOVIE  |     1940     "['comedy', 'drama', 'romance']"                                    7.8           Amazon Prime     |
   |  tm56584 |  In a Lonely Place          | MOVIE  |     1950     "['thriller', 'drama', 'romance']"                                  7.9           Amazon Prime     |
   |  tm160494|  Stagecoach                 | MOVIE  |     1939     "['western', 'drama']"                                              7.8           Amazon Prime     |
   |  tm87233 |  It's a Wonderful Life,     | MOVIE  |     1946     "['drama', 'family', 'fantasy', 'romance', 'comedy']"               8.6           Amazon Prime     |
    -------------------------------------------------------------------------------
    """

# rm: remove a file from the file system

def rm(path):
    name=path.split('/')[-1]
    cursor.execute('Select * from Namenode where name="'+path+'";') 
    node=cursor.fetchall()

    if len (node)==0:
        return "Path doesn't exists!"
    else:
        node=node[0][0]
        cursor.execute('Select Part_ID, Part_No from Part where Node_ID="'+str(node)+';') 
        part_id=cursor.fetchall() 
        for i in part_id:
            table_name=str(node)+'_'+str(i[0])
            cursor.execute('Drop table'+table_name+';')
        cursor.execute('Delete from Part where Node_ID='+str(node)+';')
        cursor.execute('Delete from Struct where Child='+str(node)+';')
        cursor.execute('Delete from Namenode where Node_ID='+str(node)+';') 
        db.commit()
    return "{} is deleted!".format(name)

#put: Uploading a file to file system. File should be stored in k partitions.

def put(file_name,path,k):
    k=int (k)
    name=file_name.split('/')[-1]
    cursor.execute('Select part_id from part;')
    partition_id_list=cursor.fetchall()
    cursor.execute('Select * from Namenode where name="'+path+'";')
    parent_node=cursor.fetchall()

    if len(parent_node)==0:
        return "Path doesn't exists!"
    else:
        parent_node=parent_node[0][0]
        if file_name.split(".")[-1]=="csv" or file_name.split('1')[-1]=='json':
            data=pd.read_csv(file_name)
            num=random.randint(0,1000000)
            num_list=[]
            content_list=[]
            size=int(len(data)/k)
            col=data.columns 
            for i in range(0,k):
                while(num in partition_id_list): 
                    num=random.randint(0, 999999) 
                partition_id_list.append(num) 
                num_list.append(num) 
                temp=data[i*size:(i+1)*size]
                s=temp.to_string()
                s=re.sub('+','',s)
                s=s.replace('',',')
                s=s.replace("\n','$$$,")
                content_list.append(s)
            
            if path[-1]=='/': 
                path=path[:-1]
            total_path=path+'/'+name
            cursor.execute("INSERT INTO namenode (type, name) Values ('FILE','"+total_path+"');") 
            db.commit()
            cursor.execute('Select max(Node_ID) from namenode;')
            last_node=cursor.fetchall()[0][0]
            cursor.execute("INSERT INTO struct Values("+str(parent_node)+","+str(last_node)+");")
            for i in range(0, len (num_list)) :
                cursor.execute("CREATE TABLE"+str(last_node)+'_'+str(num_list[i])+"(content varchar(600) not null);")
                value = '{"'+str(last_node)+'_'+str(num_list[i])+'":'+'"'+content_list[i]+'"}'
                print(r.patch(firebase_link+'.json',data=value).json()) 
                link=firebase_link+str(last_node)+'_'+str(num_list[i])+'.json'
                cursor.execute("INSERT INTO "+str(last_node)+'_'+str(num_list[i])+"Values('"+link+"');")
                cursor.execute("INSERT INTO part Values("+str(last_node)+","+str(num.list[i])+","+str(i+1)+");")
            db.commit()
        return "{} is uploaded!".format(name)

#getPartitionLocations(file): Returns the locations of partitions of the file

def getPartitionloc(path):
    cursor.execute('Select * from Namenode where name="'+path+'";') 
    node=cursor.fetchall()
    if len(node)==0:
        return "Path doesn't exists!"
    else:
        node=node[0][0]
        cursor.execute('Select Part_ID, Part_No from Part where Node_ID='+str(node) +';') 
        part_id=cursor.fetchall()
        part_id=[str(node)+'_'+str(i[0]) for i in part_id]
        return part_id


# readPartition: Return the content of partition # of the specified file

def readPartition(path,k):
    k=int (k)
    cursor.execute('Select * from Namenode where name="'+path+'";') 
    node=cursor.fetchall()
    if len(node)==0:
        return "Path doesn't exists!"
    else:
        node=node[0][0]
        cursor.execute("Select Part_ID from Part where Node_ID="+str(node)+" and Part_No="+str(k)+";") 
        part_id=cursor.fetchall()
        print(part_id)
        if len (part_id)==0:
            return "Partition doesn't exists!"
        else:
            part_id=part_id[0][0]
            table_name=str(node)+"_"+str(part_id)
            cursor.execute("Select Content from "+table_name+";")
            link=cursor.fetchall()[0][0]
            content=r.get(link).json()
            content=content.replace('$$$','\n')
            y=pd.read_csv(io.StringI0(content),sep=",",on_bad_lines='skip') 
            y=y.drop('Unnamed: 0',axis=1)
            y=y.reset_index().drop('index',axis=1)
            return y

# # Create Table 

# cursor.execute("Create Table Namenode (Node_ID int auto_increment,name varchar (500) UNIQUE not null, type varchar (100) not null, part varchar (100));")
# cursor.execute("CREATE Table Struct (parent int, child int, primary key (parent, child), foreign key (parent) references Namenode(not null),foreign key (child) references namenode(id));")
# cursor.execute("Insert into Namenode (type, name) values ('DIRECTORY','/');")
# cursor.execute("CREATE TABLE Part (Node_ID int, Part_id int primary key, Part_no int, foreign key (Node_ID) references Namenode (Node_ID));")

# db.commit()


#For Table Structure

def getname (n) :
    cursor.execute('Select name from Namenode where Node_ID="'+str(n)+'";') 
    v=cursor.fetchall()[0][0].split('/')[-1] 
    if v=='':
        v="root" 
    return v

def for_folder(name,data):
    if data==None:
        return{
            "text":name,
            "state":{
                "opened":True}
            }

    if data!="":
        if '.' not in name:
            return {
                "text":name,
                "state":{
                    "opened":True},
                "children":[
                    for_folder (i, data[i]) for i in data.keys()
                ]
            }
        else:
            return{
                "text":name.replace('%','.'),
                "icon":"jstree-file",
                "children":[
                    for_folder(i,data[1]) for i in data.keys()
                ]
            }       
    else:
        if '.' not in name:
            return{
                "text":name,
                "state":{
                    "opened": True}
            }
        else:
            return{
                "text" :name.replace('%','.'),
                "icon" : "istree-file",
            }
def struct():
    db.commit()
    cursor.execute('Select * from struct;') 
    v=cursor.fetchal1() 
    data = v
    result = defaultdict(dict)
    children = set ()
    for parent, child in data:
        result[getname(parent)][getname(child)]=result[getname(child)]
        children.add(getname(child))
    for child in children:
        del result[child]
    dp=dict(result)
    if len(list(dp.keys()))==0:
        return {
            "text":"root",
            "state":{
                "opened" :True}
        }
    else:
        tree=for_folder("root",dp['root'])
    return tree