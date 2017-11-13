# -*- coding: utf-8 -*-
from odoo import models, fields


class Timeconstraints(models.Model):
    _inherit = 'op.faculty'

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
