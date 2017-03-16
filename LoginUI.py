from tkinter import *
from tkinter import messagebox

from FriendUI import FriendUI
from QQCONFIG import *
from property import *


def login(username, password):
    if name_re.fullmatch(username):
        if name_re.fullmatch(password):
            mes = "02#{0}#{1}#".format(username, password).encode('utf-8')
            print(mes)
            s.sendto(mes, ADDR)
            recThread=ReceiveThread()
            recThread.start()
            recThread.join(1)
            if q.empty():
                messagebox.showinfo(message='登录超时，请重试')
                return
            rec=q.get_nowait()
            rec_code = rec.decode('utf-8').split(':')[1]
            if rec_code == '01':
                root.destroy()
                friend_ui = FriendUI(username=username)
            elif rec_code == '02':
                messagebox.showinfo(message='密码错误')
            elif rec_code == '03':
                messagebox.showinfo(message='用户不存在')
            elif rec_code == '04':
                messagebox.showinfo(message='用户已登录')
                root.destroy()
                friend_ui = FriendUI(username=username)
        else:
            messagebox.showinfo(message='password illegal')
    else:
        messagebox.showinfo(message='username illegal')


def register(username, password, nickname):
    if name_re.fullmatch(username):
        if name_re.fullmatch(password):
            if re.compile("[^#:]+").fullmatch(nickname):
                mes = "01#{0}#{1}#{2}#{2}#".format(username, nickname, password).encode('utf-8')
                print(mes)
                s.sendto(mes, ADDR)
                rec, _ = s.recvfrom(1024)
                print(rec)
                rec_code = rec.decode('utf-8').split(':')[1]
                if rec_code == '01':
                    messagebox.showinfo(message='注册成功,请登录')
                    change_mode()
                elif rec_code == '03':
                    messagebox.showinfo(message='用户已存在')
            else:
                messagebox.showinfo(message='用户名非法')
        else:
            messagebox.showinfo(message='密码非法')
    else:
        messagebox.showinfo(message='用户名非法')


def login_click(event=None):
    if rmode.get() == '登录':
        login(user_entry.get(), password_entry.get())
    else:
        register(user_entry.get(), password_entry.get(), name_entry.get())


def enter(event=None):
    if event.widget is user_entry:
        password_entry.focus_set()
    elif event.widget is password_entry:
        login_click()


def change_mode(event=None):
    if mode.get() == '注册':
        start_window_anim(root, 'height', 100, offset=30)
        start_weight_anim(name_entry, 'height', 100, offset=25)
        start_weight_anim(user_entry, 'y', 100, offset=30)
        start_weight_anim(password_entry, 'y', 100, offset=30)
        start_weight_anim(user_label, 'y', 100, offset=30)
        start_weight_anim(pass_label, 'y', 100, offset=30)
        start_weight_anim(nick_label, 'y', 100, offset=80)
        start_weight_anim(reg, 'y', 100, offset=30)
        start_weight_anim(login_button, 'y', 100, offset=30)
        mode.set('登录')
        rmode.set('注册')
        password_entry['show'] = t
    else:
        start_weight_anim(name_entry, 'height', 100, offset=-25)
        start_window_anim(root, 'height', 100, offset=-30)
        start_weight_anim(nick_label, 'y', 100, offset=-80)
        start_weight_anim(user_entry, 'y', 100, offset=-30)
        start_weight_anim(password_entry, 'y', 100, offset=-30)
        start_weight_anim(pass_label, 'y', 100, offset=-30)
        start_weight_anim(user_label, 'y', 100, offset=-30)
        start_weight_anim(reg, 'y', 100, offset=-30)
        start_weight_anim(login_button, 'y', 100, offset=-30)
        user_entry.place_info()['x'] = 100
        mode.set('注册')
        rmode.set('登录')
        password_entry['show'] = '*'


root = Tk()

mode = StringVar(root, '注册')
rmode = StringVar(root, '登录')
root.geometry('310x200')
root.resizable(width=False, height=False)
user_label = Label(root, text='用户名:')
user_label.place(x=50, y=40)
nick_label = Label(root, text='昵称:')
nick_label.place(x=50, y=-40)
pass_label = Label(root, text='密码:')
pass_label.place(x=50, y=70)
name_entry = Entry(root, font=('YaHei', 15))
name_entry.place(x=100, y=40, height=0, width=160)
user_entry = Entry(root, font=('YaHei', 15))
user_entry.place(x=100, y=40, width=160, height=25)
password_entry = Entry(root, font=('YaHei', 15))
password_entry.place(x=100, y=70, width=160, height=25)

t = password_entry['show']
password_entry['show'] = '*'
reg = Label(root, textvariable=mode)
reg.place(x=230, y=100)
reg.bind('<Button-1>', change_mode)
login_button = Button(root, font=('YaHei', 15), bg='aqua', textvariable=rmode, command=login_click,
                      highlightthickness=0, padx=0,
                      pady=0, relief=FLAT)
login_button.place(x=50, width=210, y=130)
root.bind('<Return>', enter)
user_entry.focus_set()
root.mainloop()
