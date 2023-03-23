import http.client
from odoo import models, fields
import json


class TrackingTiki(models.Model):
    _name= "tracking.tiki"


    def _get_tracking_tiki(self, tracking):
        conn = http.client.HTTPSConnection("api.tiki.vn")
        payload = ''
        headers = {
          'tiki-api': '7a34ac38-a33e-4335-9e88-b80615ca624b'
        }
        conn.request("GET", "/integration/v2/tracking/"+tracking, payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8").replace("'", '"')
        res_json = json.loads(data)
        return res_json