# -*- coding: utf-8 -*-

from odoo import fields, models, api

TIMETABLE_DAYS = ['tt_monday', 'tt_tuesday', 'tt_wednesday', 'tt_thursday', 'tt_friday', 'tt_saturday', 'tt_sunday']
WEEK_DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


class ResCompany(models.Model):
    _inherit = "res.company"

    @api.one
    @api.depends('tt_monday', 'tt_tuesday', 'tt_wednesday', 'tt_thursday', 'tt_friday', 'tt_saturday', 'tt_sunday')
    def _compute_timetable_max_days(self):
        self.tt_max_days = sum([1 for d in TIMETABLE_DAYS if getattr(self, d)])

    tt_max_days = fields.Integer("TimeTable Max Days", compute='_compute_timetable_max_days')
    tt_monday = fields.Boolean("Monday")
    tt_tuesday = fields.Boolean("Tuesday")
    tt_wednesday = fields.Boolean("Wednesday")
    tt_thursday = fields.Boolean("Thursday")
    tt_friday = fields.Boolean("Friday")
    tt_saturday = fields.Boolean("Saturday")
    tt_sunday = fields.Boolean("Sunday")
