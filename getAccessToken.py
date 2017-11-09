import webapp2
import dbConnectExample
import logging
from plaid import Client
import json
from requests_toolbelt.adapters import appengine
appengine.monkeypatch()
import ssl
from google.appengine.api import urlfetch


class MainPage(webapp2.RequestHandler):
	PLAID_CLIENT_ID = "5929e9dd4e95b8036a672bde" #os.getenv('PLAID_CLIENT_ID')
	PLAID_SECRET = "2af823a90ccec8e7ac1393c48ac302" #os.getenv('PLAID_SECRET')
	PLAID_PUBLIC_KEY = "5dc31b6f8922727de6085b8cb5ddc7" #os.getenv('PLAID_PUBLIC_KEY')
	access_token = None
	public_token = None
	def get(self):          

		self.response.headers["Content-Type"] = "text/plain"
		self.response.write("test")

	def post(self):
		jsonstring = self.request.body
		jsonobject = json.loads(jsonstring)
		jsonobject['client_id']=self.PLAID_CLIENT_ID
		jsonobject['secret']=self.PLAID_SECRET
		public_token = jsonobject['public_token']
		payload = json.dumps(jsonobject)
		logging.debug(payload)
		access_token='test'
		institution = self.request.get("institution")
		self.response.headers["Content-Type"] = "application/json"
		self.response.headers['Access-Control-Allow-Origin']='*'
		try:
			form_data = jsonobject
			headers = {'Content-Type': 'application/json'}
			result = urlfetch.fetch(
				url='https://sandbox.plaid.com/item/public_token/exchange',
				payload=payload,
				method=urlfetch.POST,
				headers=headers)
			self.response.write(result.content)
		except urlfetch.Error:
			logging.exception('Caught exception fetching Access Token')
		try:
			newPayload = {};
			accessTokenResponse = json.loads(result.content)
			accessToken = accessTokenResponse['access_token']
			logging.debug(accessToken)
			newPayload['access_token']=accessToken
			newPayload['client_id']=self.PLAID_CLIENT_ID
			newPayload['secret']=self.PLAID_SECRET
			newPayload['start_date']='2017-01-01'
			newPayload['end_date']='2017-10-31'
			newPayload['options']={'count':250,'offset':100}
			payload=json.dumps(newPayload)
			headers = {'Content-Type': 'application/json'}
			result = urlfetch.fetch(
				url='https://sandbox.plaid.com/transactions/get',
				payload=payload,
				method=urlfetch.POST,
				headers=headers)
			self.response.write(result.content)
			# logging.debug(json.loads(result.content)['transactions'])
		except:
			logging.exception('Caught Exception Fetching Transaction Data')
		# client = Client(client_id=self.PLAID_CLIENT_ID, secret=self.PLAID_SECRET, public_key=self.PLAID_PUBLIC_KEY, environment='sandbox')
		# response = client.Item.public_token.exchange(public_token)
		# access_token = response['access_token']

		# self.response.headers["Content-Type"] = "application/json"
		# self.response.write(access_token)
	def decorateHeaders(self):
		"""Decorates headers for the current request."""
		self.response.headers.add_header('Access-Control-Allow-Origin', '*')
		self.response.headers.add_header('Access-Control-Allow-Headers', 'Content-Type, Accept')
		self.response.headers.add_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')

	def options(self):
		"""Default OPTIONS handler for the entire app."""
		self.decorateHeaders()
# routes =[('/getAccessToken', MainPage)]


# my_app = webapp2.WSGIApplication(routes, debug=True)