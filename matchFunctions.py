##no longer in use

import airtable
import datetime

#tablename = valid table title
def getTable(tablename):
    fellowstable = airtable.Airtable('appepRGO7wI0cmN4q', tablename,'keyi9WRicMVH9g2ui')
    return fellowstable

#int match, list jobskills[]
def matchPercent(match, jobskills):
    percent = (match / len(jobskills))*100
    return int(percent)

#creates a simple ID that can be referenced later to update or delete records
def createID(name, title):
    uniID = name+title
    return uniID

#final percentage taking into account all categories
def finalPercent(skillPercent, majorCheck):
    percent = (skillPercent * 0.8) + (majorCheck * 20)
    return percent/100

#cycles through both tables and compares necesarry lists
def cycleTables(jobs, fellows, matches):

    for person in fellows.get_all(sort='Name'):
        for job in jobs.get_all(sort='Title'):
            #counter for matching hardskills
            skillmatch = 0
            
            #grabs gpa of the fellow     
            fellgpa = float(person['fields']['GPA'])
            #grabs the gpa requirement from the job, given that it will at least be 0.00 float
            gpareq = float(job['fields']['GPA Req'])
            
            #gpa check, disqualifies fellow from job if not met
            if fellgpa >= gpareq:

                #job type check can also be added to condion in gpa check
                #while person['fields']['Job Type'] == job['fields']['Job Type']:
                
                #skill check 
                for skill in person['fields']['Skills categories']:
                    if skill in job['fields']['Skills categories']:
                        skillmatch += 1

                skillPercent = matchPercent(skillmatch, job['fields']['Skills categories'])
                
                #check to see if major is matching
                if person['fields']['Major'] in job['fields']['Major']:
                    majorCheck = 1
                elif job['fields']['Major'] == 'None':
                    majorCheck = 1
                else:
                    majorCheck = 0
                
                #relocation check
                #need to finalize lists for location elements
                finmatch = finalPercent(skillPercent, majorCheck)
                
                addMatch(job, person, matches, finmatch)
                #altMatch(job, person, matches, finmatch)
                #print (person['fields']['Name'] + ' is ' + str(finmatch) + '% match with ' + job['fields']['Title'])
            
#goes to airtable and adds rows where students match jobs
def addMatch(job, person, matches, finalPercent):
    
    if finalPercent >= 0.40:
        
        fellowName = person['fields']['Name']
        title = job['fields']['Title']
        uniID = createID(fellowName, title)
        
        record = {'Fellow': fellowName, 'Job': title, 'Match': finalPercent, 'ID': uniID}
        if matches.search('ID', uniID):
            matches.update_by_field('ID', uniID, record)
        else:
            matches.insert(record)

##def altMatch(job, person, matches, finalPercent):
##
##    fellowName = person['fields']['Name']
##    fellow = fellowName + str(finalPercent)
##    title = job['fields']['Title']
##    record = {'Job': title, 'Match': fellow}
##    matches.insert(record)
##    
    #create column with job - not possible?
    #add person as a row
    #finalpercent is the value in the cell

#checks if job is expired, if so call delete function
def checkExpireDates(job):
    d = datetime.datetime.today()
    date = d.strftime('%Y-%m-%d')
    print (date)
    for job in jobs.get_all(sort='Title'):
        deadline = job['fields']['Expires']
        print (deadline, type(deadline))
