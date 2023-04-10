from odoo import fields, models
import http.client
import json

class IntegrationOrderTiki(models.Model):
    _name = "integration.order.tiki"


    def _confirm_order_dropping(self, id, payload):
        conn = http.client.HTTPSConnection("api.tiki.vn")
        data_conn = self.env['base.integrate.tiki'].sudo().search([])
        headers = {
            'Authorization': 'Bearer ' + data_conn.access_token,
            'Content-Type': 'application/json'
        }

        conn.request("POST", "/integration/v2/orders/"+id+"/dropship/confirm-available", payload, headers)
        res = conn.getresponse()

    def _confirm_order(self,id, payload):
        conn = http.client.HTTPSConnection("api.tiki.vn")
        data_conn = self.env['base.integrate.tiki'].sudo().search([])
        headers = {
            'Authorization': 'Bearer ' + data_conn.access_token,
            'Content-Type': 'application/json'
        }

        conn.request("POST", "/integration/v2/orders/" + id + "/confirm-available", payload, headers)
        res = conn.getresponse()