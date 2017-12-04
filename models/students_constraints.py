# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Studentnotavailable(models.Model):
    _name = 'all.student.constraints'

    name = fields.Char('Name', default='Student Constraint')
    weight_percent = fields.Integer('Weight Percentage', default=100)
    max_days_week = fields.Integer('Max Days Per Week For All Studenst',
                                   default=lambda self: self.env.user.company_id.tt_max_days, size=10)
    max_gaps_per_week = fields.Integer(
        'Max Gaps Per Week For All Students', size=10)
    max_gaps_per_day = fields.Integer(
        '**Max Gaps Per Day For All Students', size=10)
    max_beginnings = fields.Integer(
        'Max Beginnings At second Hour(per week)', size=10)
    max_hr_daily = fields.Float('Max Hours Daily For All Students', size=10)
    min_hr_daily = fields.Float('Min Hours Daily For All Students', size=10)
    max_hr_cont_act = fields.Float(
        'Max Hour Continously with Activity For All Students', size=10)
    max_hr_cont = fields.Float(
        'Max Hour Continously For All Students', size=10)
    start_time = fields.Many2one('op.timing', 'Interval Start Hour')
    end_time = fields.Many2one('op.timing', 'Interval End Hour')
    max_hr_daily_act = fields.Float(
        '**Max Hour Daily with an Activity For All Students', size=10)
    max_hr_cont = fields.Float(
        'Max Hour Continously For All Students', size=10)
    max_build = fields.Integer('Max building changes per day', size=10)
    max_build_week = fields.Integer('Max Building Changes per week', size=10)
    min_gaps_build = fields.Integer(
        'Min Gaps Between building changes', size=10)
    activity = fields.Many2one('op.activity.tags', 'Activity')
