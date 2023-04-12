import bcrypt
import pwinput

encoding = 'utf-8'

def hash_password(password):
    return bcrypt.hashpw(password.encode(encoding), bcrypt.gensalt()).decode(encoding)

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(encoding), hashed_password.encode(encoding))

def input_password(message):
    return pwinput.pwinput(prompt=message, mask='*')