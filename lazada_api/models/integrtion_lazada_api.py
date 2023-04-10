from odoo import fields, models
import requests
import datetime
import hmac
import hashlib
import json
import urllib.parse


class IntegrateLazada(models.Model):
    _name = 'integrate.lazada'

    def create_signature(self, secret, api, parameters):
        sort_dict = sorted(parameters)
        parameters_str = "%s%s" % (api,str().join('%s%s' % (key, parameters[key]) for key in sort_dict))
        h = hmac.new(secret.encode(encoding="utf-8"), parameters_str.encode(encoding="utf-8"), digestmod=hashlib.sha256)
        return h.hexdigest().upper()

    def _create_product_api(self, payload):
        now = datetime.datetime.utcnow()
        timestamp = round(now.timestamp() * 1000)

        parameters = json.loads(self.env['base.integrate.lazada'].sudo().search([]).parameters.replace("\'", "\""))
        parameters.update({"timestamp": timestamp, "payload": payload})

        app_secret = self.env['res.config.settings'].sudo().search([])[-1].app_secret
        api = "/product/create"
        sign = self.create_signature(app_secret, api, parameters)

        endpoint = "https://api.lazada.vn/rest"
        headers = {}
        payload_url = urllib.parse.quote_plus(str(payload))

        url = endpoint + api + "?payload=" + payload_url + "&app_key=" + parameters['app_key'] + "&sign_method=" + parameters['sign_method'] + "&access_token=" + parameters["access_token"] + "&sign=" + sign + "&timestamp=" + str(timestamp)
        response = requests.request("POST", url, headers=headers, data={})
        return response.json()

    def request_category_tree(self):
        now = datetime.datetime.utcnow()
        timestamp = round(now.timestamp() * 1000)
        language_code = "vi_VN"
        parameters = json.loads(self.env['base.integrate.lazada'].sudo().search([]).parameters.replace("\'", "\""))
        parameters.update({"timestamp": timestamp, "language_code": language_code})

        app_secret = self.env['res.config.settings'].sudo().search([])[-1].app_secret
        api = "/category/tree/get"
        sign = self.create_signature(app_secret, api, parameters)
        url = "https://api.lazada.vn/rest"+api+"?language_code="+language_code+ "&app_key=" + parameters['app_key'] + "&sign_method=" + parameters['sign_method'] + "&access_token=" + parameters["access_token"] + "&sign=" + sign + "&timestamp=" + str(timestamp)

        headers = {}
        response = requests.request("GET", url, headers=headers, data={})
        return response.json()

