from odoo import fields, models
from odoo.exceptions import ValidationError
import datetime
import requests

class ResConfigSettingLazada(models.TransientModel):
    _inherit = "res.config.settings"

    app_key= fields.Char("App key", config_parameter="lazada_api.app_key")
    app_secret = fields.Char("App secret",config_parameter="lazada_api.app_secret")
    auth_code = fields.Char("Auth code", config_parameter="lazada_api.auth_code")

    def btn_get_auth(self):
        if self.app_key:
            url = "https://auth.lazada.com/oauth/authorize?response_type=code&force_auth=true&redirect_uri=https://www.lazada.vn&client_id="+self.app_key
            return {
                'name': 'Authorization',
                'type': 'ir.actions.act_url',
                'url': url,  # Replace this with tracking link
                'target': 'new',  # you can change target to current, self, new.. etc
            }
        else:
            raise ValidationError("Invalid Client ID")

    def btn_access_token(self):

        now = datetime.datetime.utcnow()
        timestamp = str(round(now.timestamp() * 1000))
        sign_method = "sha256"
        api = "/auth/token/create"
        parameters ={"app_key":self.app_key,"timestamp":timestamp,"code":self.auth_code, "sign_method":sign_method}
        sign = self.env['integrate.lazada'].create_signature(self.app_secret,api,parameters)
        endpoint = "https://auth.lazada.com/rest"

        url = endpoint + api + "?app_key="+self.app_key+"&sign_method=sha256&sign="+sign+"&code="+self.auth_code+"&timestamp="+timestamp

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            try:
                data = response.json()
                token_test = "50000201832wabsatvjXbbPfpztgmHKl4DVS9fyCsRbK137903b4wxRusAY4y8we"
                self.env['base.integrate.lazada'].sudo().search([]).unlink()
                self.env['base.integrate.lazada'].sudo().create({
                    'access_token': data['access_token'],
                    'refresh_token': data['refresh_token'],
                    'parameters':{"app_key":self.app_key,"sign_method":sign_method,"access_token":token_test,"timestamp":timestamp}
                })
            except:
                raise ValidationError('Kết nối thất bại')
    def sync_data(self):
        self.env['product.category'].category_lazada()

class BaseIntegrateLazada(models.Model):
    _name = 'base.integrate.lazada'

    access_token = fields.Char(string='Access token')
    refresh_token = fields.Char('Refresh Token')
    parameters = fields.Text("Parameters")

