import webapp2
from plaidIntegration import addBankAccount
from plaidIntegration.getTransactions import GetTransactions
import testDump
import Categorization


routes =[
	('/addBankAccount', addBankAccount.AddBankAccount),
	('/getTransactions',GetTransactions),
	('/tester', testDump.testOktaCall),
	('/Categorization',Categorization.categorizer)
	]


router = webapp2.WSGIApplication(routes, debug=True)