# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class Product(models.Model):
    _inherit = 'product.template'

    body_part_ids  = fields.One2many('product.line.measure','measurement_id',"Measurements")

class Measurements(models.Model):
    _name = 'product.line.measure'
    _description = 'measurements'

    body_part_id = fields.Many2one('body.parts',"Name")
    measurement_id = fields.Many2one('product.template',"Measure")
