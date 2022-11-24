'''
File: main.py
Author: github.com/HydroGest
Description: See who are peeping screens.
'''

from flask import Flask, render_template, request, send_from_directory
import os,time,json
app = Flask(__name__)

def SearchObject(groupId,info):
    fileName='./data/'+groupId+'.json'
    if os.path.isfile(fileName)==False:
        createdTime= int(time.time())
        with open(fileName,"w",encoding="utf-8") as f:
            f.write('{"createdTime":'+str(createdTime)+',"peeperList":[]}')
    fileContents=''
    with open(fileName,'r') as f:
        fileContents=fileContents+f.read()
    groupDict = json.loads(fileContents)
    if int(time.time())-int(groupDict['createdTime'])>300:
        createdTime=time.time()
        groupDict={
            "createdTime":createdTime,
            "peeperList":[]
        }
    if (info in groupDict['peeperList'])==False:
        groupDict['peeperList'].append(info)
    with open(fileName,"w",encoding="utf-8") as f:
        f.write(json.dumps(groupDict))
    return {
        'groupId': groupId,
        'createdTime': groupDict['createdTime'],
        'peeperList': groupDict['peeperList']
    }

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/search')
def search():
    #groupId = request.form['GroupId']
    groupId = request.args.get('GroupId', '')
    ip= request.remote_addr
    userAgent = request.headers.get("User-Agent")
    groupInfo = SearchObject(groupId,{
        'ip':ip,
        'userAgent': userAgent
    })
    return render_template(
        'group.html',
        currentTime=time.time(),
        GroupId=groupId,
        createdTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(groupInfo['createdTime'])),
        peeperList=groupInfo['peeperList']
    )

@app.route('/api/search/')
def api():
    groupId = request.form('GroupId', '')
    ip = request.remote_addr
    userAgent = request.headers.get("User-Agent")
    groupInfo = SearchObject(groupId,{
        'ip':ip,
        'userAgent': userAgent
    })
    return groupInfo

@app.route('/api/getimg/<groupId>/<string>/icon.jpg')
def imgget(groupId,string):
    ip = request.remote_addr
    userAgent = request.headers.get("User-Agent")
    groupInfo = SearchObject(groupId,{
        'ip':ip,
        'userAgent': userAgent
    })
    return send_from_directory('','icon128.jpg')
