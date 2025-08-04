from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    def do_something(self):
        print(self,'Inside do_something Method')
