# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class MeasureWizard(models.Model):
    _name = 'sale.order.line.measure.wizard'
    _description = 'measurements'

    customer_id = fields.Many2one('res.partner','Customer Name')
    fabric_details = fields.Text('Fabric Details')
    body_measure_ids  = fields.One2many('sale.order.line.measure.line','measure_id',"Measurements")

    @api.model
    def default_get(self, fields):
        res = super(MeasureWizard, self).default_get(fields)
        if self._context and self._context.get('active_id'):
            active_id = self.env['sale.order.line'].browse(self._context.get('active_id',False))
            res['customer_id'] = active_id.order_id.partner_id.id
            res['fabric_details'] = active_id.fabric_details
            if active_id and active_id.body_measure_ids:
                lis = []
                for vals in active_id.body_measure_ids:
                    lis.append(vals.id)
                res['body_measure_ids'] = [(6,0,lis)]
            elif active_id and active_id.product_id and active_id.product_id.body_part_ids:
                lis = []
                for part_id in active_id.product_id.body_part_ids:
                     lis.append((0,0,{'body_part_id':part_id.body_part_id.id,'measure':0}))
                res['body_measure_ids'] = lis
        return res

    def action_save(self):
        if self._context and self._context.get('active_id'):
            active_id = self.env['sale.order.line'].browse(self._context.get('active_id',False))
            active_id.customer_id = self.customer_id
            active_id.fabric_details = self.fabric_details
            lis = []
            if self.body_measure_ids:
                for vals in self.body_measure_ids:
                    lis.append(vals.id)
            active_id.body_measure_ids = [(6,0,lis)]
