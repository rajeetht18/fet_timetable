# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _

class service_inwards(models.Model):
    _name = 'service.inwards.line'
    _rec_name = 'product_id'

    product_id = fields.Many2one('product.product','Product')
    qty = fields.Integer('Quantity')
    reference = fields.Char("Reference/Description")
    estimated_val = fields.Float('Estimated Value')
    service_id = fields.Many2one('service.agreement','Services')
    move_id = fields.Many2one('stock.move','Stock Move')
    service_status = fields.Selection("Service Status",related='move_id.service_status',store=True)

class Task(models.Model):
     _inherit = 'project.task'

     group_id = fields.Many2one('service.agreement.group','Service')
     department_id = fields.Many2one('hr.department',"Department")
     service_task_id = fields.Many2one('service.agreement','Services')
     sale_order_id = fields.Many2one('sale.order',"Sale Order")
     sale_state_done = fields.Boolean("Sale Done")
     sale_state_complete = fields.Boolean("Sale Complete")

class service_history_line(models.Model):
    _name = 'service.history.line'

    department_id = fields.Many2one('hr.department',"Department")
    duration = fields.Char("Duration")
    start_date = fields.Date("Start Date")
    expected_end_date = fields.Date("Expected End Date")
    actual_end_date = fields.Date("End Date")
    service_history_id = fields.Many2one('service.agreement','Services')
    group_id = fields.Many2one('service.agreement.group','Service')

class service_agreement(models.Model):
    _inherit = 'service.agreement'

    @api.model
    def create(self, vals):
        res = super(service_agreement, self).create(vals)
        project = self.env['project.project'].create({'name':res['name']})
        res['project_id'] = project
        if res['service_task_ids']:
            res['service_task_ids'].project_id = project
        return res

    @api.multi
    def write(self,vals):
        res = super(service_agreement, self).write(vals)
        for rec in self:
            rec.project_id.name = rec.name
        return res

    @api.multi
    def unlink(self):
        for rec in self:
            for lines in rec.service_task_ids:
                lines.unlink()
            rec.project_id.unlink()
        return super(service_agreement, self).unlink()

    @api.model
    def _default_company(self):
        return self.env['res.company']._company_default_get('date.range')

    project_id = fields.Many2one('project.project',"Project")
    service_task_ids = fields.One2many('project.task','service_task_id','History Lines')
    lead_id = fields.Many2one("crm.lead","Leads")
    cycle_id = fields.Many2one('service.cycle', string='Billing Cycle', required=False, readonly=True,
                               states={'draft': [('readonly', False)]})
    inward_ids = fields.One2many('service.inwards.line','service_id','Inwards')
    company_id = fields.Many2one('res.company', string='Company',default=_default_company)
    partner_id = fields.Many2one('res.partner', string='Customer',
                                 required=True, readonly=True, states={'draft': [('readonly', False)]})
    tot_qty = fields.Float("Inward Total Qty",compute="total_qty")
    tot_est_val = fields.Float("Total Estimated Value",compute="total_est_val")

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

    @api.multi
    def contract_open(self):
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
        return super(service_agreement,self).contract_open()

    @api.multi
    def contract_close(self):
        if self.inward_ids:
            for inward in self.inward_ids:
                inward.move_id.state = 'cancel'
        return self.write({'state': 'closed'})

class res_company(models.Model):
    _inherit = 'res.company'

    default_warehouse = fields.Many2one('stock.warehouse',string='Warehouse')
    default_src_location = fields.Many2one('stock.location', string='Source Location')
    default_dest_location = fields.Many2one('stock.location', string='Destination Location')
