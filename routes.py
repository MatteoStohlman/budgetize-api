import webapp2
from plaidIntegration import getAccessToken
import testDump
import Categorization


routes =[
	('/getAccessToken', getAccessToken.MainPage),
	('/tester', testDump.testOktaCall),
	('/Categorization',Categorization.categorize)
	]


router = webapp2.WSGIApplication(routes, debug=True)