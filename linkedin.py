import requests
from bs4 import BeautifulSoup
import json
import urllib2
from HTMLParser import HTMLParser
import sqlite3

# Get login form
URL = 'https://www.linkedin.com/uas/login'
session = requests.session()
login_response = session.get('https://www.linkedin.com/uas/login')
login = BeautifulSoup(login_response.text,"html.parser")

# Get hidden form inputs
inputs = login.find('form', {'name': 'login'}).findAll('input', {'type': ['hidden', 'submit']})

# Create POST data
post = {input.get('name'): input.get('value') for input in inputs}
post['session_key'] = 'dhanush987@gmail.com'
post['session_password'] = 'welcome@456'

# Post login
post_response = session.post('https://www.linkedin.com/uas/login-submit', data=post)

# Get home page
# home_response = session.get('http://www.linkedin.com/nhome')
home_response = session.get('https://www.linkedin.com/in/dhanush987/')
home = BeautifulSoup(home_response.text,'lxml') # Get the html from the site
# print type(home_response)
# Parse the home_response page to get top skills from linkedin
final_msg = ""
for line in home_response.iter_lines():
	try:
		parser = HTMLParser()
		html_decoded_string = parser.unescape(line)	
		if html_decoded_string.find("vieweeEndorsementsEnabled") != -1:
			final_msg = html_decoded_string
		msg = json.loads(line)
	except Exception as e:
		pass


list_of_skills = list()
final_list = final_msg.split('","name":"')
for i in range(len(final_list)-1):
	list_of_skills.append(str(final_list[i+1].split('","')[0]))

string_of_skills = ", ".join(list_of_skills)

print string_of_skills



conn = sqlite3.connect('stuffToPlot.db')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS linkedin_skills')
c.execute('CREATE TABLE linkedin_skills(ID INTEGER PRIMARY KEY AUTOINCREMENT, SKILLS TEXT)')
c.execute('INSERT INTO linkedin_skills (ID, SKILLS) VALUES(?, ?)', ( 1, string_of_skills))
conn.commit()
c.close()
conn.close()
