import time
from tkinter import *
from tkinter import messagebox

from QQCONFIG import *


class ChatUI(object):
    def __init__(self, my_name, user_info, friend_ui, messages=None):
        self.friend_ui=friend_ui
        self.chat_username = user_info['username']
        self.chat_nickname = user_info['nickname']
        self.my_name = my_name
        self.chat_root = Toplevel(friend_ui.friend_root)
        self.chat_root.protocol("WM_DELETE_WINDOW", self.close_chat)
        self.chat_root.title(('与{0}聊天中({1})'.format(self.chat_nickname, self.chat_username)))
        # 创建几个frame作为容器
        self.frame_left_top = Frame(self.chat_root, width=380, height=270, bg='white')
        self.frame_left_center = Frame(self.chat_root, width=380, height=100, bg='white')
        self.frame_left_bottom = Frame(self.chat_root, width=380, height=30)
        self.frame_right = Frame(self.chat_root, width=170, height=430, bg='white')
        ##创建需要的几个元素
        self.text_msglist = Text(self.frame_left_top)
        self.text_msglist['state'] = DISABLED
        self.text_msg = Text(self.frame_left_center,wrap='none')
        self.text_msg.bind('<Return>', self.send_message)

        self.button_sendmsg = Label(self.frame_left_bottom, text='发送')
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
        if messages is not None:
            for x in messages:
                self.receive_message(x)

    def send_message(self, event=None):
        self.text_msglist['state'] = NORMAL
        send_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 在聊天内容上方加一行 显示发送人及发送时间
        content = self.text_msg.get('0.0', END)
        if len(content) == 0:
            messagebox.showinfo('提示', '不能发送空消息')
            return
        elif len(content) >= 800:
            messagebox.showinfo('提示', '消息过长')
            return
        mes = "03#{0}#{1}#".format(self.chat_username, content).encode('utf-8')
        print(mes)
        s.sendto(mes, ADDR)
        recThread = ReceiveThread()
        recThread.start()
        recThread.join(5)
        if q.empty():
            print('连接超时')
            return
        rec=q.get_nowait()
        print(rec)
        rec_code = rec.decode('utf-8').split(':')[1]
        self.text_msglist.delete(str(float(self.text_msglist.index(END)) - 2.0), END)
        self.text_msglist.insert(END, self.my_name + ':' + send_time + '\n', 'green')
        self.text_msglist.insert(END, '  ' + content + '\n\n\n\n')
        self.text_msglist.see(END)
        self.text_msg.delete('0.0',END)
        self.text_msglist['state'] = DISABLED
        return 'break'

    def close_chat(self):

        self.chat_root.destroy()
        self.friend_ui.close_chat(self.chat_username)

    def receive_message(self, message):
        self.text_msglist['state'] = NORMAL
        self.text_msglist.delete(str(float(self.text_msglist.index(END)) - 2.0), END)
        time_text = message[1] + ':' + message[2] + ':' + message[3]
        msg_content = self.chat_nickname + ':' + time_text + '\n '
        self.text_msglist.insert(END, msg_content, 'brown')
        self.text_msglist.insert(END, '  ' + message[4] + '\n\n\n\n')
        self.text_msglist.see(END)
        self.text_msg.delete('0.0', END)
        self.text_msglist['state'] = DISABLED
