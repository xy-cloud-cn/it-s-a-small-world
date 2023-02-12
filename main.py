# -*- coding: utf-8 -*-
'''
@Author   : xy_cloud
@IDE      : PyCharm
@Project  : Python Project
@File     : main.py
@Time     : 2023/2/11 20:58
'''
import copy
import os
import shutil
import signal
import time
from tkinter import messagebox
import yaml, subprocess, threading
from send import *
import csv
def ping_127():
    try:
        requests.get('http://127.0.0.1:5700')
    except:
        return False
    else:
        return True


def set_uin(uin):
    file_name = "./config.yml"
    with open(file_name, encoding='utf-8') as f:
        doc = yaml.safe_load(f)
    doc['account']['uin'] = int(uin)
    with open(file_name, 'w', encoding='utf-8') as f:
        yaml.safe_dump(doc, f, default_flow_style=False)


def open_gocq():
    global pcs
    pcs=subprocess.Popen(cq_file, shell=True)


def info(msg):
    messagebox.showinfo(title="提示", message=msg)

global pcs
if not (os.path.exists('go-cqhttp.exe') or os.path.exists('go-cqhttp')):
    print('\033[31m[ERROR]请在github上下载最新版的go-cqhttp(https://github.com/Mrs4s/go-cqhttp/releases/latest)\033[0m')
    print('\033[31m[ERROR]如果你已经下载了go-cqhttp,请将它重命名为go-cqhttp.exe(Linux下没有.exe),并且放到这个文件夹下\033[0m')
    print('\033[31m[ERROR]下载教程(仅供参考):苹果电脑下载darwin（此程序暂未支持苹果系统），linux下载linux，windows下载windows，请自行查询处理器架构，如amd,arm等\033[0m')
    exit(0)
cq_file=''
if os.path.exists('go-cqhttp.exe'):
    cq_file='go-cqhttp.exe'
elif os.path.exists('go-cqhttp.exe'):
    cq_file = 'go-cqhttp'
if not os.path.exists('config.yml'):
    print('未检测到config.yml,请重新clone项目!')
    exit(0)
if os.path.exists('qrcode.png'):
    os.remove('qrcode.png')
if os.path.exists('device.json'):
    os.remove('device.json')
if os.path.exists('session.token'):
    os.remove('session.token')
if os.path.exists('data'):
    shutil.rmtree('data')
if os.path.exists('logs'):
    shutil.rmtree('logs')
qq = input('请输入你的qq号:')
set_uin(qq)
t = threading.Thread(target=open_gocq)
t.start()
while not ping_127():
    pass
group_list = get_group_list()['data']
for i in range(len(group_list)):
    group_list[i] = [group_list[i]['group_id'], group_list[i]['group_name']]

for i in range(len(group_list)):
    tmp = get_group_member_list(group_list[i][0])['data']
    group_list[i].append([])
    for j in range(len(tmp)):
        group_list[i][2].append([tmp[j]['user_id'], tmp[j]['nickname'], tmp[j]['card']])
member_dic={}
for i in group_list:
    for j in i[2]:
        if not (j[0],j[1]) in member_dic.keys():
            member_dic[(j[0],j[1])]=[]
        member_dic[(j[0],j[1])].append([i[0],i[1],j[2]])
member_list=list(member_dic.items())
member_list.sort(reverse=True,key=lambda x:len(x[1]))
for i in range(len(member_list)):
    member_list[i][1].sort(key=lambda x:x[0])
header=copy.deepcopy(member_list[0][1])
gid_list=[]
for i in range(len(header)):
    gid_list.append(header[i][0])
    header[i]=f'{header[i][0]}-{header[i][1]}'
with open(qq+'的qq世界.csv','w',encoding='utf-8-sig') as f:
    writer=csv.writer(f)
    writer.writerow(['qq号','昵称']+header)
    for i in member_list:
        tmp2=['']*len(gid_list)
        for j in i[1]:
            for k in range(len(gid_list)):
                if j[0]==gid_list[k]:
                    tmp2[k] = '√'
                    break
        writer.writerow([i[0][0],i[0][1]]+tmp2)

print('运行已结束，5秒后自动退出')
time.sleep(5)
os.kill(0, signal.CTRL_C_EVENT)
