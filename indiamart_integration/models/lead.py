# -*- coding: utf-8 -*-
from odoo import fields, models, api

class im_api_integration(models.Model):
    _name = "im.api.integration"
    _rec_name = "glusr_mobile"

    glusr_mobile = fields.Char("GLUSR Mobile")
    glusr_mobile_key = fields.Char("GLUSR Mobile Key")
    timestamp_bool = fields.Boolean("Time Stamp")
    date1 = fields.Date("Start Date")
    date2 = fields.Date("End Date")
    time1 = fields.Datetime("Start Date")
    time2 = fields.Datetime("End Date")


class CRMLead(models.Model):
    _inherit = 'crm.lead'

    def _call_lead_api(self):
        print("HEylooooo..!!!!")
        self.env['im.api.fetchlead'].call_url()