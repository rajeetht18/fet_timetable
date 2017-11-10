# -*- coding: utf-8 -*-
from odoo import api,fields,models

class BatchConstraints(models.Model):
    _name = 'op.batch.constraints'
    _description = 'A Students set not available times'
    _rec_name = 'student_id'

    @api.model
    def default_line(self):
        list1 = []
        timing_obj = self.env['op.timing'].search([])
        for time in timing_obj:
            dic = {
                'name':time.name,
            }
            list1.append((0,0,dic))
        return list1

    @api.multi
    @api.constrains('break_line_ids')
    def _check_break_line_ids(self):
        for record in self:
            flag = False
            for line in record.break_line_ids:
                if line.monday != 0 and line.monday != 1:
                    flag = True
                if line.tuesday != 0 and line.tuesday != 1:
                    flag = True
                if line.wednesday != 0 and line.wednesday != 1:
                    flag = True
                if line.thursday != 0 and line.thursday != 1:
                    flag = True
                if line.friday != 0 and line.friday != 1:
                    flag = True
                if line.saturday != 0 and line.saturday != 1:
                    flag = True
                if line.sunday != 0 and line.sunday != 1:
                    flag = True
            if flag:
                raise UserError(_("Break value should be 1 or 0."))
            
    _sql_constraints = [
        ('unique_batch',
         'unique(student_id)', 'You cannot create a Batch Constraint again with the same batch!')]



    student_id = fields.Many2one('op.batch',"Batch",required=1)
    batch_constraints_line_ids = fields.One2many('op.breaks.constraints.line','batch_constraint_id',"Batch Constraints",default=default_line)

class BatchConstraintsLine(models.Model):
    _name = 'op.breaks.constraints.line'
    _description = 'Batch constraints Line'


    name = fields.Char("Periods")
    monday = fields.Integer("Monday",size=1)
    tuesday = fields.Integer("Tuesday",size=1)
    wednesday = fields.Integer("Wednesday",size=1)
    thursday = fields.Integer("Thursday",size=1)
    friday = fields.Integer("Friday",size=1)
    saturday = fields.Integer("Saturday",size=1)
    sunday = fields.Integer("Sunday",size=1)
    mon_bool = fields.Boolean("Monday Bool",default="0")
    tues_bool = fields.Boolean("Tuesday Bool",default="0")
    wed_bool = fields.Boolean("Wednesday Bool",default="0")
    thurs_bool = fields.Boolean("Thurs Bool",default="0")
    fri_bool = fields.Boolean("Friday Bool",default="0")
    sat_bool = fields.Boolean("Saturday Bool",default="0")
    sun_bool = fields.Boolean("Sunday Bool",default="0")
    batch_constraint_id = fields.Many2one('op.batch.constraints',"Batch Constraints")
