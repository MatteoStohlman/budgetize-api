import webapp2
import dbConnectExample
import logging
from plaid import Client


class MainPage(webapp2.RequestHandler):

    def get(self):
    	bankExport = [["Giant",110],["Safeway",110],["Washington Gas",110],["Car",110]]

    	categoriesMapping = {}
    	categoriesMapping['Groceries']=['Giant','Safeway']
    	categoriesMapping['Utilities']=['Old Dominion','Washington Gas']

    	categorizedSpending = {}
    	categorizedSpending['Unknown']=0

    	for expense in bankExport:
    	    foundMatch=False
    	    for category in categoriesMapping:
    	        if(expense[0] in categoriesMapping[category] ):
    	            foundMatch=True
    	            if(category in categorizedSpending):
    	                categorizedSpending[category]+=expense[1]
    	            else:
    	                categorizedSpending[category]=expense[1]
    	    if(foundMatch==False):
    	        categorizedSpending['Unknown']+=expense[1]

    	##print(categorizedSpending)
        self.response.headers["Content-Type"] = "text/plain"
        self.response.write(categorizedSpending)

routes =[('/', MainPage)]


my_app = webapp2.WSGIApplication(routes, debug=True)