from flask import url_for, current_app, redirect, request
from rauth import OAuth2Service

import simplejson as json
import urllib


GOOGLE_LOGIN_CLIENT_ID = "793272902999-kafvrc1e3kbvgvgpooitdtqu56qm11ss.apps.googleusercontent.com"
GOOGLE_LOGIN_CLIENT_SECRET = "p-jgtnRZMBMCPeve2uComf7x"

OAUTH_CREDENTIALS={
        'google': {
            'id': GOOGLE_LOGIN_CLIENT_ID,
            'secret': GOOGLE_LOGIN_CLIENT_SECRET
        }
}

class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        # print(url_for('oauth_callback', provider=self.provider_name,
        #                 _external=True))
        return url_for('oauth_callback', provider=self.provider_name,
                        _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers={}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]

class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        googleinfo = urllib.request.urlopen('https://accounts.google.com/.well-known/openid-configuration')
        str_response = googleinfo.read().decode('utf-8')
        google_params = json.loads(str_response)
        # google_params = json.load(googleinfo)
        self.service = OAuth2Service(
                name='google',
                client_id=self.consumer_id,
                client_secret=self.consumer_secret,
                authorize_url=google_params.get('authorization_endpoint'),
                base_url=google_params.get('userinfo_endpoint'),
                access_token_url=google_params.get('token_endpoint')
        )

    def authorize(self):
        # print(self.get_callback_url())
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
            )

    def callback(self):
        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
                data={'code': request.args['code'],
                      'grant_type': 'authorization_code',
                      'redirect_uri': self.get_callback_url()
                     },
                decoder = json.loads
        )
        me = oauth_session.get('').json()
        print("me = oauth_session.get('').json()", me)
        print("CODE:", request.args['code'])
        return (me['name'],
                me['email'], request.args['code'], me['picture'])
