import json
from google.appengine.api import urlfetch

def validateAccessToken(oktaAccessToken=False):
	if(oktaAccessToken):
		token=oktaAccessToken
		token_type_hint="access_token"
		client_id="0oacqlu6f2SNDYwf00h7"
		baseUrl="https://dev-481660.oktapreview.com/oauth2/default/v1/introspect"
		tokenType_urlComponent="token_type_hint="+token_type_hint
		token_urlComponent="token="+token
		clientId_urlComponent='client_id='+client_id
		composedUrl = baseUrl+"?"+tokenType_urlComponent+"&"+token_urlComponent+'&'+clientId_urlComponent
		result = urlfetch.fetch(
			url=composedUrl,
			method=urlfetch.POST,
			headers={'Content-Type':'application/x-www-form-urlencoded','Accept':'application/json'})
		return result.content
	else:
		return {'status':False}