# -*- coding: utf-8 -*-

from odoo import api, fields, models


class District(models.Model):

    _name = 'res.district'
    _description = 'City'
    _order = 'name'

    name = fields.Char("Name", required=True, translate=True)
    zipcode = fields.Char("Zip")
    city_id = fields.Many2one('res.city', string='城市', domain="[('state_id', '=', state_id)]")


class City(models.Model):

    _name = 'res.city'
    _inherit = 'res.city'

    district_ids = fields.One2many('res.district', 'city_id', string='District')
