from odoo import fields, models
import requests
import json
import calendar
import time
import hmac
import hashlib

class IntergrateTiktok(models.Model):
    _name="integrate.tiktok"

    token = fields.Char(string="Token")

    def get_token_tiktok(self):
        ir_config = self.env['ir.config_parameter'].sudo()
        app_key = ir_config.get_param('tiktok.app.key', '')
        auth_code = ir_config.get_param('tiktok.auth.key', '')
        app_secret = ir_config.get_param('tiktok.app.secret', '')
        url = 'https://auth-sandbox.tiktok-shops.com/api/v2/token/get?app_key=' + app_key + '&auth_code=' + auth_code + '&app_secret=' + app_secret + '&grant_type=authorized_code'
        req = requests.get(url).json()
        if req['code'] == 0:
            search_token = self.sudo().search([('token','!=',None)])
            if not search_token:
                self.env['integrate.tiktok'].sudo().create({
                    'token': req['data']['access_token'],
                })
            else:
                search_token.sudo().write({
                    'token': req['data']['access_token']
                })
            access_token = req['data']['access_token']
        else:
            access_token = self.sudo().search([]).token
        return access_token

    def get_sign_tiktok(self, url_api, time_stamp, parameter=None):
        if parameter is None:
            parameter = {}
        ir_config = self.env['ir.config_parameter'].sudo()
        # secret = ir_config.get_param('tiktok.app.secret', '')
        # app_key = ir_config.get_param('tiktok.app.key', '')
        secret = "4636a2640848f83f03d01af1c76f63d462a593cd"
        app_key="66hhd4nrhfrbi"

        parameters = {"app_key": app_key, "timestamp": time_stamp}
        parameters.update(parameter)
        sort_dict = sorted(parameters)

        parameters_str = "%s%s" % (url_api, str().join('%s%s' % (key, parameters[key]) for key in sort_dict))
        signstring = secret + parameters_str + secret

        sign = hmac.new(secret.encode("utf-8"), signstring.encode("utf-8"), hashlib.sha256).hexdigest()
        return sign

    def _post_data_tiktok(self, api, payload=None, files=None, params={}, headers=None):
        if headers is None:
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Odoo'
            }
        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)

        sign = self.get_sign_tiktok(api,time_stamp)
        data = payload or dict()

        params= {"app_key":"66hhd4nrhfrbi",
                 "access_token":"ROW_WNcXYQAAAADJX2Km_KOCQQDOMgrrpf5bKEQyx1a8mQw6IUMUrghtJ0rWmhHjNEluIf_jidDHlU-JEWmWisAq6qMkxbJOl-lBdkWqsuqhsxmpIsIvKs2JLw",
                 "sign":sign,
                 "timestamp":time_stamp,
                 }
        url = "https://open-api-sandbox.tiktokglobalshop.com"+api
        res = requests.post(
            url,
            data=data,
            params=params,
            files=files,
            headers=headers,
            verify=False
        )
        if res.status_code == 200:
            return res.text

    def _get_data_tiktok(self, api, payload=None, files=None, param=None, headers=None):
        if param is None:
            param = {}
        if headers is None:
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Odoo'
            }
        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)

        sign = self.get_sign_tiktok(api, time_stamp, parameter=param)
        data = payload or dict()
        data = data or dict()
        params = {"app_key": "66hhd4nrhfrbi",
                  "access_token": "ROW_WNcXYQAAAADJX2Km_KOCQQDOMgrrpf5bKEQyx1a8mQw6IUMUrghtJ0rWmhHjNEluIf_jidDHlU-JEWmWisAq6qMkxbJOl-lBdkWqsuqhsxmpIsIvKs2JLw",
                  "sign": sign,
                  "timestamp": time_stamp,
                  }
        params.update(param)

        url = "https://open-api-sandbox.tiktokglobalshop.com" + api
        res = requests.get(
            url,
            data=data,
            params=params,
            files=files,
            headers=headers,
            verify=False
        )
        if res.status_code == 200:
             return res.text