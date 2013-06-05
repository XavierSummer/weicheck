# -*- coding: utf-8 -*-
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt  
from django.utils.encoding import smart_str, smart_unicode
from maingame.models import Story, Items, Users,Users_Current
import datetime
import hashlib
import urllib2
import json
import xml.etree.ElementTree as ET  
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
TOKEN = "Your TOKEN"
Welcome="This is Welcome"
INPUT_UNAVAILABLE="骚年，你就按选项来输入呗"
ERROR_UNSTART="未开始游戏"

def current_datetime(request):
    now = datetime.datetime.now()
    t = get_template('newtemp.html')
#    pub=Publisher.objects.get(name__contains='123')
    html = t.render(Context({'current_date': 's'}))
    return HttpResponse(html)


def handleRequest(request):
    if request.method == 'GET':
        response = HttpResponse(checkSignature(request),content_type="text/plain")
        return response
    elif request.method == 'POST':
        response = HttpResponse(responseMsg(request),content_type="application/xml")
        return response
    else:
        return None

def checkSignature(request):
    global TOKEN
    signature = request.GET.get("signature", None)
    timestamp = request.GET.get("timestamp", None)
    nonce = request.GET.get("nonce", None)
    echoStr = request.GET.get("echostr",None)
    token = TOKEN
    tmpList = [token,timestamp,nonce]
    tmpList.sort()
    tmpstr = "%s%s%s" % tuple(tmpList)
    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    if tmpstr == signature:
        return echoStr
    else:
        return None

def responseMsg(request):
    global Welcome
    relpyType='text'
    rawStr = smart_str(request.raw_post_data)  
    msg = paraseMsgXml(ET.fromstring(rawStr))
    usr=msg.get('FromUserName')
    if is_subscribe(msg)==True: #若为订阅事件
        return replyXml(msg,getWelcome(),relpyType)
        
    if is_text(msg)==True:
        usrStr=msg.get('Content')
        content = process(usr,usrStr)
        return replyXml(msg, content,relpyType)

def process(usr,msg):
    dic=['1','2','3','4','5','6']
    if msg in dic:
        pass
    else:
        return INPUT_UNAVAILABLE
    checkusr_cur=Users_Current.objects.filter(usrname=usr)
    checkusr=Users.objects.filter(usrname=usr)
    checkstory=Story.objects.filter(storyId=msg)
    if len(checkusr_cur)==0:      #用户未参与过id=msg 的活动;发送剧本叙述 以及第一次选择
        if len(checkstory)==0:      #输入不可用
            remsg=getWelcome()
            return remsg
        else:
            startItem=checkstory[0].startItem
            crusr=Users.objects.create(usrname=usr,storyId_id=msg,current=0,currentId=startItem,history='0',isover=2)
            usr_cur=Users_Current.objects.create(usrname=usr,storyId_id=msg,current=0,currentId=startItem,isover=0,location=0,finished_story='')
            crd=checkusr[0].currentId
            allop=Items.objects.filter(itemId=checkusr[0].currentId)
            remsg='你将要进入剧本：  '+unicode(checkstory[0].topic)+"""
"""+"""1.确认进入
"""+'2.返回选择'
            return remsg
    
    elif checkusr_cur[0].location==0:
        story=Story.objects.filter(storyId=checkusr_cur[0].storyId_id)
        dic=['1','2']
        if msg in dic:
            if msg=='1':
                checkusr_cur[0].location=1
                checkusr_cur[0].save()
                allop=Items.objects.filter(itemId=checkusr[0].currentId)
                remsg='当前剧本：  '+unicode(story[0].topic)+'  '+unicode(story[0].message)+unicode(allop[0].message)
                for x in range(1,6):
                    usrOp='op'+unicode(x)
                    op=getattr(allop[0],unicode(usrOp))
                    if op!='':
                        remsg=unicode(remsg)+"""
"""+unicode(op)
                
                return remsg
            else:
                checkusr=Users.objects.filter(usrname=usr,storyId_id=checkusr_cur[0].storyId_id)
#                checkusr[0].delete()
                checkusr_cur[0].location=-1
                checkusr_cur[0].save()
                return getWelcome()
        else:
            remsg='你将要进入剧本：  '+unicode(story[0].topic)+"""
"""+"""1.确认进入
"""+'2.返回选择'
            return remsg
    elif checkusr_cur[0].location==-1:
        if len(checkstory)==0:      #输入不可用
            remsg=getWelcome()
            return remsg
        else:
            remsg='你将要进入剧本：  '+unicode(checkstory[0].topic)+"""
    """+"""1.确认进入
    """+'2.返回选择'
            checkusr=Users.objects.filter(usrname=usr,storyId_id=msg)
            if len(checkusr)==0:
                checkusr=Users.objects.filter(usrname=usr,storyId_id=msg)
                if len(checkusr)==0:
                    crusr=Users.objects.create(usrname=usr,storyId_id=msg,current=0,currentId=checkstory[0].startItem,history='0',isover=2)
                else:
                    Users.objects.filter(usrname=usr,storyId_id=checkusr_cur[0].storyId_id).update(storyId=msg)
                checkusr_cur[0].storyId_id=msg
                checkusr_cur[0].location=0
                checkusr_cur[0].save()
                return remsg
            elif checkusr[0].isover<0:
                return '该游戏已经完成，请重新选择'+"""
"""+getWelcome()
            else:
                checkusr_cur[0].storyId_id=msg
                checkusr_cur[0].location=0
                checkusr_cur[0].save()
                return remsg
                
                
    #            checkusr_cur[0].storyId_id=msg
    #            checkusr[0].storyId_id=msg
    #            checkusr_cur[0].location=0
    #            checkusr_cur[0].save()
    #            checkusr[0].save()


    else:
        checkusr=Users.objects.filter(usrname=usr,storyId_id=checkusr_cur[0].storyId_id)
        cks=Story.objects.filter(storyId=checkusr_cur[0].storyId_id)
        usrOp='op'+unicode(msg)+'_next'
        currentid=checkusr[0].currentId
        item=Items.objects.filter(itemId=currentid)
        if available_input(msg,'item',currentid):
            next_id=getattr(item[0],unicode(usrOp))
            next_item=Items.objects.filter(itemId=next_id)
            if next_item[0].isend==1:
                Users.objects.filter(usrname=usr,storyId_id=checkusr_cur[0].storyId_id).update(current=0)
                
                Users.objects.filter(usrname=usr,storyId_id=checkusr_cur[0].storyId_id).update(currentId=cks[0].startItem)
                Users.objects.filter(usrname=usr,storyId_id=checkusr_cur[0].storyId_id).update(isover=checkusr[0].isover-1)
#                Users.objects.filter(usrname=usr,storyId_id=checkusr_cur[0].storyId_id).update(isover=checkusr[0].isover-1)
                checkusr_cur[0].location=-1
                checkusr_cur[0].save()
#                checkusr[0].delete()
                return unicode(next_item[0].message)+"""
"""+'游戏结束! '+"""=============
"""+getWelcome()
            else:
                Users.objects.filter(usrname=usr,storyId_id=checkusr_cur[0].storyId_id).update(current=checkusr[0].current+1)
                Users.objects.filter(usrname=usr,storyId_id=checkusr_cur[0].storyId_id).update(currentId=next_id)
                remsg=next_item[0].topic+next_item[0].message
                
                for x in range(1,6):
                    usrOp='op'+unicode(x)
                    op=getattr(next_item[0],unicode(usrOp))
                    if op!='':
                        remsg=unicode(remsg)+"""
"""+unicode(op)
                
                return remsg
        else:
            remsg=getItem(checkusr[0].currentId)
            return remsg
        
def available_input(instr,type,id):
    count=0
    if instr=='ck':
        return True
    elif type=='item':
        item=Items.objects.filter(itemId=id)
        for x in range(1,7):
            usrOp='op'+unicode(x)
            op=getattr(item[0],unicode(usrOp))
            if op!='':
                count=count+1
        if int(count)<int(instr):
            return False
        else:
            return True
    elif type=='story':
        story=Story.objects.filter(storyId=instr)
        if len(story)==0:
            return False
        else:
            return True

def getWelcome():
    count=Story.objects.count()
    checkstory=Story.objects.order_by('storyId')
    remsg=unicode('欢迎进入，你有3次机会完成游戏，若网络延迟，请勿重复输入。请选择剧本：')
    for x in range(0,count):
        remsg+="""
"""+'【'+unicode(checkstory[x].storyId)+'】'+(unicode(checkstory[x].topic))
    return remsg

def getItem(id):
    allop=Items.objects.filter(itemId=id)
    remsg=unicode('输入无效,请重新输入')
    for x in range(1,6):
        usrOp='op'+unicode(x)
        op=getattr(allop[0],unicode(usrOp))
        if op!='':
            remsg=remsg+"""
        """+unicode(op)
    return remsg
def is_subscribe(msg):
    return msg['MsgType'] == 'event' and msg['Event'] == 'subscribe'

def is_text(msg):
    return msg['MsgType'] == 'text'



def paraseMsgXml(rootElem):  
    msg = {}  
    if rootElem.tag == 'xml':
        for child in rootElem:  
            msg[child.tag] = smart_str(child.text)  
    return msg  


def replyXml(recvmsg, replyContent,relpyType):
    textTpl = """ <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName> 
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[%s]]></MsgType>
                <Content><![CDATA[%s]]></Content>
                <FuncFlag>0</FuncFlag>
                </xml>
                """
    echostr = textTpl % (recvmsg['FromUserName'], recvmsg['ToUserName'], recvmsg['CreateTime'], relpyType, replyContent)
    return echostr