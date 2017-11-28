# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Buildings(models.Model):
    _name = 'op.buildings'
    _description = 'Buildings'

    name = fields.Char("Name", required=True)
    code = fields.Char("Code")


class Classroom(models.Model):
    _inherit = 'op.classroom'

    building = fields.Many2one('op.buildings', "Building")


class ActivityTags(models.Model):
    _name = 'op.activity.tags'

    name = fields.Char("Tag", required=True)
    description = fields.Char("Description")
    room_id = fields.Many2one('op.classroom', "Preferred Room")
    room_weight = fields.Integer("Weight Percentage", default=100)
    rooms_ids = fields.Many2many(
        'op.classroom', 'tag_room_rel', 'subject_id', 'room_id', "Preferred Rooms")
    rooms_weight = fields.Integer("Weight Percentage", default=100)


class Batch(models.Model):
    _inherit = 'op.batch'

    group_ids = fields.Many2many('op.batch.group', string="Group")


class BatchGroup(models.Model):
    _name = 'op.batch.group'

    name = fields.Char('Name', required=True)
    description = fields.Text("Description")
    subgroup_ids = fields.Many2many('op.batch.subgroup', string='Subgroups')


class BatchSubgroup(models.Model):
    _name = 'op.batch.subgroup'

    name = fields.Char('Name', required=True)
    description = fields.Text("Description")


class OpSubject(models.Model):
    _inherit = 'op.subject'

    tag_id = fields.Many2one('op.activity.tags', "Activity Tags")
    room_id = fields.Many2one('op.classroom', "Preferred Room")
    room_weight = fields.Integer("Weight Percentage", default=100)
    rooms_ids = fields.Many2many(
        'op.classroom', 'subjects_room_rel', 'subject_id', 'room_id', "Preferred Rooms")
    rooms_weight = fields.Integer("Weight Percentage", default=100)
