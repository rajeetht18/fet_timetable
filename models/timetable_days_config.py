# -*- coding: utf-8 -*-
from odoo import api, fields, models


class TimetableDaysConfig(models.TransientModel):
    _name = "timetable.days.config"
    _inherit = 'res.config.settings'

    def get_default_params(self, fields):
        res = {}
        for field_name in ['tt_monday', 'tt_tuesday', 'tt_wednesday', 'tt_thursday', 'tt_friday', 'tt_saturday', 'tt_sunday']:
            res[field_name] = self.env['ir.values'].get_default('timetable.days.config', field_name)
        return res

    @api.multi
    def set_timetable_defaults(self):
        self.env['ir.values'].sudo().set_default('timetable.days.config', 'tt_monday', self.tt_monday)
        self.env['ir.values'].sudo().set_default('timetable.days.config', 'tt_tuesday', self.tt_tuesday)
        self.env['ir.values'].sudo().set_default('timetable.days.config', 'tt_wednesday', self.tt_wednesday)
        self.env['ir.values'].sudo().set_default('timetable.days.config', 'tt_thursday', self.tt_thursday)
        self.env['ir.values'].sudo().set_default('timetable.days.config', 'tt_friday', self.tt_friday)
        self.env['ir.values'].sudo().set_default('timetable.days.config', 'tt_saturday', self.tt_saturday)
        self.env['ir.values'].sudo().set_default('timetable.days.config', 'tt_sunday', self.tt_sunday)
        return True

    tt_monday = fields.Boolean("Monday")
    tt_tuesday = fields.Boolean("Tuesday")
    tt_wednesday = fields.Boolean("Wednesday")
    tt_thursday = fields.Boolean("Thursday")
    tt_friday = fields.Boolean("Friday")
    tt_saturday = fields.Boolean("Saturday")
    tt_sunday = fields.Boolean("Sunday")
