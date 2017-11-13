# -*- coding: utf-8 -*-
from odoo import models, fields


class Facultyconstraints(models.Model):
    _name = 'op.faculty.constraints'

    # Time Constraint II (All Teachers)
    name = fields.Char('Name', default="Faculty Constraint")
    weight_percent = fields.Float('Weight %', default=100, size=100)
    max_days_per_week = fields.Integer('Max days for All Faculty', size=10)
    min_days_per_week = fields.Integer('Min days For All Faculty', size=10)
    max_gaps_per_day = fields.Integer('Max gaps per day for all Faculty', size=10)
    max_gaps_per_week = fields.Integer('Max gaps per Week for All Faculty', size=10)
    max_hrs_daily = fields.Float('Max Hours daily For All Faculty', size=10)
    max_hrs_act = fields.Float('Max Hours Daily with an activity For all Faculty', size=10)
    min_hrs_daily = fields.Float('Min Hours Daily For All Faculty', size=10)
    max_hrs_cont_tr = fields.Float('Max Hours Continuously For All Faculty', size=10)
    max_hrs_cont_tr_act = fields.Float('Max Hours Continuously with an activity For All Faculty')

    _sql_constraints = [('unique_Faculty', 'unique(name)', 'Only one Constraint required.')]
