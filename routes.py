import webapp2
from plaidIntegration import addBankAccount
import testDump
import Categorization


routes =[
	('/getAccessToken', addBankAccount.AddBankAccount),
	('/tester', testDump.testOktaCall),
	('/Categorization',Categorization.categorize)
	]


router = webapp2.WSGIApplication(routes, debug=True)