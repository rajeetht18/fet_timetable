# -*- coding: utf-8 -*-
from odoo import api,fields,models

class Buildings(models.Model):
    _name = 'op.buildings'
    _description = 'Buildings'

    name = fields.Char("Name", required=True)
    code = fields.Char("Code")


class Classroom(models.Model):
    _inherit = 'op.classroom'

    building = fields.Many2one('op.buildings',"Building")


class ActivityTags(models.Model):
    _name = 'op.activity.tags'

    name = fields.Char("Tag", required=True)
    description = fields.Char("Description")


class Batch(models.Model):
    _inherit = 'op.batch'

    group_ids = fields.Many2many('op.batch.group', string="Group")
    

class BatchGroup(models.Model):
    _name = 'op.batch.group'

    name = fields.Char('Name', required=True)
    description = fields.Text()
    subgroup_ids = fields.Many2many('op.batch.subgroup', string='Subgroups')


class BatchSubgroup(models.Model):
    _name = 'op.batch.subgroup'

    name = fields.Char('Name', required=True)
    description = fields.Text()

