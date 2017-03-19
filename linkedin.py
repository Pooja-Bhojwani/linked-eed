import requests
from bs4 import BeautifulSoup

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
home_response = session.get('http://www.linkedin.com/nhome')
#home_response = session.get('https://www.linkedin.com/in/pooja-bhojwani-159420105/')
home = BeautifulSoup(home_response.text,"html.parser") # Get the html from the site
    
for script in home(["script", "style"]):
    script.extract() # Remove these two elements from the BS4 object
   

text = home.get_text()
print text