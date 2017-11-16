# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StudentCourse(models.Model):
    _inherit = 'op.student.course'

    group_id = fields.Many2one('op.batch.group', 'Group')
    subgroup_id = fields.Many2one('op.batch.subgroup', 'Subgroup')


class Faculty(models.Model):
    _inherit = 'op.faculty'

    @api.model
    def _get_default_maxdays(self):
        res_days = self.env['res.company'].search([('id', '=', self.env.user.company_id.id)])
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



    class_details = fields.One2many('op.faculty.class.list', 'list_id', string="Splits")
    weight_percent = fields.Float('Weight %', default=100, size=100)
    max_days = fields.Integer('Max days Per Week', default=_get_default_maxdays, size=10)
    min_days = fields.Integer('Min days Per Week', size=10)
    max_gaps = fields.Integer('Max gaps Per Day', size=10)
    min_gaps = fields.Integer('Min gaps per Day', size=10)
    max_hrs = fields.Float('Max Hours', size=60)
    max_hrs_act = fields.Float('Max Hours with Activity', size=60)
    min_hrs = fields.Float('Min Hours Daily', size=18)
    interval_start = fields.Many2one('op.timing', 'Interval Start Hour', size=20)
    interval_end = fields.Many2one('op.timing', 'Interval End Hour', size=25)
    max_hrs_cont = fields.Float('Max Hours Continuously', size=18)
    max_hr_cont_act = fields.Float('Max Hours Continuous with Activity', size=20)
    max_buliding = fields.Integer('Max Building Changes Per Day', size=10)
    max_bulid_week = fields.Integer('Max Buliding Changes Per Week', size=10)
    max_gap_build = fields.Integer('Max Gap Between Building Changes', size=10)
    activity_name = fields.Many2one('op.activity.tags', 'Activity')
    room = fields.Many2one('op.classroom', 'Home Room')
    room_weight = fields.Float('Home Room Weight Percent', default=100, size=100)
    set_of_room = fields.Many2many('op.classroom', string="Set of Home Rooms")
    set_of_room_weight = fields.Float('Set of Room Weight Percent', default=100, size=100)

    @api.multi
    @api.constrains('interval_end', 'interval_start')
    def check_interval_time(self):
        for t in self:
            if t.interval_end and t.interval_start and t.interval_end.sequence > t.interval_start.sequence:
                raise UserError(_("Interval End Time Should Be Greater"))

    @api.multi
    @api.constrains('weight_percent')
    def check_weight_percentage(self):
        for rec in self:
            if rec.weight_percent != 100:
                raise UserError(_("Please set the weight percentage to 100."))

    @api.multi
    @api.constrains('room_weight', 'set_of_room_weight')
    def check_room_weight(self):
        for w in self:
            if w.room_weight or w.set_of_room_weight > 100:
                raise UserError(_("Please set the weight percentage to 100 or below."))


class FacultyClassList(models.Model):
    _name = 'op.faculty.class.list'

    @api.multi
    @api.depends('subject_id', 'batch_id', 'activity_tag')
    def compute_name(self):
        for rec in self:
            if rec.id:
                rec.name = str(rec.id)+" - "+str(rec.duration)+" - "+str(rec.list_id.name)+" - "+str(rec.subject_id.name)+" - "+str(rec.activity_tag.name)+" - "+str(rec.batch_id.name)

    name = fields.Char("Name", readonly=1, compute='compute_name')
    list_id = fields.Many2one('op.faculty', 'Faculty Class')
    subject_id = fields.Many2one('op.subject', 'Subject', required=True)
    batch_id = fields.Many2one('op.batch', 'Batch Name', required=True)
    split = fields.Integer('Number of Classes Per Week', size=35)
    weight_percent = fields.Float('Weight %', default=100, size=100)
    duration = fields.Integer("Duration", default=1)
    activity_tag = fields.Many2many('op.activity.tags', string="Activity Tag")
