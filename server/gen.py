from .models import User
import bcrypt


def get_cookie_key(uuid):
    salt = bcrypt.gensalt()

    byte_uuid = bytes(str(uuid), 'utf-8')
    return bcrypt.hashpw(byte_uuid, salt)


def check_cookie(cookie_key):
    for i in User.objects.all:
        if bcrypt.checkpw(bytes(i.unique_id, 'utf-8'), bytes(cookie_key, 'utf-8')):
            return i
        continue
