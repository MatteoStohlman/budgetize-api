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

PLAID_CLIENT_ID = "5929e9dd4e95b8036a672bde" #os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = "2af823a90ccec8e7ac1393c48ac302" #os.getenv('PLAID_SECRET')
PLAID_PUBLIC_KEY = "5dc31b6f8922727de6085b8cb5ddc7" #os.getenv('PLAID_PUBLIC_KEY')

class GetTransactions(webapp2.RequestHandler):
    def get(self):
        userId = self.request.get('userId')
        self.response.headers["Content-Type"] = "application/json"
        self.response.write(self.byUserId(userId))
    def fromLocal(self,userId):
        headers = {'Content-Type': 'application/json'}
        result = urlfetch.fetch(
            url='https://budget-master-reston.appspot.com/getTransactions?userId='+str(userId),
            method=urlfetch.GET,
            headers=headers)
        # print('Result')
        # print(result.content)
        return json.loads(result.content)

    def byUserId(self,userId):          
        query_getAuthUserId=""" SELECT plaid_access_token,plaid_institution_name
                                FROM budgetizer.plaid_access_tokens
                                WHERE user_id = %s"""
        resp_getAccessToken = rawQuery(query_getAuthUserId,(userId,))
        logging.debug(resp_getAccessToken)
        if(resp_getAccessToken and len(resp_getAccessToken)):
            collectedTransactions = []
            for accessToken in resp_getAccessToken:
                try:
                    newPayload = {};
                    newPayload['access_token']=accessToken[0]
                    newPayload['client_id']=PLAID_CLIENT_ID
                    newPayload['secret']=PLAID_SECRET
                    newPayload['start_date']='2017-01-01'
                    newPayload['end_date']='2017-10-31'
                    newPayload['options']={'count':500}
                    payload=json.dumps(newPayload)
                    headers = {'Content-Type': 'application/json'}
                    result = urlfetch.fetch(
                        url='https://sandbox.plaid.com/transactions/get',
                        payload=payload,
                        method=urlfetch.POST,
                        headers=headers)
                    if(json.loads(result.content)['transactions']):
                        collectedTransactions+=json.loads(result.content)['transactions']
                    # logging.debug(json.loads(result.content)['transactions'])
                except:
                    logging.exception('Caught Exception Fetching Transaction Data')
        else:
            logging.exception('No Data Returned')

        return {'transactions':collectedTransactions,'numberOfBanks':len(resp_getAccessToken)}
