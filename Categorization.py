import webapp2
import logging
from database.rawQuery import rawQuery

class categorizer(webapp2.RequestHandler):
	def get(self):
		self.response.headers["Content-Type"] = "text/plain"
		bank = self.bank()
		catMap = self.categoryMapping()
#		spending = self.categorize(bank)
#		self.response.write(spending)
#		self.response.write(queryResult)
		self.response.write(catMap)

	def bank(self):
		return([['Giant',25],['Safeway',50],['Matteogay',69]])

	def categoryMapping(self):
		queryResult = rawQuery('SELECT name,expense_descriptions.description FROM \
			budgetizer.budget_categories INNER JOIN budgetizer.expense_descriptions on \
			budget_categories.id = expense_descriptions.budget_category_id;',None)
		catMap = {}
		for entry in queryResult:
			if entry[0] in catMap:
				catMap[entry[0]] += (entry[1])
			else:
				catMap[entry[0]] = entry[1]
		return(catMap)

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