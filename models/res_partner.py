from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_id = fields.Many2one('property')
    # price = fields.Float(compute='_compute_property_price')
    price = fields.Float(related='property_id.selling_price', store=True)

    @api.depends('property_id')
    def _compute_property_price(self):
        for rec in self:
            rec.price = rec.property_id.selling_price