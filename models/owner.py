from odoo import models, fields

class Owner(models.Model):
    _name = 'owner'
    _description = "Owner"

    name = fields.Char(required=True, default='Owner')
    phone = fields.Char()
    address = fields.Char()
    property_ids = fields.One2many('property','owner_id')