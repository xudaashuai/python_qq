from tkinter import *
from tkinter import messagebox

from ChatUI import ChatUI
from QQCONFIG import *
from property import *

"""
#E0F7FA
#B2EBF2
#80DEEA
"""


class FriendUI(object):
	messages_no_read = {}
	friends_info = [
		#{
		#	username:
		#  mes_count:
		#  nickname:
		#}
	]
	friends_index = {
		# usename: index
	}

	def __init__(self, username):
		self.username = username
		self.nickname = username
		self.chat_list = dict()
		self.friend_root = Tk()
		self.friend_root.maxsize(300, 600)
		self.friend_root.minsize(300, 600)
		self.frame_top = Frame(self.friend_root, bg='#B2EBF2')
		self.frame_top.place(x=0, y=0, width=300, height=60)
		self.frame_top_2 = Frame(self.friend_root, bg='#80DEEA')
		self.frame_top_2.place(x=0, y=40, width=300, height=20)
		self.list_text = StringVar()
		self.nick_label_text = StringVar()
		self.nick_label_text.set(self.nickname)
		self.nick_entry = Entry(self.friend_root, font=('YaHei', 20), bg='#00BCD4')
		self.nick_entry.place(x=-220, y=0, width=220, height=40)
		self.nick_entry.bind('<Return>', self.change_ok_click)
		self.nickname_label = Label(self.friend_root, font=('YaHei', 28), textvariable=self.nick_label_text,
		                            bg='#B2EBF2')
		self.nickname_label.place(x=0, y=0, height=40)
		self.username_label = Label(self.friend_root, font=('YaHei', 10), text=self.username, bg='#80DEEA')
		self.username_label.place(x=0, y=40, height=20)
		bm1 = PhotoImage(file='change.png')
		bm2 = PhotoImage(file='cancel.png')
		bm3 = PhotoImage(file='ok.png')
		self.change_nick = Button(self.friend_root, image=bm1, bg='#B2EBF2', highlightthickness=0, padx=0,
		                          pady=0, relief=FLAT, command=self.change_nick_click)
		self.change_nick.place(x=260, y=0, width=40, height=40)
		self.change_cancel = Button(self.friend_root, image=bm2, bg='#B2EBF2', highlightthickness=0, padx=0,
		                            pady=0, relief=FLAT, command=self.change_cancel_click)
		self.change_cancel.place(x=220, y=-40, width=40, height=40)
		self.change_ok = Button(self.friend_root, image=bm3, bg='#B2EBF2', highlightthickness=0, padx=0,
		                        pady=0, relief=FLAT, command=self.change_ok_click)
		self.change_ok.place(x=260, y=-40, width=40, height=40)
		self.lb = Listbox(self.friend_root, bg='#4DD0E1', font=('YaHei', 15), selectmode=SINGLE, highlightthickness=0
		                  , relief=FLAT, listvariable=self.list_text)
		self.lb.place(x=0, y=60, width=300, height=540)
		self.lb.bind('<Double-Button-1>', self.start_chat_with)
		# self.lb.bind('<<ListboxSelect>>', self.start_chat_with)
		self.friend_root.protocol("WM_DELETE_WINDOW", self.close_app)
		self.rec_thread = threading.Thread(target=self.rec_message, args=tuple())
		self.rec_thread.setDaemon(True)
		self.rec_thread.start()
		self.friend_root.mainloop()

	def change_cancel_click(self):
		start_weight_anim(self.nickname_label, 'y', 200, offset=50)
		start_weight_anim(self.nick_entry, 'x', 100, offset=-220)
		start_weight_anim(self.change_ok, 'y', 100, offset=-40)
		start_weight_anim(self.change_nick, 'y', 100, offset=-80)
		start_weight_anim(self.change_cancel, 'y', 100, offset=-40)
		pass

	def change_ok_click(self, event=None):
		if int(self.nick_entry.place_info()['x']) < 0:
			return
		new_nick = self.nick_entry.get()
		if new_nick.__len__() == 0:
			return
		if (re.compile('[^:#]+').fullmatch(new_nick)):
			if new_nick.__len__() > 20:
				messagebox.showinfo('提示', '昵称太长')
				return
			s.sendto('10#{0}#'.format(new_nick).encode('utf-8'), ADDR)
			recThread = ReceiveThread()
			recThread.start()
			recThread.join(2)
			if q.empty():
				print('连接超时')
				messagebox.showinfo('提示', '修改失败')
			rec=q.get_nowait()
			rec_content = rec.decode('utf-8').split(':')
			if rec_content[0] == '10' and rec_content[1] == '01':
				self.nickname = rec_content[2]
				self.nick_label_text.set(self.nickname)
			else:
				messagebox.showinfo('提示', '修改失败')
				return
		else:
			messagebox.showinfo('提示', '含有非法字符:或者#')
			return
		start_weight_anim(self.nickname_label, 'y', 200, offset=50)
		start_weight_anim(self.nick_entry, 'x', 100, offset=-220)
		start_weight_anim(self.change_ok, 'y', 100, offset=-40)
		start_weight_anim(self.change_nick, 'y', 100, offset=-80)
		start_weight_anim(self.change_cancel, 'y', 100, offset=-40)

	def change_nick_click(self):
		self.nick_entry.focus_get()
		start_weight_anim(self.change_nick, 'y', 200, offset=80)
		start_weight_anim(self.nickname_label, 'y', 100, offset=-50)
		start_weight_anim(self.nick_entry, 'x', 230, offset=220)
		start_weight_anim(self.change_ok, 'y', 200, offset=40)
		start_weight_anim(self.change_cancel, 'y', 200, offset=40)

	def rec_message(self):

		while True:
			mes = "11#".encode('utf-8')
			print(mes)
			s.sendto(mes, ADDR)
			recThread = ReceiveThread()
			recThread.start()
			recThread.join(5)
			if q.empty():
				print('连接超时')
				continue
			rec=q.get_nowait()
			users = []
			index = 0
			print(rec)
			for i in range(rec.__len__()):
				if rec[i] == 35:
					users.append(rec[index:i])
					index = i + 1
			print(users)
			for i in range(users.__len__()):
				try :
					users[i]=users[i].decode('utf-8')
				except:
					users[i]=users[i].decode('gbk')
					print(users[i])

			rec_content = users
			rec_code = rec_content[0].split(':')
			for user in rec_content[1:]:
				user_info = user.split(':')
				if user_info.__len__() == 2:
					if user_info[0] == self.username:
						self.nickname = user_info[1]
						self.nick_label_text.set(self.nickname)
						continue
					if user_info[0] in self.friends_index:
						self.friends_info[self.friends_index[user_info[0]]]['nickname'] = user_info[1]
					else:
						self.friends_info.append({
							'username': user_info[0],
							'nickname': user_info[1],
							'mes_count': 0
						})
						self.friends_index[user_info[0]] = self.friends_info.__len__() - 1
				self.refresh_list()
			while True:
				mes = "05#".encode('utf-8')
				print(mes)
				s.sendto(mes, ADDR)
				recThread = ReceiveThread()
				recThread.start()
				recThread.join(5)
				if q.empty():
					print('连接超时')
					continue
				rec=q.get_nowait()
				rec_content = rec.decode('utf-8').split(':')
				if rec_content.__len__() is 2:
					print('没人发消息给你')
					break
				else:
					send_from = rec_content[1]
					if send_from not in self.friends_index:
						self.friends_info.append({
							'username': send_from,
							'nickname': send_from,
							'mes_count': 0
						})
						self.friends_index[send_from] = self.friends_info.__len__() - 1
					if send_from in self.chat_list.keys():
						self.chat_list[send_from].receive_message(rec_content[1:])
					else:
						self.lb.see(0)
						self.message_not_chat(rec_content[1:])
			time.sleep(10)

	def message_not_chat(self, message):
		print(message)
		if message[0] in self.messages_no_read.keys():
			self.messages_no_read[message[0]].append(message)
		else:
			self.messages_no_read[message[0]] = [message]
		self.refresh_list()

	def refresh_list(self):

		sorted(self.friends_info,key=lambda info:  info['mes_count'],reverse=True)
		for i in range(self.friends_info.__len__()):
			self.friends_index[self.friends_info[i]['username']]=i
		for item in self.messages_no_read.items():
			self.friends_info[self.friends_index[item[0]]]['mes_count'] = item[1].__len__()
		self.list_text.set(tuple(list("{0}({1})".format(self.friends_info[item[1]]['nickname'],
		                                                self.friends_info[item[1]]['mes_count'], )
		                              for item in self.friends_index.items())))

	def start_chat_with(self, event=None):
		user_chat_to = self.friends_info[self.lb.curselection()[0]]
		username = user_chat_to['username']
		print(user_chat_to)
		if username in self.chat_list.keys():
			self.chat_list[username].chat_root.update()
			self.chat_list[username].chat_root.deiconify()
		else:
			if self.friends_info[self.friends_index[username]]['mes_count'] != 0:
				self.chat_list[username] = ChatUI(self.username, user_chat_to, self, self.messages_no_read[username])
				self.messages_no_read[username] = []
				self.refresh_list()
			else:
				self.chat_list[username] = ChatUI(self.username, user_chat_to, self)

	def close_chat(self, username):
		if username in self.chat_list:
			self.chat_list.pop(username)

	def close_app(self, event=None):
		s.sendto("06#".encode('utf-8'), ADDR)
		self.friend_root.destroy()


if __name__ == '__main__':
	FriendUI('20151003248')
