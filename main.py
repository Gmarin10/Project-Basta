import matchFunctions
import airtable
import datetime

#get tables from base
fellows = matchFunctions.getTable('Fellows')
jobs = matchFunctions.getTable('Jobs')
matches = matchFunctions.getTable('Matches')

matchFunctions.cycleTables(jobs,fellows,matches)
