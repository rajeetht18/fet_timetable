# -*- coding: utf-8 -*-
from odoo import api,fields,models,_
from odoo.exceptions import UserError

class BreaksTime(models.Model):
    _name = 'op.break.time'
    _description = 'Break Times'

    @api.model
    def default_line(self):
        period_list = []
        day_config = self.env['timetable.days.config'].search([], order='id desc', limit=1)
        print day_config,' day_config.tt_monday'
        for time in self.env['op.timing'].search([]):
            period_dict = {'name':time.name}
            if day_config:
                period_dict.update({'is_monday': day_config.tt_monday, 'is_tuesday': day_config.tt_tuesday,'is_wednesday': day_config.tt_wednesday, 'is_thursday': day_config.tt_thursday, 'is_friday': day_config.tt_friday, 'is_saturday': day_config.tt_saturday, 'is_sunday': day_config.tt_sunday})
            period_list.append((0,0,period_dict))
        return period_list

    _sql_constraints = [('unique_name','unique(name)', 'There must be another constraint of this type. Please edit that one.')]

    name = fields.Char("Name",default="Break Time Constraints",readonly="1")
    break_line_ids = fields.One2many('op.break.time.line','break_id',"Breaks",default=default_line)

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

class BreakTimeLine(models.Model):
    _name = 'op.break.time.line'
    _description = 'Break Time Line'

    @api.model
    def _default_monday(self):
        day_config = self.env['timetable.days.config'].search([])
        print day_config.tt_monday,' day_config.tt_monday'
        return day_config and day_config.tt_monday
 
    name = fields.Char("Periods")
    monday = fields.Integer("Monday",size=1)
    tuesday = fields.Integer("Tuesday",size=1)
    wednesday = fields.Integer("Wednesday",size=1)
    thursday = fields.Integer("Thursday",size=1)
    friday = fields.Integer("Friday",size=1)
    saturday = fields.Integer("Saturday",size=1)
    sunday = fields.Integer("Sunday",size=1)
    is_monday = fields.Boolean("Monday?")
    is_tuesday = fields.Boolean("Tuesday?",default="0")
    is_wednesday = fields.Boolean("Wednesday?",default="0")
    is_thursday = fields.Boolean("Thursday?",default="0")
    is_friday = fields.Boolean("Friday?",default="0")
    is_saturday = fields.Boolean("Saturday?",default="0")
    is_sunday = fields.Boolean("Sunday?",default="0")
    break_id = fields.Many2one('op.break.time',"Break")
