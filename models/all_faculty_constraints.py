# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Allfacultyconstraints(models.Model):
    _name = 'op.all.faculty.constraints'

    # Time Constraint II (All Teachers)
    name = fields.Char('Name', default="Faculty Constraint")
    weight_percent = fields.Float('Weight %', default=100, size=100)
    max_days_per_week = fields.Integer('Max days Per Week For All Faculty', default='set_default_week', size=10)
    min_days_per_week = fields.Integer('Min days Per Week For All Faculty', size=10)
    max_gaps_per_day = fields.Integer('Max gaps per day for all Faculty', size=10)
    max_gaps_per_week = fields.Integer('Max gaps per Week for All Faculty', size=10)
    max_hrs_daily = fields.Float('Max Hours daily For All Faculty', size=10)
    max_hrs_act = fields.Float('Max Hours Daily with an activity For all Faculty', size=10)
    min_hrs_daily = fields.Float('Min Hours Daily For All Faculty', size=10)
    max_hrs_cont_tr = fields.Float('Max Hours Continuously For All Faculty', size=10)
    max_hrs_cont_tr_act = fields.Float('Max Hours Continuously with an activity For All Faculty')
    interval_start = fields.Many2one('op.timing', 'Interval Start Hour', size=30)
    interval_end = fields.Many2one('op.timing', 'Interval End Hour', size=30)

    _sql_constraints = [('unique_Faculty', 'unique(name)', 'Only one Constraint required.')]

    @api.model
    def set_default_week(self):
        default_week = self.env['timetable.days.config'].search[()]
        for max_days_per_week in default_week:
            if max_days_per_week == default_week.tt_monday:
                max_days_per_week.monday = 1
            if max_days_per_week == default_week.tt_tuesday:
                max_days_per_week.tuesday = 2
            if max_days_per_week == default_week.tt_wednesday:
                max_days_per_week.wednesday = 3
            if max_days_per_week == default_week.tt_thursday:
                max_days_per_week.thursday = 4
            if max_days_per_week == default_week.tt_friday:
                max_days_per_week.friday = 5
            if max_days_per_week == default_week.tt_saturday:
                max_days_per_week.saturday = 6
            if max_days_per_week == default_week.tt_sunday:
                max_days_per_week.sunday = 7
        return max_days_per_week



    @api.multi
    @api.constrains('weight_percent')
    def check_weight_percentage(self):
        for rec in self:
            if rec.weight_percent != 100:
                raise UserError(_("Please set the weight percentage to 100."))
