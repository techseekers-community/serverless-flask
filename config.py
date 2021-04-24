import os

CONFIGURATION_SET = "email-config"
SECURITY_PASSWORD_SALT = "dsfdsfsgfgfg"
SECRET_KEY = 'my_precious'

SENDER = "er.nitikeshbhad@gmail.com"

EMAIL_CONFIRMATION_HTML = """
<p>Welcome! Thanks for signing up. Please follow this link to activate your account:</p>
<p><a href="{{ confirm_url }}">{{ confirm_url }}</a></p>
<br>
<p>Cheers!</p>
"""

EMAIL_CONFIRMATION_TEXT = """
Welcome! Thanks for signing up. Please follow this link to activate your account:
{{ confirm_url }}
Cheers!
"""

IS_OFFLINE = os.environ.get('IS_OFFLINE')
FRONTEND = 'http://www.apigatewaystage.co.in'
if IS_OFFLINE:
    FRONTEND = 'http://localhost:3000'
