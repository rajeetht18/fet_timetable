# -*- coding: utf-8 -*-
from odoo import api,fields,models

class Buildings(models.Model):
    _name = 'op.buildings'
    _description = 'Buildings'

    name = fields.Char("Name", required=True)
    code = fields.Char("Code")


class OpClassroom(models.Model):
    _inherit = 'op.classroom'

    building = fields.Many2one('op.buildings',"Building")


class OpTiming(models.Model):
    _inherit = 'op.timing'

    is_break = fields.Boolean("Break")


class OpActivityTags(models.Model):
    _name = 'op.activity.tags'

    name = fields.Char("Tag")
    description = fields.Char("Description")

class OpSubject(models.Model):
    _inherit = 'op.subject'

    tag_id = fields.Many2one('op.activity.tags',"Activity Tags")
