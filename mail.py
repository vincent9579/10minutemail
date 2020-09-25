import requests
from bs4 import BeautifulSoup
import json
import time
import sys
import os
def restart_program():
	python = sys.executable
	os.execl(python, python, * sys.argv)

def get():
	url="https://10minutemail.net/address.api.php"
	cookies="PHPSESSID=678c127330a8291d2ba60e32d703573d"
	header = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63',
	'Connection': 'keep-alive',
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Cookie': cookies}
	resp=requests.get(url,headers=header)
	soup =BeautifulSoup(resp.text, "html.parser")
	data=json.loads(soup.text)
	get_mail=data['permalink']['mail']
	get_link=data['permalink']['url']
	mail_list=data['mail_list']
	mail_left_time=data['mail_left_time']
	return get_mail,get_link,mail_list,mail_left_time

def get_reply(mail_id):
	url="https://10minutemail.net//mail.api.php?mailid={}&sessionid=678c127330a8291d2ba60e32d703573d".format(mail_id)
	cookies="PHPSESSID=678c127330a8291d2ba60e32d703573d"
	header = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63',
	'Connection': 'keep-alive',
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Cookie': cookies}
	resp=requests.get(url,headers=header)
	soup =BeautifulSoup(resp.text, "html.parser")
	data=json.loads(soup.text)
	mail_from=data['from']
	mail_to=data['to']
	subject=data['subject']
	datetime=data['datetime']
	header_decode_from=data['header_decode']['from']
	header_decode_from_name=[]
	for i in range(0,len(header_decode_from)):
		header_decode_from_name.append(header_decode_from[i]['name'])
	html=data['html']
	return mail_from,mail_to,subject,datetime,header_decode_from_name,html


if __name__ == "__main__":
	get_mail,get_link,mail_list,mail_left_time = get()
	print(get_mail)
	print(get_link)
	print("剩下:%d秒\n\n"%(mail_left_time))
	print("=================================\n")
	for i in range(0,len(mail_list)):
		mail_id = mail_list[i]['mail_id']
		mail_from,mail_to,subject,datetime,header_decode_from_name,html=get_reply(mail_id)
		mail_string='寄件人:{}\n收件人:{}\n時間:{}\nName:{}\n\n標題:{}\n內容:{}\n'.format(mail_from,mail_to,datetime,header_decode_from_name,subject,html)
		print(mail_string)
		print("=================================\n")
	get_mail_old = get_mail
	mail_list_len = len(mail_list)
	while True:
		get_mail,get_link,mail_list,mail_left_time = get()
		if get_mail_old == get_mail:
			if len(mail_list) != mail_list_len:
				mail_id = mail_list[0]['mail_id']
				mail_from,mail_to,subject,datetime,header_decode_from_name,html=get_reply(mail_id)
				mail_string='寄件人:{}\n收件人:{}\n時間:{}\nName:{}\n\n標題:{}\n內容:{}\n\n'.format(mail_from,mail_to,datetime,header_decode_from_name,subject,html)
				print("=================================\n")
				mail_list_len = len(mail_list)
				print(mail_string)
		else:
			print("信箱已失效 自動重啟中...")
			restart_program()
			
