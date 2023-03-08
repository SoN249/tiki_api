from odoo import fields, models
import logging
import http.client
import base64
import json

logging.captureWarnings(True)


class ResConfigSetting(models.TransientModel):
    _inherit = "res.config.settings"

    client_id = fields.Char('Client ID', config_parameter="tiki_api.client_id")
    client_secret = fields.Char('Client Secret', config_parameter="tiki_api.client_secret")

    def btn_get_token(self):
        conn = http.client.HTTPSConnection("api.tiki.vn")
        payload = 'grant_type=client_credentials'

        data_auth = (self.client_id + ":" + self.client_secret).encode()
        authorization_byte = base64.b64encode(data_auth)
        authorization_string = authorization_byte.decode('ascii')

        headers = {
            'Authorization': 'Basic ' + authorization_string,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        conn.request("POST", "/sc/oauth2/token", payload, headers)
        res = conn.getresponse()

        response = res.read().decode("utf-8").replace("'", '"')
        res_json = json.loads(response)
        data = json.dumps(res_json, indent=4, sort_keys=True)



class BaseItegrateTiki(models.Model):
    _name = 'base.itegrate.tiki'

    access_token = fields.Char(string='access_token')
    expires_in = fields.Char('time_exp')
    scope = fields.Char('scope')
