#-*- coding: utf-8 -*-
#王強毅
#F74029038
#利用json爬出link 與 website 再去判斷link有幾個 link可能為0個所以要事先檢查好
import sys
import json
import re
if(len(sys.argv)<3):
	print "argv not enough"
	sys.exit(0)

file_name = sys.argv[1]
top_k=sys.argv[2]
out_link_num=[]
try:
	file = open(file_name,"r")
except:
	print("no input file")
	sys.exit(0)

	
def find_link(line):
	json_type=json.loads(line)
	website = json_type["Envelope"]["WARC-Header-Metadata"]["WARC-Target-URI"]
	metadata = json_type["Envelope"]["Payload-Metadata"]["HTTP-Response-Metadata"]["HTML-Metadata"]
	num = 0
	if("Links" in metadata):
		links = metadata["Links"] 
		for index in range(0,len(links),1):
			if("href" in links[index] ):
				num= num+1
			elif("url" in links[index]):
				num = num +1
	
		
	else:
		num=0
		
	dict = {}
	dict["website"]=website
	dict["num"] = num
	out_link_num.append(dict)
for line in file.readlines():
	find_link(line)
out_link_num = sorted(out_link_num, key=lambda d: d["num"])
out_link_num.reverse()
def print_link(out_link_num,top_k):
	top_k = int(top_k)
	count=1
	last_num=out_link_num[0]["num"]
	for i in range(0,len(out_link_num),1):
		cur_num = out_link_num[i]["num"]
		if (count>top_k):
			if(cur_num!=last_num):
				break
		last_num=cur_num
		print out_link_num[i]["website"],":",out_link_num[i]["num"]
		count+=1
print_link(out_link_num,top_k)
file.close()