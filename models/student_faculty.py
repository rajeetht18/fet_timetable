# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StudentCourse(models.Model):
    _inherit = 'op.student.course'

    group_id = fields.Many2one('op.batch.group', 'Group')
    subgroup_id = fields.Many2one('op.batch.subgroup', 'Subgroup')


class Faculty(models.Model):
    _inherit = 'op.faculty'

    class_details = fields.One2many('op.faculty.class.list', 'list_id', string="Splits")


class FacultyClassList(models.Model):
    _name = 'op.faculty.class.list'

    list_id = fields.Many2one('op.faculty', 'Faculty Class')
    subject_id = fields.Many2one('op.subject', 'Subject', required=True)
    batch_id = fields.Many2one('op.batch', 'Batch Name', required=True)
    split = fields.Integer('Number of Classes Per Week', size=35)
    weight_percent = fields.Float('Weight %', default=100, size=100)
    activity_tag = fields.Many2many('op.activity.tags', string="Activity Tag")
