# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _

class service_inwards(models.Model):
    _inherit = 'service.inwards.line'

    sale_inward_id = fields.Many2one('sale.order','Sale')

class Task(models.Model):
     _inherit = 'project.task'

     sale_task_id = fields.Many2one('sale.order','Sale')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_task_ids = fields.One2many('project.task','sale_task_id','History Lines')
    inward_ids = fields.One2many('service.inwards.line','sale_inward_id','Inwards')
    tot_qty = fields.Float("Inward Total Qty",compute="total_qty")
    tot_est_val = fields.Float("Total Estimated Value",compute="total_est_val")
    project_id = fields.Many2one('project.project',"Project")

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Confirmed'),
        ('progress','Progress'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        project = self.env['project.project'].create({'name':res['name']})
        res['project_id'] = project
        if res['sale_task_ids']:
            res['sale_task_ids'].project_id = project
        return res

    @api.multi
    def write(self,vals):
        res = super(SaleOrder, self).write(vals)
        for rec in self:
            if rec.project_id:
                rec.project_id.name = rec.name
        return res

    @api.multi
    def unlink(self):
        for rec in self:
            for lines in rec.sale_task_ids:
                lines.unlink()
            rec.project_id.unlink()
        return super(SaleOrder, self).unlink()

    @api.multi
    def set_to_done(self):
        self.state = 'done'

    @api.multi
    def set_to_progress(self):
        if self.inward_ids:
            for inward in self.inward_ids:
                move = self.env['stock.move'].create({
                    'name': inward.reference,
                    'location_id': self.company_id.default_src_location.id,
                    'location_dest_id': self.company_id.default_dest_location.id,
                    'product_id': inward.product_id.id,
                    'product_uom': inward.product_id.uom_id.id,
                    'product_uom_qty': inward.qty,
                    'origin':self.name
                })
                move._action_confirm()
                move._action_assign()
                move.move_line_ids.write({'qty_done': inward.qty})
                move._action_done()
                inward.move_id = move.id
        self.state = 'progress'

    @api.depends('inward_ids.qty')
    def total_qty(self):
        self.tot_qty = 0
        for rec in self.inward_ids:
            if rec.qty:
                self.tot_qty += rec.qty

    @api.depends('inward_ids.estimated_val')
    def total_est_val(self):
        self.tot_est_val = 0
        for rec in self.inward_ids:
            if rec.estimated_val:
                self.tot_est_val += rec.estimated_val
