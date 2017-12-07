# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Allfacultyconstraints(models.Model):
    _name = 'op.all.faculty.constraints'

    # Time Constraint II (All Teachers)
    @api.multi
    @api.constrains('interval_end', 'interval_start')
    def check_interval_time(self):
        for t in self:
            if t.interval_end and t.interval_start and (t.interval_end.sequence < t.interval_start.sequence):
                raise UserError(_("Start hour cannot be greater or equal than end hour"))

    name = fields.Char('Name', default="Faculty Constraint")
    weight_percent = fields.Float('Weight %', default=100, size=100)
    max_days_per_week = fields.Integer(
        'Max days per Week For All Faculty', default=lambda self: self.env.user.company_id.tt_max_days, size=10)
    min_days_per_week = fields.Integer('Min days per Week For All Faculty', size=10)
    max_gaps_per_day = fields.Integer('Max gaps per day for all Faculty', size=10)
    max_gaps_per_week = fields.Integer('Max gaps per Week for All Faculty', size=10)
    max_hrs_daily = fields.Integer('Max Hours daily For All Faculty', size=10)
    max_hrs_act = fields.Integer('**Max Hours Daily with an activity For all Faculty', size=10)
    min_hrs_daily = fields.Integer('Min Hours Daily For All Faculty', size=10)
    max_hrs_cont_tr = fields.Integer('Max Hours Continuously For All Faculty', size=10)
    interval_start = fields.Many2one('op.timing', 'Interval Start Hour')
    interval_end = fields.Many2one('op.timing', 'Interval End Hour')
    max_building_change = fields.Integer('Max Building Changes Per Day', size=10)
    max_building_week = fields.Integer('Max Building Changes Per Week', size=10)
    min_gap_building = fields.Integer('Min Gaps Between Building Changes', size=10)

    _sql_constraints = [('unique_Faculty', 'unique(name)', 'Only one Constraint required.')]

    @api.multi
    @api.constrains('weight_percent')
    def check_weight_percentage(self):
        for rec in self:
            if rec.weight_percent != 100:
                raise UserError(_("Please set the weight percentage to 100."))
