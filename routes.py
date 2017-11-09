import webapp2
from plaidIntegration import getAccessToken
import testDump


routes =[
	('/getAccessToken', getAccessToken.MainPage),
	('/tester', testDump.testOktaCall)
	]


router = webapp2.WSGIApplication(routes, debug=True)