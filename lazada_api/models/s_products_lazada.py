from odoo import fields,models,api
from odoo.exceptions import ValidationError

class SProductLazada(models.Model):
    _inherit = ['product.template']

    package_height = fields.Float('Chiều cao (cm)')
    package_length = fields.Float('Chiều dai (cm)')
    package_width = fields.Float('Chiều rộng (cm)')
    package_weight = fields.Float('Trọng lượng')
    check_sync_product = fields.Boolean('Check sync', default=False, readonly=True)

    @api.onchange('attribute_line_ids')
    def _check_attribute_id(self):
        if len(self.attribute_line_ids.attribute_id) > 2:
            raise ValidationError("Not more than 2 attribute")

    def variation_custions(self):
        if self.attribute_line_ids:
            variation_name = self.attribute_line_ids.attribute_id.mapped('name')
            variation =  {"variation1":{"name": variation_name[0],
                               "hasImage": "True",
                               "customize": "True",
                               "options": {
                                   "option": [
                                   ]
                                 }}
                          }
            for name in self.attribute_line_ids[0].value_ids.mapped("name"):
                variation['variation1']['options']['option'].append(name)

            if len(self.attribute_line_ids) == 2:
                variation2 = {"name": variation_name[1],
                              "hasImage": "False",
                              "customize": "True",
                              "options": {
                                  "option": [

                                  ]
                              }}
                for name in self.attribute_line_ids[1].value_ids.mapped("name"):
                    variation2['options']['option'].append(name)

                variation.update({"variation2": variation2})
                return variation
        else:
            return False

        #
    def sku_product(self):
        Skus = {"Sku": []}
        variation_name = self.attribute_line_ids.attribute_id.mapped('name')
        if len(self.attribute_line_ids) == 0 or len(self.product_variant_ids) == 1:
            Skus["Sku"].append({
                "SellerSku": self.default_code,
                "saleProp": {},
                "quantity": "3",
                "price": str(self.lst_price),
                "package_height": str(self.package_height),
                "package_length": str(self.package_length),
                "package_width": str(self.package_width),
                "package_weight": str(self.package_weight),
                "Images": {
                    "Image": [
                        "https://vn-live-02.slatic.net/p/10e05aa7f00447dcfb3814d439100b08.jpg"
                    ]
                }
            })

            if len(self.attribute_line_ids) == 2:
                Skus["Sku"]["saleProp"].update({variation_name[0]: self.attribute_line_ids[0].value_ids.name,variation_name[1]: self.attribute_line_ids[2].value_ids.name})
            elif len(self.attribute_line_ids) == 1:
                Skus["Sku"]["saleProp"].update({variation_name[0]: self.attribute_line_ids[0].value_ids.name})
        else:
                for r in range(len(self.product_variant_ids)):
                        for value in self.product_variant_ids[r]:
                            Skus['Sku'].append({
                                "SellerSku": value.default_code,
                                "saleProp": {
                                    variation_name[0]: value.product_template_variant_value_ids[0].name
                                },
                                "quantity": "3",
                                "price": str(value.lst_price),
                                "package_height": str(self.package_height),
                                "package_length": str(self.package_length),
                                "package_width": str(self.package_width),
                                "package_weight": str(self.package_weight),
                                "Images": {
                                    "Image": [
                                        "https://vn-live-02.slatic.net/p/10e05aa7f00447dcfb3814d439100b08.jpg"
                                    ]
                                }
                            })
                            if len(self.attribute_line_ids) == 2:
                                Skus['Sku'][r]["saleProp"].update(
                                    {variation_name[1]: value.product_template_variant_value_ids[1].name})

        return Skus


    def btn_create_product_lazada(self):
        payload = {
                "Request": {
                    "Product": {
                    "PrimaryCategory": self.categ_id.category_lazada_id,
                    "AssociatedSku":"Existing SKU in seller center",
                    "Images": {
                        "Image": [
                        "https://vn-live-02.slatic.net/p/10e05aa7f00447dcfb3814d439100b08.jpg"
                        ]
                    },
                    "Attributes": {
                        "propCascade": {
                            "26": "120013644:162,100006867:160387"
                                },
                        "name": self.name,
                        "description": "" ,
                        "brand_id":"4",
                        "warranty_type": 'Local Manufacturer Warranty',
                        "warranty": "1 Month",
                        "model": "test",
                        "delivery_option_sof": "No"
                    }
                    }
                }
             }
        if self.description != False:
            payload['Request']['Product']['Attributes'].update({'description': self.description})

        variation = self.variation_custions()
        sku = self.sku_product()
        payload['Request']['Product'].update({"Skus":sku})
        if variation != False:
            payload['Request']['Product'].update({"variation": variation})
        response = self.env['integrate.lazada']._create_product_api(payload)
        if 'message' in response:
            raise ValidationError(response['message'])