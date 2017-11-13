# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StudentCourse(models.Model):
    _inherit = 'op.student.course'

    group_id = fields.Many2one('op.batch.group', 'Group')
    subgroup_id = fields.Many2one('op.batch.subgroup', 'Subgroup')


class Faculty(models.Model):
    _inherit = 'op.faculty'

    class_details = fields.One2many('op.faculty.class.list', 'list_id', string="Splits")
    weight_percent = fields.Float('Weight %', default=100, size=100)
    max_days = fields.Integer('Max days Per Week', size=10)
    min_days = fields.Integer('Min days Per Week', size=10)
    max_gaps = fields.Integer('Max gaps Per Day', size=10)
    min_gaps = fields.Integer('Min gaps per Day', size=10)
    max_hrs = fields.Float('Max Hours', size=60)
    max_hrs_act = fields.Float('Max Hours with Activity', size=60)
    min_hrs = fields.Float('Min Hours Daily', size=18)
    max_hrs_cont = fields.Float('Max Hours Continuously', size=18)
    max_hr_cont_act = fields.Float('Max Hours Continuous with Activity', size=20)
    activity_name = fields.Many2one('op.activity.tags', 'Activity')

class FacultyClassList(models.Model):
    _name = 'op.faculty.class.list'

    list_id = fields.Many2one('op.faculty', 'Faculty Class')
    subject_id = fields.Many2one('op.subject', 'Subject', required=True)
    batch_id = fields.Many2one('op.batch', 'Batch Name', required=True)
    split = fields.Integer('Number of Classes Per Week', size=35)
    weight_percent = fields.Float('Weight %', default=100, size=100)
    activity_tag = fields.Many2many('op.activity.tags', string="Activity Tag")
