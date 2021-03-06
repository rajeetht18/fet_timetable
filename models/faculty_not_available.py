# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from company import WEEK_DAYS


class FacultyTime(models.Model):
    _name = 'op.faculty.not.available'
    _description = 'Faculty Times'

    @api.multi
    def set_not_available(self):
        day_config = self.env['res.company'].search(
            [('id', '=', self.env.user.company_id.id)])
        if day_config:
            for l in self.faculty_not_line_ids:
                if day_config.tt_monday:
                    l.monday = 1
                if day_config.tt_tuesday:
                    l.tuesday = 1
                if day_config.tt_wednesday:
                    l.wednesday = 1
                if day_config.tt_thursday:
                    l.thursday = 1
                if day_config.tt_friday:
                    l.friday = 1
                if day_config.tt_saturday:
                    l.saturday = 1
                if day_config.tt_sunday:
                    l.sunday = 1

    @api.multi
    def set_available(self):
        day_config = self.env['res.company'].search(
            [('id', '=', self.env.user.company_id.id)])
        if day_config:
            for l in self.faculty_not_line_ids:
                if day_config.tt_monday:
                    l.monday = 0
                if day_config.tt_tuesday:
                    l.tuesday = 0
                if day_config.tt_wednesday:
                    l.wednesday = 0
                if day_config.tt_thursday:
                    l.thursday = 0
                if day_config.tt_friday:
                    l.friday = 0
                if day_config.tt_saturday:
                    l.saturday = 0
                if day_config.tt_sunday:
                    l.sunday = 0

    @api.model
    def create(self, values):
        res = super(FacultyTime, self).create(values)
        if len(values['faculty_not_line_ids']) == 0:
            raise UserError(
                _("Please configure Timetable Days to create your Faculty Time Constraint."))
        return res

    @api.model
    def default_line(self):
        period_list = []
        period_dict = {}
        day_config = self.env['res.company'].search(
            [('id', '=', self.env.user.company_id.id)])
        if day_config:
            for time in self.env['op.timing'].search([]):
                period_dict = {
                    'name': time.name,
                    'is_monday': day_config.tt_monday,
                    'is_tuesday': day_config.tt_tuesday,
                    'is_wednesday': day_config.tt_wednesday,
                    'is_thursday': day_config.tt_thursday,
                    'is_friday': day_config.tt_friday,
                    'is_saturday': day_config.tt_saturday,
                    'is_sunday': day_config.tt_sunday
                }
                period_list.append((0, 0, period_dict))
        return period_list

    _sql_constraints = [('unique_faculty', 'unique(name)',
                         'There must be another constraint of this Faculty. Please edit that one.')]

    name = fields.Many2one('op.faculty', 'Faculty Name', required=True)
    weight_percent = fields.Float('Weight Percent', default=100)
    faculty_not_line_ids = fields.One2many(
        'op.faculty.not.available.list', 'faculty_id', "Facutly Not Available", default=default_line)

    @api.multi
    @api.constrains('faculty_not_line_ids')
    def _check_faculty_line_ids(self):
        for record in self:
            flag = any([True for line in record.faculty_not_line_ids for d in WEEK_DAYS if getattr(
                line, d) != 0 and getattr(line, d) != 1])
            if flag:
                raise UserError(_("Period value should be 1 or 0."))


class Facultytimelist(models.Model):
    _name = 'op.faculty.not.available.list'
    _description = 'Faculty Time Line'

    name = fields.Char("Periods")
    monday = fields.Integer("Monday", size=1, default=0)
    tuesday = fields.Integer("Tuesday", size=1, default=0)
    wednesday = fields.Integer("Wednesday", size=1, default=0)
    thursday = fields.Integer("Thursday", size=1, default=0)
    friday = fields.Integer("Friday", size=1, default=0)
    saturday = fields.Integer("Saturday", size=1, default=0)
    sunday = fields.Integer("Sunday", size=1, default=0)
    is_monday = fields.Boolean("Monday?")
    is_tuesday = fields.Boolean("Tuesday?")
    is_wednesday = fields.Boolean("Wednesday?")
    is_thursday = fields.Boolean("Thursday?")
    is_friday = fields.Boolean("Friday?")
    is_saturday = fields.Boolean("Saturday?")
    is_sunday = fields.Boolean("Sunday?")
    faculty_id = fields.Many2one('op.faculty.not.available', "Faculty")
