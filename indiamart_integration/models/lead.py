# -*- coding: utf-8 -*-
from odoo import fields, models, api
from . import controllers as cr

class im_api_integration(models.Model):
    _name = "im.api.integration"
    _rec_name = "glusr_mobile"

    glusr_mobile = fields.Char("GLUSR Mobile")
    glusr_mobile_key = fields.Char("GLUSR Mobile Key")


class CRMLead(models.Model):
    _inherit = 'crm.lead'

    def _call_lead_api(self):
        print("HEylooooo..!!!!")
        cr.FetchLead()