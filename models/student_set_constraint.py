# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class studentconstraints(models.Model):
    _name = 'student.time.constraints'

    @api.multi
    @api.constrains('weight_percent', 'weight_room')
    def check_weight_percentage(self):
        for rec in self:
            if rec.weight_percent != 100:
                raise UserError(_("Please set the weight percentage to 100."))

    # Student Time Constraints
    name = fields.Many2one('op.batch', 'Batch', required=True)
    group_name = fields.Many2one('op.batch.group', 'Group')
    subgroup_name = fields.Many2one('op.batch.subgroup', 'Subgroup')
    weight_percent = fields.Integer('Weight Percent', default=100, size=10)
    max_days_week = fields.Integer('Max Days Per Week For Student',
                                   default=lambda self: self.env.user.company_id.tt_max_days, size=10)
    max_gaps_day = fields.Integer(
        'Max Gaps Per Day For Student', size=10)
    max_gaps_week = fields.Integer('Max Gaps Per Week For Student', size=10)
    max_begin_second = fields.Integer(
        'Max Beginnings At Second Hour(Per Week)', size=10)
    max_hrs_daily = fields.Integer('Max Hours daily For Student', size=10)
    max_hrs_daily_act = fields.Integer(
        'Max Hour daily with an activity', size=10)
    min_hrs_daily = fields.Integer('Min Hours daily for Student', size=10)
    max_hr_cont = fields.Integer('Max Hours Continuously for student', size=10)
    max_hr_cont_act = fields.Integer(
        'Max Hours Continuously with an activity', size=10)
    interval_start = fields.Many2one('op.timing', 'Interval Start')
    interval_end = fields.Many2one('op.timing', 'Interval End')
    activity_name = fields.Many2one('op.activity.tags', 'Activity')

    # Space Constraints
    student_homeroom = fields.Many2one(
        'op.classroom', string="A Set of students has home room")
    student_set_of_homerooms = fields.Many2many(
        'op.classroom', string="A set of Students Has a set of rooms")
    weight_room = fields.Integer(
        'Weight Percentage For Room', default=100, size=10)
    max_building_changes = fields.Integer(
        'Max Building Changes Per day', size=10)
    max_build_week = fields.Integer('Max Building Changes Per Week')
    min_gaps_building = fields.Integer(
        'Min gaps between building changes', size=10)

    @api.multi
    @api.constrains('name', 'group_name', 'subgroup_name')
    def check_batch_groups(self):
        for t in self:
            res = self.search([('name','=',t.name.id),('group_name','=',t.group_name.id or False),('subgroup_name','=',t.subgroup_name.id or False)])
            if len(res) > 1:
                raise UserError(_("You can't set the same constrains more than once."))
                
    @api.multi
    @api.constrains('interval_end', 'interval_start')
    def check_interval_time(self):
        for t in self:
            if t.interval_end and t.interval_start and t.interval_end.sequence < t.interval_start.sequence:
                raise UserError(_("Interval End Time Should Be Greater"))

    @api.multi
    @api.constrains('weight_room')
    def check_room_weight(self):
        for w in self:
            if w.weight_room > 100:
                raise UserError(
                    _("Please set the weight percentage to 100 or below."))
