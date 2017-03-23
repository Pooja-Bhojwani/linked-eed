import sqlite3


skills = {"java, c, javascript, python, ruby on rails, c++"}
text   = "This is a sample "

conn = sqlite3.connect('linkedeed.db')
c = conn.cursor()
c.execute('''SELECT * FROM indeed_jobs''')
user1 = c.fetchone() #retrieve the first row
print(user1[0]) #Print the first column retrieved(user's name)
all_jobs = c.fetchall()
for row in all_jobs:
    print type(row[3])

text_file = open("data.txt")
lines = text_file.readlines()
new_list = list()
for element in lines:
	element = element.strip()
	new_list.append(element)
print new_list

# for row in all_rows:
	# if 
indeed_list = list()

# for job in all_jobs:
# 	i = 0
# 	print type(job[3])
# 	for elements in new_list:
# 		if(str(job[3]).find(elements)!= -1):
# 			indeed_list.append(1)
# 			i += 1
# 		else:
# 			indeed_list.append(0)
# 	print i

# print len(indeed_list)
# print indeed_list



