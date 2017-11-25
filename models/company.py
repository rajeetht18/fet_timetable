# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = "res.company"

    tt_monday = fields.Boolean("Monday")
    tt_tuesday = fields.Boolean("Tuesday")
    tt_wednesday = fields.Boolean("Wednesday")
    tt_thursday = fields.Boolean("Thursday")
    tt_friday = fields.Boolean("Friday")
    tt_saturday = fields.Boolean("Saturday")
    tt_sunday = fields.Boolean("Sunday")
