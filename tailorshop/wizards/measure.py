# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class BodyParts(models.Model):
    
    _name = 'body.parts'
    _description = 'Body parts'

    name = fields.Char("Name")
    code = fields.Char("Code")


class MeasureWizard(models.Model):

    _name = 'sale.order.line.measure.wizard'
    _description = 'measurements'

    customer_id = fields.Many2one('res.partner','Customer Name')
    fabric_details = fields.Text('Fabric Details')
    body_measure_ids  = fields.One2many('sale.order.line.measure.line','measure_id',"Measurements")


class MeasureLineWizard(models.Model):

    _name = 'sale.order.line.measure.line'
    _description = 'measurements'


    body_part_id = fields.Many2one('body.parts',"Name")
    measure = fields.Char("Measure (m)")
    measure_id = fields.Many2one('sale.order.line.measure.wizard',"Measure ID")

