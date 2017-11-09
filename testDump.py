import webapp2
# from plaid import Client
from oktaIntegration.validateAccessToken import validateAccessToken

# PLAID_CLIENT_ID = "5929e9dd4e95b8036a672bde" #os.getenv('PLAID_CLIENT_ID')
# PLAID_SECRET = "2af823a90ccec8e7ac1393c48ac302" #os.getenv('PLAID_SECRET')
# PLAID_PUBLIC_KEY = "5dc31b6f8922727de6085b8cb5ddc7" #os.getenv('PLAID_PUBLIC_KEY')

# client = Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET, public_key=PLAID_PUBLIC_KEY, environment='sandbox')

# response = client.Transactions.get(access_token, start_date='2017-10-01', end_date='2017-10-25')
# transactions = response['transactions']

# # the transactions in the response are paginated, so make multiple calls while increasing the offset to
# # retrieve all transactions
# while len(transactions) < response['total_transactions']:
#     response = client.Transactions.get(access_token, start_date='2016-07-12', end_date='2017-01-09',
#                                        offset=len(transactions)
#                                       )
#     transactions.extend(response['transactions'])

# class MainPage(webapp2.RequestHandler):

#     def get(self):
#         self.response.headers["Content-Type"] = "text/plain"
#         self.response.write(transactions)

class testOktaCall(webapp2.RequestHandler):

    def get(self):
    	self.response.headers["Content-Type"] = "text/plain"
        self.response.write(validateAccessToken())

