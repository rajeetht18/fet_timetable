# -*- coding: utf-8 -*-
from odoo import api, fields, models
from company import TIMETABLE_DAYS


class TimetableDaysConfig(models.TransientModel):
    _name = "timetable.days.config"
    _inherit = 'res.config.settings'

    def get_default_params(self, fields):
        res = {}
        for day in TIMETABLE_DAYS:
            res[day] = self.env['ir.values'].get_default('timetable.days.config', day)
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

    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.user.company_id)
    tt_monday = fields.Boolean(related='company_id.tt_monday', string="Monday")
    tt_tuesday = fields.Boolean(related='company_id.tt_tuesday', string="Tuesday")
    tt_wednesday = fields.Boolean(related='company_id.tt_wednesday', string="Wednesday")
    tt_thursday = fields.Boolean(related='company_id.tt_thursday', string="Thursday")
    tt_friday = fields.Boolean(related='company_id.tt_friday', string="Friday")
    tt_saturday = fields.Boolean(related='company_id.tt_saturday', string="Saturday")
    tt_sunday = fields.Boolean(related='company_id.tt_sunday', string="Sunday")
