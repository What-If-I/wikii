import hmac
import random
from string import letters
import unicodedata


_secret = "8e892d6fd453739121d8806f212ad3e5"


def make_salt():
    return "".join(random.choice(letters) for _ in xrange(5))


def make_hash(hash_args, return_value="", salt="", secret=False):
    hash_args_string = "".join(hash_args).encode()

    if secret:
        hash_args_string += _secret

    if salt:
        hash_str = hmac.new(hash_args_string, salt).hexdigest()
    else:
        salt = make_salt()
        hash_str = hmac.new(hash_args_string, salt).hexdigest()

    if return_value:
        return '%s|%s~%s' % (return_value, hash_str, salt)

    return '%s~%s' % (hash_str, salt)


def valid_hash(hash_values, hash_str, secret=False):
    salt = hash_str.split("~")[-1]
    if make_hash(hash_values, salt=salt, secret=secret) == hash_str:
        return True


def valid_user_cookie(cookie):
    try:
        user_id, hash_string = cookie.split("|")[0:2]
    except:
        return False
    if valid_hash(user_id, hash_string, secret=True):
        return True
