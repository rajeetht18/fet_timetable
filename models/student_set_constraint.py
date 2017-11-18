# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class studentconstraints(models.Model):
    _name = 'student.time.constraints'

    # Student Time Constraints
    batch_name = fields.Many2one('op.batch', 'Batch', required=True)
    group_name = fields.Many2one('op.batch.group', 'Group')
    subgroup_name = fields.Many2one('op.batch.subgroup', 'Subgroup')
    weight_percent = fields.Integer('Weight Percent', size=10)
    max_days_week = fields.Integer('Max Days Per Week For Student', size=10)
    max_gaps_day = fields.Integer('Max Gaps Per Day For Student', size=10)
    max_gaps_week = fields.Integer('Max Gaps Per Week For Student', size=10)
    max_begin_second = fields.Integer('Max Beginnings At Second Hour(Per Week)', size=10)
    max_hrs_daily = fields.Integer('Max Hours daily For Student', size=10)
    max_hrs_daily_act = fields.Integer('Max Hour daily with an activity', size=10)
    min_hrs_daily = fields.Integer('Min Hours daily for Student', size=10)
    max_hr_cont = fields.Integer('Max Hours Continuously for student', size=10)
    max_hr_cont_act = fields.Integer('Max Hours Continuously with an activity', size=10)
    interval_start = fields.Many2one('op.timing', 'Interval Start')
    interval_end = fields.Many2one('op.timing', 'Interval End')

    # Space Constraints
    room = fields.Integer('A Set of students has home room', size=10)
    set_of_rooms = fields.Integer('A set of Students Has a set of rooms', size=10)
    max_building_changes = fields.Integer('Max Building Changes Per day', size=10)
    max_build_week = fields.Integer('Max Building Changes Per Week')
    min_gaps_building = fields.Integer('Min gaps between building changes', size=10)
