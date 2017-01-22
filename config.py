import os
basedir = os.path.abspath(os.path.dirname(__file__))

# GOOGLE_LOGIN_CLIENT_ID = b'793272902999-kafvrc1e3kbvgvgpooitdtqu56qm11ss.apps.googleusercontent.com'
# GOOGLE_LOGIN_CLIENT_SECRET = 'p-jgtnRZMBMCPeve2uComf7x'

GOOGLE_LOGIN_CLIENT_ID = "793272902999-kafvrc1e3kbvgvgpooitdtqu56qm11ss.apps.googleusercontent.com"
GOOGLE_LOGIN_CLIENT_SECRET = "p-jgtnRZMBMCPeve2uComf7x"

OAUTH_CREDENTIALS={
        'google': {
            'id': GOOGLE_LOGIN_CLIENT_ID,
            'secret': GOOGLE_LOGIN_CLIENT_SECRET
        }
}