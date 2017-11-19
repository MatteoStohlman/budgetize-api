import webapp2
import dbConnectExample
import logging
#from plaid import Client
import json
#from requests_toolbelt.adapters import appengine
#appengine.monkeypatch()
import ssl
from google.appengine.api import urlfetch
from oktaIntegration.validateAccessToken import validateAccessToken
from database.rawQuery import rawQuery

class AddBankAccount(webapp2.RequestHandler):
    PLAID_CLIENT_ID = "5929e9dd4e95b8036a672bde" #os.getenv('PLAID_CLIENT_ID')
    PLAID_SECRET = "2af823a90ccec8e7ac1393c48ac302" #os.getenv('PLAID_SECRET')
    PLAID_PUBLIC_KEY = "5dc31b6f8922727de6085b8cb5ddc7" #os.getenv('PLAID_PUBLIC_KEY')
    def get(self):          

        self.response.headers["Content-Type"] = "text/plain"
        self.response.write("test")

    def post(self):
        oktaAccessToken = self.request.headers['Authorization']
        validationResult = validateAccessToken(oktaAccessToken)
        if(json.loads(validationResult)['active']):
            authUserEmail=json.loads(validationResult)['username']
            query_getAuthUserId=""" SELECT id 
                                    FROM budgetizer.users
                                    WHERE email = %s"""
            resp_getAuthUserId = rawQuery(query_getAuthUserId,(authUserEmail,))
            if(len(resp_getAuthUserId)):
                userId=resp_getAuthUserId[0][0]
                incomingPayload = json.loads(self.request.body)
                logging.debug(incomingPayload)

                
                publicToken = incomingPayload['public_token']
                accounts=incomingPayload['accounts']
                institutionName=incomingPayload['institution']['name']
                institutionId=incomingPayload['institution']['institution_id']
                linkSessionId=incomingPayload['link_session_id']
                
                outgoingPayload={}
                outgoingPayload['public_token']=publicToken
                outgoingPayload['client_id']=self.PLAID_CLIENT_ID
                outgoingPayload['secret']=self.PLAID_SECRET
                outgoingPayload=json.dumps(outgoingPayload)
                logging.debug(outgoingPayload)

                self.response.headers["Content-Type"] = "application/json"
                self.response.headers['Access-Control-Allow-Origin']='*'
                try:
                    # form_data = outgoingPayload
                    headers = {'Content-Type': 'application/json'}
                    result = urlfetch.fetch(
                        url='https://sandbox.plaid.com/item/public_token/exchange',
                        payload=outgoingPayload,
                        method=urlfetch.POST,
                        headers=headers)
                    self.response.write(result.content)
                    newPayload = {};
                    accessTokenResponse = json.loads(result.content)
                    accessToken = accessTokenResponse['access_token']
                    itemId = accessTokenResponse['item_id']
                    logging.debug(accessToken)
                    query = """ INSERT INTO budgetizer.plaid_access_tokens 
                                (plaid_access_token,plaid_item_id,user_id,plaid_institution_name,plaid_institution_id,plaid_link_session_id) 
                                VALUES (%s,%s,%s,%s,%s,%s);"""
                    params=(accessToken,itemId,userId,institutionName,institutionId,linkSessionId)
                    logging.debug(params)
                    rawQuery(query,params)
                    
                except:
                    logging.exception('Caught Exception Fetching f')
            else:
                self.response.write('No User Found in Budgetizer')
        else:
            self.response.write('No User Found at Okta')


        # client = Client(client_id=self.PLAID_CLIENT_ID, secret=self.PLAID_SECRET, public_key=self.PLAID_PUBLIC_KEY, environment='sandbox')
        # response = client.Item.public_token.exchange(public_token)
        # access_token = response['access_token']

        # self.response.headers["Content-Type"] = "application/json"
        # self.response.write(access_token)
    def decorateHeaders(self):
        """Decorates headers for the current request."""
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers.add_header('Access-Control-Allow-Headers', 'Content-Type, Accept, Authorization')
        self.response.headers.add_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')

    def options(self):
        """Default OPTIONS handler for the entire app."""
        self.decorateHeaders()
# routes =[('/getAccessToken', MainPage)]


# my_app = webapp2.WSGIApplication(routes, debug=True)