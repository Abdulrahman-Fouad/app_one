from odoo import models, fields, api


class Tag(models.Model):
    _name = 'tag'
    _description = ""

    name = fields.Char(required=1, default='Tag')