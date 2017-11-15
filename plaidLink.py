import webapp2
import dbConnectExample
import logging
#from plaid import Client


class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers["Content-Type"] = "text/html"
        self.response.write("""
              <button id="link-button">Link Account</button>

              <script src="https://cdn.plaid.com/link/v2/stable/link-initialize.js"></script>
              <script type="text/javascript">
              var handler = Plaid.create({
                clientName: 'Plaid Walkthrough Demo',
                env: 'sandbox',
                key: '[PUBLIC_KEY]', // Replace with your public_key to test with live credentials
                product: ['auth', 'transactions'],
                webhook: '[WEBHOOK_URL]', // Optional – use webhooks to get transaction and error updates
                selectAccount: false, // Optional – trigger the Select Account
                onLoad: function() {
                  // Optional, called when Link loads
                },
                onSuccess: function(public_token, metadata) {
                  // Send the public_token to your app server.
                  // The metadata object contains info about the institution the
                  // user selected and the account ID, if `selectAccount` is enabled.
                  $.post('/get_access_token', {
                    public_token: public_token,
                  });
                },
                onExit: function(err, metadata) {
                  // The user exited the Link flow.
                  if (err != null) {
                    // The user encountered a Plaid API error prior to exiting.
                  }
                  // metadata contains information about the institution
                  // that the user selected and the most recent API request IDs.
                  // Storing this information can be helpful for support.
                }
              });

              $('#link-button').on('click', function(e) {
                handler.open();
                // Alternatively, you can have a specific institution
                // prompt for authentication. Example:
                //
                // handler.open('ins_100000');
                //
                // This will open Link with Union Bank as the institution.
              });
              </script>
          """)

routes =[('/', MainPage)]


my_app = webapp2.WSGIApplication(routes, debug=True)


