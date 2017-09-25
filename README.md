# linked-eed
Aim is to come up with a job recommender system, which takes the skills from LinkedIn and jobs from Indeed and throws the best jobs available for you according to your skills.

DataSet Used:
To detect the skillset from the text posted on Indeed, a universal skillset dataset was used:
  https://www.itsyourskills.com/list-of-skills/

Process:
The data from LinkedIn is scraped to get the skills, also, data from Indeed is scraped to get the skills required for the job. They are then matched using Jaccard Similarity. The best matching jobs are showed on the basis of matching percentage.


All the user need to do is: Login to LinkedIn :). Once he is logged in, he can search for relevant job for himself/herself or his/her connections.
    
To run it: 
Step 1: Go to linkedDeed/ directory, run this command python app.py.
Step 2: Open linkedDeed/templates/index.html in the browser.
Step 3: Fill up the form and submit.

Future Work(If you are interested in extending this project then you could do the following):
 -- We are just considering the skillset which we get from LinkedIn. There are so many other sections on LinkedIn like Summary, Experience, Projects which could be mined to make better recommendations.
 
Demo Link:
    https://www.youtube.com/watch?v=WbtJNs3p6cA
 
