from odoo import models, fields, api


class Building(models.Model):
    _name = 'building'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Building"
    # _rec_name = 'code'

    name = fields.Char()
    no= fields.Integer()
    code = fields.Char()
    description = fields.Text()
    active = fields.Boolean(default= True)