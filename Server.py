import json
import re
import socket
from pprint import pprint
from QQCONFIG import *


def login_check():
    s_login=socket(AF_INET,SOCK_DGRAM)
    for x in user_state.keys():
        s_login

user_info = {
    'xudashuai': {
        'password':'19980819',
        'friends':['xuxiaoshuai','xu','xiao']
    },
    'xuxiaoshuai':{
        'password':'19980818',
        'friends':['xudashuai']
    },
    'testtest':{
        'password':'111111',
        'friends':[]
    }
}
user_state = {'xudashuai': ('', '')}
wait_message = {}
s.bind(ADDR)

while True:
    rec, addr = s.recvfrom(1024)
    data = json.loads(rec.decode())
    pprint(data)
    response = {}
    if data['type'] is LOGIN:
        if data['username'] in user_info.keys():
            if user_info[data['username']]['password'] == data['password']:
                user_state[data['username']] = addr
                response['username']=data['username']
                response['type'] = LOGIN_SUCCESS
                response['friends']=user_info[data['username']]['friends']
                response['wait_message']=[]
                if data['username'] in wait_message.keys():
                    for message in wait_message[data['username']]:
                        response['wait_message'].append(message)
                s.sendto(json.dumps(response).encode(),addr)
                for user in user_state.keys():
                    if data['username'] in user_info[user]['friends']:
                        s.sendto(json.dumps(
                            {'username':data['username'],'type':ONLINE,'time':data['time']}).encode(),user_state[user])
                print(data['username'],' online')
                print(user_state)
            else:
                response['type'] = LOGIN_FAIL
                response['reason'] = 'wrong password'
                s.sendto(json.dumps(response).encode(),addr)
        else:
            response['type'] = LOGIN_FAIL
            response['reason'] = 'user not exist'
            s.sendto(json.dumps(response).encode(),addr)
    elif data['type'] is REGISTER:
        register_re = re.compile(r"[\w]{6,}")
        if register_re.fullmatch(data['username']):
            if register_re.fullmatch(data['password']):
                if data['username'] in user_info.keys():
                    response['type'] = REGISTER_FAIL
                    response['reason'] = 'username exist'
                    s.sendto(json.dumps(response).encode(),addr)
                else:
                    user={
                        'password':data['password'],
                        'friends':[]
                    }
                    response['username']=data['username']
                    user_info[data['username']]=user
                    user_state[data['username']] = addr
                    response['type'] = REGISTER_SUCCESS
                    response['friends']=user_info[data['username']]['friends']
                    response['wait_message']=[]
                    s.sendto(json.dumps(response).encode(),addr)
            else:
                response['type'] = REGISTER_FAIL
                response['reason'] = 'password illegal'
                s.sendto(json.dumps(response).encode(),addr)
        else:
            response['type'] = REGISTER_FAIL
            response['reason'] = 'username illegal'
            s.sendto(json.dumps(response).encode(),addr)
    elif data['type'] is MESSAGE:
        if data['send_to'] in user_state.keys():
            s.sendto(rec, user_state[data['send_to']])
        else:
            pprint('add to wait_message')
            if data['send_to'] in wait_message.keys():
                wait_message[data['send_to']].append(data)
            else:
                wait_message[data['send_to']] = [data]
            pprint(wait_message)
            response['type']=USER_OFFLINE
            response['send_to']=data['send_to']
    elif data['type'] is ONLINE:
        for user in user_state.keys():
            if data['username'] in user_info[user]['friends']:
                s.sendto(json.dumps(data).encode(),user_state[user])
    elif data['type'] is OFFLINE:
        if data['username'] in user_state.keys():
            user_state.pop(data['username'])
        for user in user_state.keys():
            if data['username'] in user_info[user]['friends']:
                s.sendto(json.dumps(data).encode(),user_state[user])
        print(data['username'],' offline')
        print(user_state)
    elif data['type'] is ADD_FRIEND:
        if data['add_id'] in user_info.keys():
            if data['add_id'] in user_state.keys():
                s.sendto(rec, user_state[data['add_id']])
                response['type']=ADD_WAIT
                s.sendto(json.dumps(response).encode(),addr)
            else:
                if data['add_id'] in wait_message.keys():
                    k=False
                    for x in wait_message[data['add_id']]:
                        if x['username'] == data['username']:
                            k=True
                            break
                    if k:
                        response['type']=ADD_FAIL
                        response['username']=data['add_id']
                        response['reason']='请不要重复发送请求'
                        s.sendto(json.dumps(response).encode(),addr)
                    else:
                        wait_message[data['add_id']].append(data)
                        response['type']=ADD_WAIT
                        s.sendto(json.dumps(response).encode(),addr)
                else:
                    wait_message[data['add_id']] = [data]
                    response['type']=ADD_WAIT
                    s.sendto(json.dumps(response).encode(),addr)
        else:
            response['type']=ADD_FAIL
            response['reason']='用户不存在'
            response['username']=data['add_id']
            s.sendto(json.dumps(response).encode(),addr)
    elif data['type'] is ADD_SUCCESS:
        user_info[data['username']]['friends'].append(data['add_id'])
        user_info[data['add_id']]['friends'].append(data['username'])
        if data['username'] in user_state.keys():
            s.sendto(rec, user_state[data['username']])
        else:
            if data['username'] in wait_message.keys():
                wait_message[data['username']].append(data)
            else:
                wait_message[data['username']] = [data]


