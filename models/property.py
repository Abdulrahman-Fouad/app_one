from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Property"

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed')
    ], default="draft", tracking=1)

    ref = fields.Char(default='New', readonly= 1)
    name = fields.Char(required=1, default='New', tracking=1)

    postcode = fields.Char(required=1, tracking=1)
    date_availability = fields.Date(default=fields.date.today(), tracking=1)
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean(tracking=1)
    expected_price = fields.Float(tracking=1)
    selling_price = fields.Float(tracking=1)
    active = fields.Boolean(default=True)
    diff = fields.Float(compute='_compute_diff', tracking=1)
    bedrooms = fields.Integer(required=1, tracking=1)
    living_area = fields.Integer(tracking=1)
    facades = fields.Integer(tracking=1)
    garage = fields.Boolean(tracking=1)
    garden = fields.Boolean(tracking=1)
    garden_area = fields.Integer(tracking=1)
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], tracking=1)
    tag_ids = fields.Many2many('tag', tracking=1)

    description = fields.Text(tracking=1)

    owner_id = fields.Many2one('owner', tracking=1)
    owner_address = fields.Char(related="owner_id.address", tracking=1)
    owner_phone = fields.Char(related="owner_id.phone", tracking=1)

    line_ids = fields.One2many('property.line', 'property_id', tracking=1)

    # owner_address_compute = fields.Char(compute = '_compute_owner_address')
    # owner_phone_compute = fields.Char(compute = '_compute_owner_phone')

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'The property name already taken')
    ]

    @api.constrains('bedrooms')
    def _non_zero_bedrooms_checker(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError('Please add a valid number of berdooms !')

    @api.constrains('living_area')
    def _non_zero_living_area_checker(self):
        for rec in self:
            if rec.living_area == 0:
                raise ValidationError('Please add a valid value for living area !')

    @api.constrains('garden_area')
    def _non_zero_garden_area_checker(self):
        for rec in self:
            if rec.garden:
                if rec.garden_area == 0:
                    raise ValidationError('Please add a valid value for garden area !')

    def create_history_record(self,old_state, new_state, reason = ""):
        for rec in self:
            rec.env['property.history'].create({
                'user_id': rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason,
                'line_ids': [(0, 0, {'description':line.description, 'area':line.area})for line in rec.line_ids],
            })




    def action_draft(self):
        for rec in self:
            rec.create_history_record(rec.state, 'draft')
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state, 'pending')
            rec.write({
                'state': 'pending'
            })

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state, 'sold')
            rec.state = 'sold'

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')
            rec.state = 'closed'

    def check_expected_selling_date(self):
        print(self)
        property_ids = self.search([])

        for rec in property_ids:
            print(rec.expected_selling_date)
            if rec.expected_selling_date and rec.expected_selling_date > fields.date.today():
                rec.is_late = False

            if rec.expected_selling_date and rec.expected_selling_date <= fields.date.today():
                rec.is_late = True

            print(rec.is_late)

    @api.depends('expected_price', 'selling_price')


    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.expected_price - rec.selling_price


    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            print('inside onchange_expected_price')
        return {'warning': {'title': 'Warning!!', 'message': 'You Changed the Expected Price!', 'type': 'warning'}
                }

    @api.model_create_multi
    def create(self, vals):
        res = super(Property, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('property_sequence')
        return res

    def action_open_change_state_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.change_state_wizard_action')
        action['context'] = {
            'default_property_id': self.id,
        }
        return action
    # @api.depends('owner_id')
    # def _compute_owner_address(self):
    #     for rec in self:
    #         rec.owner_address_compute =  rec.owner_id.address
    #
    # @api.depends('owner_id')
    # def _compute_owner_phone(self):
    #     for rec in self:
    #         rec.owner_phone_compute =  rec.owner_id.phone
#
# @api.model
# def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
#     res = super(Property,self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
#     print(f'Inside Search Method')
#     return res
#
# def write(self, vals):
#     res = super(Property, self).write(vals)
#     print(f'Inside Write Method')
#     return res
#
# def unlink(self):
#     res = super(Property, self).unlink()
#     print(f'Inside Unlink Method')
#     return res
#
#     def action(self):
#         print(self.env["owner"].search([('name','=','Abooda')]).unlink())

class PropertyLine(models.Model):
    _name = 'property.line'
    _description = 'Property Bedrooms'
    property_id = fields.Many2one('property')
    area = fields.Float()
    description = fields.Char()
