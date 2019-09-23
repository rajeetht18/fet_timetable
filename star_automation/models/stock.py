# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _

class StockMove(models.Model):
    _inherit = 'stock.move'

    service_status = fields.Selection([('progress',"In Progress"),('completed',"Completed"),('return',"Return")],"Service Status")
    inward_id = fields.Many2one('service.inwards.line',"Inward Line")