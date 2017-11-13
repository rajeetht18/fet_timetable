# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FacultyactivityMaxhrs(models.Model):
    _name = 'op.faculty.activity.maxhrs'

    name = fields.Char('Name', default="Max Hrs With Activity For All Teachers")
    act_tag_name = fields.Many2one('op.activity.tags', 'Activity')
    weight_percent = fields.Float('Weight %', default=100, size=100)
    max_hrs_cont_tr_act = fields.Float('Max Hours Continuously with an activity For All Teachers')

    # _sql_constraints = [
    #     ('unique_activity',
    #      'unique(name)', 'You cannot create another Activity Constraint!')]
