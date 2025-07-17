from cryptography.fernet import Fernet
from django.conf import settings
import base64
import logging
import traceback

def encrypt(password):
    try:
        password = str(password)
        cipher_text = Fernet(settings.ENCRYPT_KEY)
        encrypted_pass = cipher_text.encrypt(password.encode('UTF-8'))
        encrypted_pass = base64.urlsafe_b64encode(encrypted_pass).decode('UTF-8')
        return encrypted_pass
    except Exception as e:
          logging.getLogger("error_logger").error(traceback.format_exc())
          return None
    

def decrypt(password):
    try:
          password = base64.urlsafe_b64decode(password)
          cipher_text = Fernet(settings.ENCRYPT_KEY)
          decrypted_password = cipher_text.decrypt(password).decode('UTF-8')
          return decrypted_password
    except Exception as e:
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None