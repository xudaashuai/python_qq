import json
import threading
import time
from pprint import pprint
from socket import *
from tkinter import *
from tkinter import messagebox
from FriendUI import FriendUI
from QQCONFIG import *


def login(username, password):
    if register_re.fullmatch(username):
        if register_re.fullmatch(password):
            mes = dict()
            mes['type'] = LOGIN
            mes['username'] = username
            mes['password'] = password
            mes['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            s.sendto(json.dumps(mes).encode('utf-8'), ADDR)
            rec, addr = s.recvfrom(1024)
            data = json.loads(rec.decode('utf-8'))
            if data['type'] is LOGIN_FAIL:
                password_entry.delete(0, END)
                messagebox.showinfo(message='password wrong')
            elif data['type'] is LOGIN_SUCCESS:
                root.destroy()
                friend_ui = FriendUI(data)
        else:
            messagebox.showinfo(message='password illegal')
    else:
        messagebox.showinfo(message='username illegal')


def register(username, password):
    if register_re.fullmatch(username):
        if register_re.fullmatch(password):
            mes = dict()
            mes['type'] = REGISTER
            mes['username'] = username
            mes['password'] = password
            mes['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            s.sendto(json.dumps(mes).encode('utf-8'), ADDR)
            rec, addr = s.recvfrom(1024)
            data = json.loads(rec.decode('utf-8'))
            if data['type'] is REGISTER_FAIL:
                messagebox.showinfo(message=data['reason'])
                password_entry.delete(0, END)
            elif data['type'] is REGISTER_SUCCESS:
                for x in data['friends']:
                    friends.append(x)
                root.destroy()
                friend_ui = FriendUI(data)
        else:
            messagebox.showinfo(message='password illegal')
    else:
        messagebox.showinfo(message='username illegal')


def login_click(event=None):
    if rmode.get() == '登录':
        login(user_entry.get(), password_entry.get())
    else:
        register(user_entry.get(), password_entry.get())


def enter(event=None):
    """

    :param event: Event
    """
    if event.widget is user_entry:
        password_entry.focus_set()
    elif event.widget is password_entry:
        login_click()


def change_mode(event=None):
    if mode.get() == '注册':
        mode.set('登录')
        rmode.set('注册')
        password_entry['show'] = t
    else:
        mode.set('注册')
        rmode.set('登录')
        password_entry['show'] = '*'


me = dict()
friends = []
root = Tk()
mode = StringVar(root, '注册')
rmode = StringVar(root, '登录')
root.maxsize(260, 200)
root.minsize(260, 200)
user_entry = Entry(root, font=('YaHei', 15))
user_entry.place(x=50, y=40, width=160)
password_entry = Entry(root, font=('YaHei', 15))
password_entry.place(x=50, y=70, width=160)
t = password_entry['show']
password_entry['show'] = '*'
reg = Label(root, textvariable=mode)
reg.place(x=180, y=100)
reg.bind('<Button-1>', change_mode)
login_button = Button(root, font=('YaHei', 15), bg='aqua', textvariable=rmode, command=login_click,
                      highlightthickness=0, padx=0,
                      pady=0, relief=FLAT)
login_button.place(x=50, width=160, y=130)
root.bind('<Return>', enter)
user_entry.focus_set()
root.mainloop()
