from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import requests
from .SQL_Commands_main import *
from .FireBase_functions import *


URL = "https://dsci551-project-51fcc-default-rtdb.firebaseio.com/"

color = {
    "Netflix":"#E50914" ,
    "Amazon_Prime":"#00A8E1",
    "Disney": "#113CCF"

}

structure = {
        "home":{
            # "name":"home",
            # "has_children":True,
            # "children":["folder1","folder2","file4"],
            # "folder1":{
            #     "name":"folder1",
            #     "has_children":True,
            #     "children":["file1","file2"],
            #     "file1":{ 
            #         "name":"file1",
            #         "has_children":False,
            #     },
            #     "file2":{
            #         "name":"file2",
            #         "has_children":False,
            #     }
            # },
            # "folder2":{
            #     "name":"folder2",
            #     "has_children":True,
            #     "children":["file3"],
            #     "file3":{
            #         "has_children":False,
            #     }
            # },
            # "file4":{
            #     "name":"file4",
            #     "has_children":False,
            # }
        }
    }
# home page.
def home(request):
    return render(request,'home.html')


#test firebase
def get_firebase_data(request,bounds):
    start,end = bounds.split(",")
    # data = requests.get('https://dsci551hw-427d5-default-rtdb.firebaseio.com/load-data.json').json()
    data=requests.get("https://dsci-551-project-b4be8-default-rtdb.firebaseio.com/Datanode.json").json()
    return JsonResponse(data,safe =False)

#select a platform

def select_platform(request,platform):
    type = platform
    return render(request,'select_platform.html',{"broadcast_type" : type})


#results and filters

def get_results(request,platform,service):

    data = requests.get(URL+platform+"/"+service+".json").json()
    # print(data[0]["Description"])
    for i in range(len(data)):
        if "Description" in data[i]:
            data[i]['Description'] = data[i]['Description'][:100]+"..."
        data[i]['Genres'] = data[i]['Genres'][1:-1]
        data[i]['Genres'] = data[i]['Genres'].replace("'","")
    return render(request,'display.html',{"platform":platform,"service":service,"data":data, 'distribution_url': "/media/"+service+"/Distribution.jpg",'runtime_url': "/media/"+service+"/Runtime.jpg",'top_10_url': "/media/"+service+"/top10.jpg","table_color":color[service]})


def filter_rating(request,platform,service,start,end):
    data = list(requests.get(URL+platform+'/'+service+'.json?orderBy="Imdb_Score"&startAt='+str(start)+'&endAt='+str(end)+'').json().values())
    for i in range(len(data)):
        if "Description" in data[i]:
            data[i]['Description'] = data[i]['Description'][:100]+"..."
        data[i]['Genres'] = data[i]['Genres'][1:-1]
        data[i]['Genres'] = data[i]['Genres'].replace("'","")
    return render(request,'display.html',{"platform":platform,"service":service,"data":data, 'distribution_url': "/media/"+service+"/Distribution.jpg",'runtime_url': "/media/"+service+"/Runtime.jpg",'top_10_url': "/media/"+service+"/top10.jpg","table_color":color[service]})

def filter_genre(request,platform,service,genre):
    data = requests.get(URL+platform+"/"+service+".json").json()
    result = []
    for i in range(len(data)):
        if genre in data[i]['Genres']:
            if "Description" in data[i]:
                data[i]['Description'] = data[i]['Description'][:100]+"..."
            data[i]['Genres'] = data[i]['Genres'][1:-1]
            data[i]['Genres'] = data[i]['Genres'].replace("'","")
            result.append(data[i])
    return render(request,'display.html',{"platform":platform,"service":service,"data":result, 'distribution_url': "/media/"+service+"/Distribution.jpg",'runtime_url': "/media/"+service+"/Runtime.jpg",'top_10_url': "/media/"+service+"/top10.jpg","table_color":color[service]})

def filter_year(request,platform,service,year):
    if year == 1980:
        start = 0
        end = 1989
    else: 
        start = year
        end = start +9
    
    data = list(requests.get(URL+platform+'/'+service+'.json?orderBy="Release_year"&startAt='+str(start)+'&endAt='+str(end)+'').json().values())
    # print(data)
    for i in range(len(data)):
        if "Description" in data[i]:
            data[i]['Description'] = data[i]['Description'][:100]+"..."
        data[i]['Genres'] = data[i]['Genres'][1:-1]
        data[i]['Genres'] = data[i]['Genres'].replace("'","")
    return render(request,'display.html',{"platform":platform,"service":service,"data":data, 'distribution_url': "/media/"+service+"/Distribution.jpg",'runtime_url': "/media/"+service+"/Runtime.jpg",'top_10_url': "/media/"+service+"/top10.jpg","table_color":color[service]})


def functions(request):
    structure = {
        "home":{
            "folder1":["file1","file2"],
            "folder2":["file3"],
            "file4":{}
        }
    }
    test= list(str(structure))
    ans= []
    for i in test:
        if i in ["[","]","{","}",","]:
            ans.append(i+"\n")
        else:
            ans.append(i)
    ans = "".join(ans)
    return render(request,"functions.html", {"files":structure,"test":ans})

def get_file_structure(request):
    data = requests.get("https://project-dsci-551-default-rtdb.firebaseio.com/Namenode.json").json()
    if len(data.keys())>1:
        result = {
            "has_children" :True,
            "children":list(data.keys()),
        }
        for i in list(data.keys()):
            if "id" in data[i]:
                result[i] = {
                    "has_children":False
                }
            else:
                result[i] = {
                    "has_children":True,
                    "children":list(data[i].keys()),
                }
                for j in list(data[i].keys()):
                    result[i][j] = {
                        "has_children":False
                    }
    
    structure = result
    # if len(result)>1:
    #     structure["home"]["has_children"]=True
    return JsonResponse(result)


def run_command(request,db,com,args):
    args = args.split(",")
    if len(args)==1:
        args = args[0]
    print(args)
    sql_command = {
        "mkdir":mkdir,
        "ls":ls,
        "put":put,
        "cat":cat,
        "getPartition":getPartitionloc,
        "readPartition":readPartition,
        "rm":rm,
        "id":id,
        "getname":getname,
        "for_folder":for_folder,
        "struct":struct
    }
    firebase_command = {
        "mkdir":fb_mkdir,
        "ls":fb_ls,
        "put":fb_put,
        "cat":fb_cat,
        "getPartitionLocations":fb_getPartitionLoc,
        "readPartitionLocations":fb_readPartitionLocations,
        "rm":fb_rm,
        # "id":fb_id,
        # "getname":fb_getname,
        # "for_folder":fb_for_folder,
        # "struct":fb_struct
    }
    if db=="sql":
        command_to_run= sql_command[com]
    else:
        command_to_run = firebase_command[com]

    output = command_to_run(args)
    print(output)
    if com == "mkdir":
        path = args.split(".")
        if len(path)==2:
            structure[path[0]]["has_children"]=True
            if "children" in structure[path[0]]:
                structure[path[0]]["children"].append(path[1])

            else:
                structure[path[0]]["children"] = []
            structure[path[0]][path[1]] = {
                "has_children": False,
            }
        if len(path)==3:
            structure[path[0]]["has_children"]==True
            if "children" in structure[path[0]]:
                structure[path[0]]["children"].append(path[1])
            if path[1] in structure[path[0]]:
                structure[path[0]][path[1]]["has_children"]=True
            if "children" in structure[path[0]][path[1]]:
                structure[path[0]][path[1]]["children"].append(path[2])
            else:
                structure[path[0]][path[1]]["children"] = [path[2]]
            structure[path[0]][path[1]][path[2]] = {
                "has_children":False
            }
    return JsonResponse({"structure":structure,"output":output})
            

