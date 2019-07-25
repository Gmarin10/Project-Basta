import airtable


#dictionaries used to map menu item inconsistencies
FellowOppTypes = {'Full-time Immediate': 1,
                  'Full-time Later': 2,
                  'Internship - Fall': 3,
                  'Internship - Summer': 4,
                  'Internship - Spring': 5
                  }

JobOppTypes = {'Full-time': 1,
               'Internship - Immediate': 2,
               'Internship - Fall': 3,
               'Internship - Summer': 4,
               'Internship - Spring': 5,
               'Long-term internship / Fellowship': 6,
               'Internship - Winter' : 7,
               'Part Time': 8,
               'Events/Immersion Experiences': 9
                  }

FellowLocTypes = {'The Northeast only (e.g., Philly, Boston)': 1,
                  'Any major cities': 2,
                  'Anywhere': 3
                  }

JobLocTypes = {'Any major city': 1,
               'Northeast': 2,
               'Other not NYC': 3
               }

#tablename = valid table from airtable
def getTable(base, tablename, apiKey):
    fellowstable = airtable.Airtable(base, tablename, apiKey)
    return fellowstable

#gets a percentage of skills that are matched within list of job skills
#int match, list jobskills[]
def matchPercent(match, jobskills):
    percent = (match / len(jobskills))*100
    return int(percent)

#goes to airtable and adds rows where students match jobs
def addMatch(job, person, matches, finalPercent):
    fellowName = person['fields']['Name']
    title = job['fields']['Opportunity']
    newRecord = {'Fellow': fellowName, 'Opportunity': title, 'Match': finalPercent}
    matches.insert(newRecord)

#the type of job matches what the fellow wants
#2 seperate dictionaries mapped to numbers that can be compared
def oppTypeMet(person, job):
    try:
##        job['fields']['Job Type']                                   #output: Full-time
##        JobOppTypes[job['fields']['Job Type']]                      #output: 1
##        person['fields']['Opportunity Types'][0]                    #output: Full-time Immediate
##        FellowOppTypes[person['fields']['Opportunity Types'][0]]    #output: 1
        for opportunity in person['fields']['Opportunity Types']:
            if FellowOppTypes[opportunity] == JobOppTypes[job['fields']['Job Type']]:
                return True
            else:
                return False
    except:
        return False

#if the fellow meets the jobs gpa requirement
def gpaMet(person, job):
    try:
        if person['fields']['GPA'] >= job['fields']['GPA Cut-off']:
            return True
        else:
            return False
    except:
        return False

#if job location resides in fellows desired location
def locationMet(person, job):
    try:
        for location in person['fields']['Relocate - Where?']:
            if FellowLocTypes[location] == JobLocTypes[job['fields']['Location Type']] or FellowLocTypes[location] == 3:
                return True
            else:
                return False
    except:
        return False
                                           
#still missing info
#if fellow interest is aligned with job
def fieldMet(person, job):
    try:
        for field in person['fields']['Fields/Functions of Interest']:
            if field == job['fields']['Field/Function']:
                return True
            else:
                return True
    except:
        return True

def skillsPercent(person, job):
    skillmatch = 0
    try:
        for skill in person['fields']['Technical Skills']:
            if skill in job['fields']['Technical Skills']:
                skillmatch += 1
        return matchPercent(skillmatch, job['fields']['Skills categories'])
    except:
        return skillmatch  

    skillPercent = matchPercent(skillmatch, job['fields']['Skills categories'])

def MatchOpps(jobs,fellows,matches):
    
    f = 0
    for person in fellows.get_all(view="Gary's View",sort='Name'):
        for job in jobs.get_all(view="Gary's View",sort='Opportunity'):
            if oppTypeMet(person, job) and gpaMet(person, job) and locationMet(person, job) and fieldMet(person, job):
            #if fieldMet(person, job):
                matchnum = skillsPercent(person, job)
                if matchnum >= 0:
                    addMatch(job, person, matches, matchnum)
        f = f+1
        print ('finished fellow ' + str(f))
    print ('finished all')
















    
