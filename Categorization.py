import webapp2
import logging
import json
from database.rawQuery import rawQuery
from plaidIntegration.getTransactions import GetTransactions
import pprint
from oktaIntegration.validateAccessToken import getLoggedUserId

class categorizer(webapp2.RequestHandler):
	def get(self):
		self.decorateHeaders()
		self.response.headers["Content-Type"] = "application/json"
		# bank = self.bank()
		# catMap = self.categoryMapping()
		oktaAccessToken = self.request.headers['Authorization']
		userId = getLoggedUserId(oktaAccessToken)
		if userId:
			logging.debug(userId)
			self.response.write(json.dumps(self.categorize(userId)))
		else:
			self.response.write(json.dumps({"status":False}))
#		spending = self.categorize(bank)
#		self.response.write(spending)
#		self.response.write(queryResult)
		# self.response.write(catMap)

	def bank(self):
		return([['Giant',25],['Safeway',50],['Matteogay',69]])

	def categoryMapping(self):
		queryResult = rawQuery("""	SELECT name,expense_descriptions.description 
									FROM budgetizer.budget_categories 
									INNER JOIN budgetizer.expense_descriptions 
									ON budget_categories.id = expense_descriptions.budget_category_id;"""

									,None
								)
		# print(queryResult)
		catMap = {}
		for entry in queryResult:
			if entry[0] in catMap:
				catMap[entry[0]].append(entry[1])
			else:
				catMap[entry[0]] = [entry[1]]
		return(catMap)

	def reverseCategoryMapping(self):
		queryResult = rawQuery("""	SELECT name,expense_descriptions.description 
									FROM budgetizer.budget_categories 
									INNER JOIN budgetizer.expense_descriptions 
									ON budget_categories.id = expense_descriptions.budget_category_id;"""

									,None
								)
		reverseCatMap={}
		for entry in queryResult:
			# print(entry[1],entry[0])
			reverseCatMap[entry[1]]=entry[0]


		return reverseCatMap

	def categorize(self,userId):
		reverseCatMap=self.reverseCategoryMapping()
		print(reverseCatMap)
		transactionsResponse=GetTransactions().byUserId(userId)
		transactions=transactionsResponse['transactions']
		numberOfBanks=transactionsResponse['numberOfBanks']
		categorized = {}
		categorized['numberOfBanks']=numberOfBanks
		categorized['summary']={}
		categorized['summary']['Unknown']={'value':0}
		categorized['Unknown']=0
		categorized['total']=0
		categorized['missingMatches']=[]
		categorized['transactionCount']=len(transactions)
		for transaction in transactions:
			foundMatch=False
			if transaction['category']:
				for category in transaction['category']:
					# print(category)
					if category in reverseCatMap:
						foundMatch=True
						if category in categorized['summary']:
							categorized['summary'][category]['value']+=transaction['amount']
							categorized['summary'][category]['transactions'].append(transaction)
						else:
							categorized['summary'][category]={'value':transaction['amount'],'transactions':[]}
						break
				if foundMatch==False:
					categorized['missingMatches']+=transaction['category']
			if foundMatch==False:
				categorized['Unknown']+=transaction['amount']
				categorized['summary']['Unknown']['value']+=transaction['amount']
				
			categorized['total']+=transaction['amount']

		# CHECKSUM
		checksum=0
		for category in categorized['summary']:
			checksum+=categorized['summary'][category]['value']
		categorized['checksum']=checksum

		# DETERMINING UNKNOWN COUNTS
		unknownCounts = {}
		for categoryName in categorized['missingMatches']:
			if categoryName in unknownCounts:
				unknownCounts[categoryName]+=1
			else:
				unknownCounts[categoryName]=1
		categorized['missingMatches']=unknownCounts

		return categorized

	def decorateHeaders(self):
		"""Decorates headers for the current request."""
		self.response.headers.add_header('Access-Control-Allow-Origin', '*')
		self.response.headers.add_header('Access-Control-Allow-Headers', 'Content-Type, Accept, Authorization')
		self.response.headers.add_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')

	def options(self):
		"""Default OPTIONS handler for the entire app."""
		self.decorateHeaders()

'''
catList = pd.read_csv(f2,header=None,keep_default_na=False) #read my list of categories and call it "catList"
mint = {} #create my blank associative array of categories and keywords

#creates mint
for column in catList:
	key = catList[column][0]
	values = catList[column]
	mint[key] = values
'''
'''
	def categorize(self,bank):
		spending = {}
		spending['Unknown'] = 0
		mint = self.categoryMapping()
		for expense in bank: 
			description = expense[0] 
			value = expense[1] 
			foundMatch = False 
			for cat in mint: 
				categoryName=cat 
				categoryVendors = mint[cat] 
				for vendor in categoryVendors: 
					if "".join(vendor.lower().split()) in "".join(description.lower().split()): 
						foundMatch = True
						if cat in spending: 
							spending[cat]+=value
						else: 
							spending[cat]=value 
			if foundMatch == False: 
				spending['Unknown'] += value 
		return spending
		
	def perSpendCat(self,spending):
		return 'Total spend categorized:', round((1-(float(self.spending['Unknown']) / float(sum(self.spending.values()))))*100,1),"%"

'''
'''
OLD ORIGINAL STUFF
import pandas as pd
###do stuff to make me able to use my bank statement
f1 = 'bank.csv' #the file where my bank statement lives
statement = pd.read_csv(f1,header=None) #read my bank statement file and call it "statement"
bank = [] #create my blank array of expenses
for index, description in enumerate(statement[0]): #for each row in my file (create an index)
	expense = round(statement[1][index],0)
	if statement[1][index] < 0:
		bank.append([description, expense*-1])#append the description and the value to bank. * value by -1
	else:
		bank.append([description, expense]) #do same except * value by -1
###do stuff to make me able to use my categories list
f2 = "Categories.csv" #the file where my list of categories lives
catList = pd.read_csv(f2,header=None,keep_default_na=False) #read my list of categories and call it "catList"
mint = {} #create my blank associative array of categories and keywords

#creates mint
for column in catList:
	key = catList[column][0]
	values = catList[column]
	mint[key] = values

#removes the first value in dictionary (since that is the key in dictionary.) Also removes blank entries
for category in mint:
	del mint[category][0]
	blankspaces = 0
	for vendor in mint[category]:
		if vendor == "":
			blankspaces += 1
	while blankspaces > 0:
		del mint[category][len(mint[category])]
		blankspaces -= 1
'''