# -*- coding: utf-8 -*-
# from odoo import http


# class TikiApi(http.Controller):
#     @http.route('/tiki_api/tiki_api', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tiki_api/tiki_api/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tiki_api.listing', {
#             'root': '/tiki_api/tiki_api',
#             'objects': http.request.env['tiki_api.tiki_api'].search([]),
#         })

#     @http.route('/tiki_api/tiki_api/objects/<model("tiki_api.tiki_api"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tiki_api.object', {
#             'object': obj
#         })
