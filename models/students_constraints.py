# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Studentnotavailable(models.Model):
    _name = 'all.student.constraints'

    # All Students Time Constraints
    @api.model
    def _get_default_maxdays(self):
        res_days = self.env['res.company'].search(
            [('id', '=', self.env.user.company_id.id)])
        count = 0
        for l in res_days:
            if l.tt_monday:
                count += 1
            if l.tt_tuesday:
                count += 1
            if l.tt_wednesday:
                count += 1
            if l.tt_thursday:
                count += 1
            if l.tt_friday:
                count += 1
            if l.tt_saturday:
                count += 1
            if l.tt_sunday:
                count += 1
        return count

    name = fields.Char('Name', default='Student Constraint')
    weight_percent = fields.Integer('Weight Percentage', default=100)
    max_days_week = fields.Integer(
        'Max Days Per Week For All Studenst', default=_get_default_maxdays, size=10)
    max_gaps_per_week = fields.Integer(
        'Max Gaps Per Week For All Students', size=10)
    max_gaps_per_day = fields.Integer(
        'Max Gaps Per Day For All Students', size=10)
    max_beginnings = fields.Integer(
        'Max Beginnings At second Hour(per week)', size=10)
    max_hr_daily = fields.Float('Max Hours Daily For All Students', size=10)
    min_hr_daily = fields.Float('Min Hours Daily For All Students', size=10)
    max_hr_cont_act = fields.Float(
        'Max Hour Continously with Activity For All Students', size=10)
    max_hr_cont = fields.Float(
        'Max Hour Continously For All Students', size=10)
    # activity_id = fields.Many2one('op.activity.tags', 'Activity', size=10)
    start_time = fields.Many2one('op.timing', 'Interval Start Hour')
    end_time = fields.Many2one('op.timing', 'Interval End Hour')
    max_hr_cont = fields.Float(
        'Max Hour Continously For All Students', size=10)
    max_build = fields.Integer('Max building changes per day', size=10)
    max_build_week = fields.Integer('Max Building Changes per week', size=10)
    min_gaps_build = fields.Integer(
        'Min Gaps Between building changes', size=10)
    activity = fields.Many2one('op.activity.tags', 'Activity')
