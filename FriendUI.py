from socket import *
from tkinter import *
from pprint import pprint
from QQCONFIG import *
import json
import threading
import time
from tkinter import messagebox


class FriendUI(object):

    class ChatUI(object):
        def __init__(self,friend_root, username):
            self.friend_root=friend_root
            self.chat_with = username
            self.my_name=friend_root.username
            self.chat_root = Toplevel()
            self.chat_root.protocol("WM_DELETE_WINDOW", self.close_chat)
            self.chat_root.title(('与{0}聊天中'.format(self.chat_with)))
            # 创建几个frame作为容器
            self.frame_left_top = Frame(self.chat_root, width=380, height=270, bg='white')
            self.frame_left_center = Frame(self.chat_root, width=380, height=100, bg='white')
            self.frame_left_bottom = Frame(self.chat_root, width=380, height=30)
            self.frame_right = Frame(self.chat_root, width=170, height=430, bg='white')
            ##创建需要的几个元素
            self.text_msglist = Text(self.frame_left_top)
            self.text_msg = Text(self.frame_left_center)
            self.text_msg.bind('<Key>',self.msg_edit)
            self.button_sendmsg = Label(self.frame_left_bottom, text=('发送'))
            self.button_sendmsg.bind('<Button-1>', self.send_message)
            # 创建一个绿色的tag
            self.text_msglist.tag_config('green', foreground='#008B00')
            # 使用grid设置各个容器位置
            self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
            self.frame_left_center.grid(row=1, column=0, padx=2, pady=5)
            self.frame_left_bottom.grid(row=2, column=0, padx=2, pady=5)
            self.frame_right.grid(row=0, column=1, rowspan=3, padx=4, pady=5)
            self.frame_left_top.grid_propagate(0)
            self.frame_left_center.grid_propagate(0)
            self.frame_left_bottom.grid_propagate(0)
            # 把元素填充进frame
            self.text_msglist.grid()
            self.text_msg.grid()
            self.button_sendmsg.place(y=0, x=340, width=40, height=30)
        def msg_edit(self,event=None):
            #print((event.keycode))
            if event.keycode == 13:
                #print(event)
                self.send_message()
        def send_message(self, event=None):
            self.text_msglist['state'] = NORMAL
            send_time =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 在聊天内容上方加一行 显示发送人及发送时间
            content = self.text_msg.get('0.0', END)
            if len(content) == 0 :
                messagebox.showinfo('提示','不能发送空消息')
                return
            elif len(content) >=800:
                messagebox.showinfo('提示','消息过长')
                return

            self.text_msglist.insert(END, self.my_name+send_time+'\n', 'green')
            self.text_msglist.insert(END, content + '\n')
            self.text_msglist.see(END)
            self.text_msg.delete('0.0', END)
            self.text_msglist['state'] = DISABLED
            message = dict()
            message['type'] = MESSAGE
            message['send_to'] = self.chat_with
            message['send_from'] = self.my_name
            message['text'] = content
            message['time'] = send_time
            s.sendto(json.dumps(message).encode('utf-8'), ADDR)

        def close_chat(self):
            self.friend_root.chat_list.pop(self.chat_with)
            self.chat_root.destroy()

        def receive_message(self, message):
            self.text_msglist['state'] = NORMAL
            # 在聊天内容上方加一行 显示发送人及发送时间
            msgcontent = message['send_from'] + ':' + message['time'] + '\n '
            self.text_msglist.insert(END, msgcontent, 'brown')
            self.text_msglist.insert(END, message['text'] + '\n')
            self.text_msglist.see(END)
            self.text_msg.delete('0.0', END)
            self.text_msglist['state'] = DISABLED

        def user_offline(self, message):
            self.text_msglist['state'] = NORMAL
            self.text_msglist.insert(END, message['time']+message['username'] + '下线了\n', 'red')
            self.text_msglist.see(END)
            self.text_msg.delete('0.0', END)
            self.text_msglist['state'] = DISABLED

        def user_online(self, message):
            self.text_msglist['state'] = NORMAL
            # 在聊天内容上方加一行 显示发送人及发送时间
            self.text_msglist.insert(END, message['time'] + message['username'] + '上线了\n', 'green')
            self.text_msglist.see(END)
            self.text_msg.delete('0.0', END)
            self.text_msglist['state'] = DISABLED

    def __init__(self,user_info):
        self.user_info=user_info
        self.username=user_info['username']
        threading._start_new_thread(self.rec_message, tuple())
        self.chat_list = dict()
        self.friend_root = Tk()
        self.friend_root.maxsize(300, 600)
        self.friend_root.minsize(300, 600)
        username_label = Label(self.friend_root, font=('YaHei', 30), text=user_info['username'])
        username_label.place(x=0, y=0)
        self.lb = Listbox(self.friend_root, bg='aqua', font=('YaHei', 15), selectmode=SINGLE)
        self.lb.place(x=0, y=80, width=300, height=520)
        self.lb.bind('<Double-Button-1>', self.start_chat_with)
        for x in range(len(user_info['friends'])):
            self.lb.insert(x, user_info['friends'][x])
        for data in user_info['wait_message']:
            threading._start_new_thread(self.deal_data,(data,))
        self.add_friend_button=Button(self.friend_root,font=('YaHei', 15),text="添加好友",command=self.add_friend)
        self.add_friend_entry=Entry(self.friend_root,font=('YaHei', 20))
        self.add_friend_entry.place(x=0,y=50,width=200,height=30)
        self.add_friend_button.place(x=200,y=50,width=100,height=30)
        self.friend_root.protocol("WM_DELETE_WINDOW", self.close_app)
        self.friend_root.mainloop()
    def add_friend(self,event=None):
        add_id=self.add_friend_entry.get()
        if register_re.fullmatch(add_id):
            if add_id == self.username:
                messagebox.showinfo('提示','不能添加自己为好友')
            elif add_id in self.user_info['friends']:
                messagebox.showinfo('提示',add_id+'已经是你的好友了')
            else:
                request={
                    'type':ADD_FRIEND,
                    'username':self.username,
                    'add_id':self.add_friend_entry.get(),
                    'time':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                }
                s.sendto(json.dumps(request).encode('utf-8'),ADDR)
        else:
            messagebox.showinfo("username illegal")

    def rec_message(self):
        while True:
            rec, addr = s.recvfrom(1024)
            data = json.loads(rec.decode('utf-8'))
            pprint(data)
            self.deal_data(data)

    def deal_data(self, data):
        if data['type'] is MESSAGE:
            if data['send_from'] in self.chat_list.keys():
                self.chat_list[data['send_from']].receive_message(data)
            else:
                self.chat_list[data['send_from']] = self.ChatUI(self, data['send_from'])
                self.chat_list[data['send_from']].receive_message(data)
        elif data['type'] is OFFLINE:
            if data['username'] in self.chat_list.keys():
                self.chat_list[data['username']].user_offline(data)
        elif data['type'] is ONLINE:
            if data['username'] in self.chat_list.keys():
                self.chat_list[data['username']].user_online(data)
        elif data['type'] is ADD_FRIEND:
            if messagebox.askyesno(title="好友请求", message=data['username'] + "请求添加你为好友，是否同意"):
                data['type'] = ADD_SUCCESS
                data['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                self.lb.insert(len(self.user_info['friends']),data['username'])
                self.user_info['friends'].append(data['username'])
            else:
                data['type'] = ADD_FAIL
                data['reason'] = '拒绝了你的请求'
                data['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            s.sendto(json.dumps(data).encode(),ADDR)
        elif data['type'] is ADD_SUCCESS:
            messagebox.showinfo('好友验证通过',data['add_id']+'同意了你的好友请求')
            self.lb.insert(len(self.user_info['friends']),data['add_id'])
            self.user_info['friends'].append(data['add_id'])
        elif data['type'] is ADD_WAIT:
            messagebox.showinfo('添加好友','添加好友请求已发送')
        elif data['type'] is ADD_FAIL:
            messagebox.showinfo('添加好友失败',data['reason'])

    def close_app(self, event=None):
        message = {
            'type': OFFLINE,
            'username': self.user_info['username'],
            'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }
        s.sendto(json.dumps(message).encode('utf-8'), ADDR)
        self.friend_root.destroy()

    def start_chat_with(self, event=None):
        user_chat_to = self.lb.get(self.lb.curselection()[0])
        if user_chat_to in self.chat_list.keys():
            self.chat_list[user_chat_to].chat_root.update()
            self.chat_list[user_chat_to].chat_root.deiconify()
        else:
            self.chat_list[user_chat_to] = self.ChatUI(self,user_chat_to)