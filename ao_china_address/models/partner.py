# -*- coding: utf-8 -*-
from lxml import etree

from odoo import api, fields, models


class Partner(models.Model):

    _name = 'res.partner'
    _inherit = 'res.partner'

    district_id = fields.Many2one('res.district', string='District of Address')

    @api.model
    def _address_fields(self):
        """Returns the list of address fields that are synced from the parent."""
        address = super(Partner, self)._address_fields()
        return address

    @api.onchange('state_id')
    def _onchange_state_id(self):
        self.city_id = False
        self.city = None

    @api.onchange('city_id')
    def _onchange_city_id(self):
        self.district_id = False

    @api.onchange('district_id')
    def _onchange_district_id(self):
        if self.district_id:
            self.city_id = self.district_id.city_id.id
            if self.district_id.zipcode:
                self.zip = self.district_id.zipcode

    @api.model
    def _fields_view_get_address(self, arch):
        arch = super(Partner, self)._fields_view_get_address(arch)
        # render the partner address accordingly to address_view_id
        doc = etree.fromstring(arch)
        if doc.xpath("//field[@name='district_id']"):
            return arch

        replacement_xml = """
            <div>
                <field name="city_id" invisible="1"/>
                <field name="district_id" placeholder="区/县" class="o_address_street"
                    context="{'default_city_id': city_id, 'default_zipcode': zip}"
                    domain="[('city_id', '=', city_id)]"
                    attrs="{
                        'invisible': [('country_enforce_cities', '=', False)],
                        'readonly': [('type', '=', 'contact')%(parent_condition)s]
                    }"
                />
            </div>
        """

        replacement_data = {}

        def _arch_location(node):
            in_subview = False
            view_type = False
            parent = node.getparent()
            while parent is not None and (not view_type or not in_subview):
                if parent.tag == 'field':
                    in_subview = True
                elif parent.tag in ['list', 'tree', 'kanban', 'form']:
                    view_type = parent.tag
                parent = parent.getparent()
            return {
                'view_type': view_type,
                'in_subview': in_subview,
            }

        for street2_node in doc.xpath("//field[@name='street2']"):
            location = _arch_location(street2_node)
            replacement_data['parent_condition'] = ''
            if location['view_type'] == 'form' or not location['in_subview']:
                replacement_data['parent_condition'] = ", ('parent_id', '!=', False)"

            replacement_formatted = replacement_xml % replacement_data
            for replace_node in etree.fromstring(replacement_formatted).getchildren():
                street2_node.addnext(replace_node)

        for city_node in doc.xpath("//field[@name='city_id']"):
            city_node.set('domain', "[('state_id', '=', state_id)]")

        arch = etree.tostring(doc, encoding='unicode')
        return arch
