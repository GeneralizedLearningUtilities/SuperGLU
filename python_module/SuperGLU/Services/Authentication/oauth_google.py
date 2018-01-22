# -*- coding: utf-8 -*-
import types

from SuperGLU.Util.PythonDirectLibs.flask_oauth_fork.flask_oauth import OAuth

GOOGLE_AUTHENTICATION = None
GOOGLE_CLIENT_ID = None
GOOGLE_CLIENT_SECRET = None

oauth = OAuth()

#Simple helper for getting user info - will be added dynamically to
#our google object
def _getUserInfo(self):
    return self.get('https://www.googleapis.com/oauth2/v1/userinfo')

def makeGoogleOAuth(client=GOOGLE_CLIENT_ID, secret=GOOGLE_CLIENT_SECRET):
    
    token_params = {
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'response_type': 'code',
    }

    google = oauth.remote_app(
        'google',
        base_url='https://www.google.com/accounts/',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        request_token_url=None,
        request_token_params=token_params,
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_method='POST',
        access_token_params={'grant_type': 'authorization_code'},
        bearer_authorization_header=True,
        consumer_key=client,
        consumer_secret=secret
    )
    
    #Since we bind per-instance (and not per-class), we need to handy
    #types library
    google.getUserInfo = types.MethodType(_getUserInfo, google)
    
    return google

def getGoogleOAuth():
    global GOOGLE_AUTHENTICATION
    if GOOGLE_AUTHENTICATION is None:
        GOOGLE_AUTHENTICATION = makeGoogleOAuth()
    return GOOGLE_AUTHENTICATION

if __name__ == "__main__":
    setGoogleOAuth()
