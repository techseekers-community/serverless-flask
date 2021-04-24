import re
from config import SECRET_KEY, SECURITY_PASSWORD_SALT
from itsdangerous import URLSafeTimedSerializer


def email_check(email):

    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

    if(re.search(regex, email)):
        return True
    else:
        return False


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    email = serializer.loads(
        token,
        salt=SECURITY_PASSWORD_SALT,
        max_age=expiration
    )
    return email
