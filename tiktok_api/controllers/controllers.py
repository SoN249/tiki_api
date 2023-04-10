# -*- coding: utf-8 -*-
# from odoo import http


# class TiktokApi(http.Controller):
#     @http.route('/tiktok_api/tiktok_api', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tiktok_api/tiktok_api/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tiktok_api.listing', {
#             'root': '/tiktok_api/tiktok_api',
#             'objects': http.request.env['tiktok_api.tiktok_api'].search([]),
#         })

#     @http.route('/tiktok_api/tiktok_api/objects/<model("tiktok_api.tiktok_api"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tiktok_api.object', {
#             'object': obj
#         })
