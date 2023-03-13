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
    tiki_api = fields.Char('Tiki API', config_parameter="tiki_api.tiki_api")

    def btn_get_token(self):

        if self.client_id and self.client_secret:
            conn = http.client.HTTPSConnection("api.tiki.vn")
            payload = 'grant_type=client_credentials'
            data = (self.client_id + ":" + self.client_secret).encode()
            authorization_byte = base64.b64encode(data)
            authorization_string = authorization_byte.decode('ascii')
            headers = {
                'Authorization': 'Basic ' + authorization_string,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            conn.request("POST", "/sc/oauth2/token", payload, headers)
            res = conn.getresponse()
            if res.status == 200:
                response = res.read().decode("utf-8").replace("'", '"')
                res_json = json.loads(response)
                self.env['base.integrate.tiki'].sudo().search([]).unlink()
                self.env['base.integrate.tiki'].sudo().create({
                    'access_token': res_json['access_token'],
                    'expires_in': res_json['expires_in'],
                    'scope': res_json['scope'],
                    'tiki_api': self.tiki_api
                })
                message = "Kết nối thành công"
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'message': message,
                        'type': 'success',
                        'sticky': False
                    }
                }
            else:
                conn2 = http.client.HTTPSConnection("api.tiki.vn")
                payload_body = 'grant_type=client_credentials&client_id=' + self.client_id + '&client_secret=' + self.client_secret
                header_body = {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                conn2.request("POST", "/sc/oauth2/token", payload_body, header_body)
                res = conn2.getresponse()

                if res.status == 200:
                    response = res.read().decode("utf-8").replace("'", '"')
                    res_json = json.loads(response)
                    self.env['base.integrate.tiki'].sudo().search([]).unlink()
                    self.env['base.integrate.tiki'].sudo().create({
                        'access_token': res_json['access_token'],
                        'expires_in': res_json['expires_in'],
                        'scope': res_json['scope'],
                        'tiki_api': self.tiki_api
                    })
                    message = "Kết nối thành công"
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'message': message,
                            'type': 'success',
                            'sticky': False
                        }
                    }
                else:
                    message = "Kết nối thất bại"
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'message': message,
                            'type': 'error',
                            'sticky': False
                        }
                    }


    def btn_sync_data_tiki(self):
        self.env['categories.tiki'].get_categories_tiktok()
        self.env['warehouses.tiki'].get_warehouses_tiki()


class BaseItegrateTiki(models.Model):
    _name = 'base.integrate.tiki'

    access_token = fields.Char(string='access_token')
    expires_in = fields.Char('time_exp')
    scope = fields.Char('scope')
    tiki_api = fields.Char('tiki_api')
