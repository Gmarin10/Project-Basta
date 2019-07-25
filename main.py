import BastaMatchingFunctions
import airtable

#Basta airtable API Keys
AIRTABLE_API_KEY = 'keyi9WRicMVH9g2ui'
##BASTA_BASE = 'app3yyj1S4SMRTGw6'

#Test base key
BASTA_BASE = 'appC07SJAr7flkFfO'

#Get required tables from Basta Base
fellows = BastaMatchingFunctions.getTable(BASTA_BASE, 'Fellows', AIRTABLE_API_KEY)
jobs = BastaMatchingFunctions.getTable(BASTA_BASE, 'Jobs', AIRTABLE_API_KEY)
matches = BastaMatchingFunctions.getTable(BASTA_BASE, 'Matches', AIRTABLE_API_KEY)

BastaMatchingFunctions.MatchOpps(jobs,fellows,matches)
