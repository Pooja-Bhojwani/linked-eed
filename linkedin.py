import requests
from bs4 import BeautifulSoup
import json
import urllib2
from HTMLParser import HTMLParser
import sqlite3

url_entered = "https://www.linkedin.com/in/pooja-bhojwani-159420105/"
# url_entered = "https://www.linkedin.com/in/dhanush987/"
# url_entered = "https://www.linkedin.com/in/disha-garg-85891768/"
user_name   = "test123@gmail.com"
password    = "test123"


def linkedin_login(user_name, password, url_entered):
	# Get login form
	URL = 'https://www.linkedin.com/uas/login'
	session = requests.session()
	login_response = session.get('https://www.linkedin.com/uas/login')
	login = BeautifulSoup(login_response.text,"html.parser")

	# Get hidden form inputs
	inputs = login.find('form', {'name': 'login'}).findAll('input', {'type': ['hidden', 'submit']})

	# Create POST data
	post = {input.get('name'): input.get('value') for input in inputs}
	post['session_key'] = user_name
	post['session_password'] = password

	# Post login
	post_response = session.post('https://www.linkedin.com/uas/login-submit', data=post)

	# Get home page
	home_response = session.get(url_entered)

	return home_response 


def feature_extraction(home_response):
	# Get the html from the site
	home_page = BeautifulSoup(home_response.text,'lxml')
	
	# Parse the home_response page to get top skills from linkedin
	home_decoded_string = home_page.prettify().encode("utf-8")
	location_code_init = home_decoded_string.split('"patentView"')
	home_code_chunk = location_code_init[1].split("/code")[0]


	#Fetch the current location from linkedin page
	locationName = home_code_chunk.split('"summary"')[1].split('"locationName":"')[1].split('","')[0]


	#Fetching all past designations from linkedin
	list_of_designation = list()
	unique_designations = list()
	designation_code_chunk = home_code_chunk.split('"companyName"')
	for i in range(len(designation_code_chunk)-1):
		if len(designation_code_chunk[i+1].split(',"title":"')) > 1:
			list_of_designation.append((designation_code_chunk[i+1].split(',"title":"')[1].split('","')[0]))

	[unique_designations.append(item) for item in list_of_designation if item not in unique_designations]

	string_of_designations = ", ".join(unique_designations)



	#Get the top skills from the linkedin page

	#HTML parser used to parse the web page line by line
	skills_code_chunk = ""
	for line in home_response.iter_lines():
		try:
			parser = HTMLParser()
			html_decoded_string = parser.unescape(line)
			if html_decoded_string.find("vieweeEndorsementsEnabled") != -1:
				skills_code_chunk = html_decoded_string
			json_skills_code_chunk = json.loads(line)
		except Exception as e:
			pass


	#Fetching the list of skills finally from the chunk of extracted html code
	list_of_skills = list()
	final_list = skills_code_chunk.split('","name":"')
	for i in range(len(final_list)-1):
		list_of_skills.append(str(final_list[i+1].split('","')[0]))

	string_of_skills = ", ".join(list_of_skills)

	return locationName, string_of_designations, string_of_skills


def database_connect(locationName, string_of_designations, string_of_skills):
	conn = sqlite3.connect('linkedeed.db')
	c = conn.cursor()
	c.execute('DROP TABLE IF EXISTS linkedin_skills')
	c.execute('CREATE TABLE linkedin_skills(ID INTEGER PRIMARY KEY AUTOINCREMENT, LOCATION TEXT, DESIGNATIONS text, SKILLS TEXT)')
	c.execute('INSERT INTO linkedin_skills (ID, LOCATION, DESIGNATIONS, SKILLS) VALUES(?, ?, ?, ?)', ( 1, locationName, string_of_designations, string_of_skills))
	conn.commit()
	c.close()
	conn.close()


home_response = linkedin_login(user_name, password, url_entered)
locationName, string_of_designations, string_of_skills = feature_extraction(home_response)
database_connect(locationName, string_of_designations, string_of_skills)

