#!coding:utf8
from hashlib import md5
import requests
from requests.exceptions import RequestException

class Geetest(object):
    """docstring for gt"""

    def __init__(self, app_id, app_key):
        self.CAPTCHA_ID = app_id
        self.PRIVATE_KEY = app_key
        self.PY_VERSION = '2.15.4.1.1'

    def register(self):
        api_reg_url = 'http://api.geetest.com/register.php?'
        reg_url = ''.join([api_reg_url, 'gt=', self.CAPTCHA_ID])
        result = None
        try:
            resp = requests.get(reg_url, timeout=2)
            if resp.status_code == requests.codes.ok:
                result = resp.text
        except RequestException:
            pass
        return result

    def validate(self, challenge, validate, seccode):
        api_validata_url = 'http://api.geetest.com/validate.php'
        if validate == self.md5value(''.join([self.PRIVATE_KEY, 'geetest', challenge])):
            params = {'seccode': seccode, 'sdk': ''.join(['python_', self.PY_VERSION])}
            resp = requests.post(api_validata_url, params)
            if resp.text == self.md5value(seccode):
                return True
        return False

    @staticmethod
    def md5value(value):
        if type(value) == str:
            value = value.encode()
        return md5(value).hexdigest()
