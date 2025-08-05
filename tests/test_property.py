from odoo import fields

from odoo.tests.common import TransactionCase


class TestProperty(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestProperty, self).setUp()

        self.property_01_record = self.env['property'].create({
            'ref': 'PRT1000',
            'name': 'Property 1000',
            'description': 'Property 1000 Description',
            'postcode': '14857',
            'date_availability': fields.Date.today(),
            'bedrooms': 4,
            'living_area': 320,
            'expected_price': 5000,
        })

    def test_01_property_values(self):
        property_id = self.property_01_record

        self.assertRecordValues(property_id, [{
            'ref': 'PRT1000',
            'name': 'Property 1000',
            'description': 'Property 1000 Description',
            'postcode': '14857',
            'date_availability': fields.Date.today(),
            'bedrooms': 4,
            'living_area': 320,
            'expected_price': 5000,
        }])
