from odoo import models, fields

class Client(models.Model):
    _name = 'client'
    _description = 'Client'
    _inherit = "owner"