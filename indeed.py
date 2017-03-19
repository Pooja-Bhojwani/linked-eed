from bs4 import BeautifulSoup, SoupStrainer # For HTML parsing
import urllib2 # Website connections
import re # Regular expressions
from time import sleep # To prevent overwhelming the server between connections
import pandas as pd # For converting results to a dataframe and bar chart plots


def job_extractor(website):
    '''
    Cleans up the raw HTML
    '''
    company_name = "Unknown"
    try:
        site = urllib2.urlopen(website).read() # Connect to the job posting
    except: 
        return   # Need this in case the website isn't there anymore or some other weird connection problem 
    
    soup_obj = BeautifulSoup(site,"html.parser") # Get the html from the site
    
    for script in soup_obj(["script", "style"]):
        script.extract() # Remove these two elements from the BS4 object

    company = soup_obj.find('span', {'class' : 'company'})
    if company:
        company_name = company.get_text()
    # print company_name

    content = soup_obj.get_text() # Get the text from this 
        
    return content

def indeed_jobs(city = None, state = None):
    '''
    Inputs the location's city and state and then looks for the job in Indeed.com 
    '''
        
    final_job = 'software+developer' # searching for data scientist exact fit("data scientist" on Indeed search)
    
    # Make sure the city specified works properly if it has more than one word (such as San Francisco)
    if city is not None:
        final_city = city.split() 
        final_city = '+'.join(word for word in final_city)
        final_site_list = 'http://www.indeed.ca/jobs?q=' + final_job + '&l=' + final_city + '%2C+' + state # Join all of our strings together so that indeed will search correctly
    else:
        final_site_list = ['http://www.indeed.ca/jobs?q="', final_job, '"']

    final_site = ''.join(final_site_list) # Merge the html address together into one string

    
    base_url = 'https://www.indeed.ca/'

    print final_site_list
    

    try:
        html = urllib2.urlopen(final_site).read() # Open up the front page of our search first
    except:
        'That city/state combination did not have any jobs. Exiting . . .' # In case the city is invalid
        return
    soup = BeautifulSoup(html,"html.parser") # Get the html from the first page
    
    # Now find out how many jobs there were

    div = soup.find(id = 'searchCount')
    #print div
    
    num_jobs_area = soup.find(id = 'searchCount').string.encode('utf-8') # Now extract the total number of jobs found
                                                                        # The 'searchCount' object has this
    
    job_numbers = re.findall('\d+', num_jobs_area) # Extract the total jobs found from the search result
    
    # print job_numbers
    if len(job_numbers) > 3: # Have a total number of jobs greater than 1000
        total_num_jobs = (int(job_numbers[2])*1000) + int(job_numbers[3])
    else:
        total_num_jobs = int(job_numbers[2]) 
    
    city_title = city
    if city is None:
        city_title = 'Nationwide'
        
    print 'There were', total_num_jobs, 'jobs found,', city_title # Display how many jobs were found
    
    num_pages = total_num_jobs/10 # This will be how we know the number of times we need to iterate over each new
                                      # search result page
    job_descriptions = [] # Store all our descriptions in this list
    
    for i in xrange(0,num_pages): # Loop through all of our search result pages
        print 'Getting page', i
        start_num = str(i*1) # Assign the multiplier of 10 to view the pages we want
        current_page = ''.join([final_site, '&start=', start_num])
        print "So that's the current page"
        print current_page
        # Now that we can view the correct 10 job returns, start collecting the text samples from each
            
        html_page = urllib2.urlopen(current_page).read() # Get the page
            
        page_obj = BeautifulSoup(html_page,"lxml") # Locate all of the job links
        for script in page_obj(["script", "style"]):
            script.extract()

        # div = page_obj.find(id = 'resultsCol')

        print "And that's the result col"
        job_link_area = page_obj.find(id = 'resultsCol') # The center column on the page where the job postings exist
            
        job_URLS = [base_url + link.get('href') for link in job_link_area.find_all('a', href=True)]

        job_URLS = filter(lambda x:'clk' in x, job_URLS)

        for j in xrange(0,len(job_URLS)):
            final_description = job_extractor(job_URLS[j])
            if final_description: # So that we only append when the website was accessed correctly
                job_descriptions.append(final_description)
            #code for database connectivity
            sleep(1) 

        print 'Done with collecting the job postings!'    
        print 'There were', len(job_descriptions), 'jobs successfully found.'


indeed_jobs(city = 'Victoria', state = 'BC') 