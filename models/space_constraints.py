# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from company import WEEK_DAYS


class RoomNotAvailableTimes(models.Model):
    _name = 'op.room.not.available'
    _description = 'A Rooms not available times'
    _rec_name = 'room_id'

    @api.multi
    def set_not_available(self):
        day_config = self.env['res.company'].search(
            [('id', '=', self.env.user.company_id.id)])
        if day_config:
            for l in self.room_not_available_line_ids:
                if day_config.tt_monday:
                    l.monday = 1
                if day_config.tt_tuesday:
                    l.tuesday = 1
                if day_config.tt_wednesday:
                    l.wednesday = 1
                if day_config.tt_thursday:
                    l.thursday = 1
                if day_config.tt_friday:
                    l.friday = 1
                if day_config.tt_saturday:
                    l.saturday = 1
                if day_config.tt_sunday:
                    l.sunday = 1

    @api.multi
    def set_available(self):
        day_config = self.env['res.company'].search(
            [('id', '=', self.env.user.company_id.id)])
        if day_config:
            for l in self.room_not_available_line_ids:
                if day_config.tt_monday:
                    l.monday = 0
                if day_config.tt_tuesday:
                    l.tuesday = 0
                if day_config.tt_wednesday:
                    l.wednesday = 0
                if day_config.tt_thursday:
                    l.thursday = 0
                if day_config.tt_friday:
                    l.friday = 0
                if day_config.tt_saturday:
                    l.saturday = 0
                if day_config.tt_sunday:
                    l.sunday = 0

    @api.model
    def create(self, values):
        if len(values['room_not_available_line_ids']) == 0:
            raise UserError(
                _("Please configure Timetable Days to create your activity time slots."))
        res = super(RoomNotAvailableTimes, self).create(values)
        return res

    @api.model
    def default_line(self):
        period_list = []
        period_dict = {}
        day_config = self.env['res.company'].search(
            [('id', '=', self.env.user.company_id.id)])
        for time in self.env['op.timing'].search([]):
            if day_config:
                period_dict = {
                    'name': time.name,
                    'is_monday': day_config.tt_monday,
                    'is_tuesday': day_config.tt_tuesday,
                    'is_wednesday': day_config.tt_wednesday,
                    'is_thursday': day_config.tt_thursday,
                    'is_friday': day_config.tt_friday,
                    'is_saturday': day_config.tt_saturday,
                    'is_sunday': day_config.tt_sunday
                }
                period_list.append((0, 0, period_dict))
        return period_list

    @api.multi
    @api.constrains('room_not_available_line_ids')
    def _check_room_not_available_line(self):
        for record in self:
            flag = any([True for line in record.room_not_available_line_ids for d in WEEK_DAYS if getattr(
                line, d) != 0 and getattr(line, d) != 1])
            if flag:
                raise UserError(_("The Value should be 1 or 0."))

    room_id = fields.Many2one('op.classroom', "Room", required=1)
    weight = fields.Integer("Weight Percentage", default=100, required=1)
    room_not_available_line_ids = fields.One2many(
        'op.room.not.available.line', 'room_not_available_id', "Room Not Available", default=default_line)


class RoomNotAvailableLine(models.Model):
    _name = 'op.room.not.available.line'
    _description = 'Room not available Line'

    name = fields.Char("Periods", required=1)
    monday = fields.Integer("Monday", size=1)
    tuesday = fields.Integer("Tuesday", size=1)
    wednesday = fields.Integer("Wednesday", size=1)
    thursday = fields.Integer("Thursday", size=1)
    friday = fields.Integer("Friday", size=1)
    saturday = fields.Integer("Saturday", size=1)
    sunday = fields.Integer("Sunday", size=1)
    is_monday = fields.Boolean("Monday?")
    is_tuesday = fields.Boolean("Tuesday?")
    is_wednesday = fields.Boolean("Wednesday?")
    is_thursday = fields.Boolean("Thursday?")
    is_friday = fields.Boolean("Friday?")
    is_saturday = fields.Boolean("Saturday?")
    is_sunday = fields.Boolean("Sunday?")
    room_not_available_id = fields.Many2one(
        'op.room.not.available', "Room not available line")


class ActivityRoom(models.Model):
    _name = 'op.activity.room'
    _description = 'An activity has a preferred room'
    _rec_name = 'weight'

    activity_id = fields.Many2one(
        'op.faculty.class.list', "Activity", required=1)
    room_id = fields.Many2one('op.classroom', "Preferred Room", required=1)
    weight = fields.Integer("Weight Percentage", default=100, required=1)
    locked = fields.Boolean("Permenantly Locked")


class ActivityRooms(models.Model):
    _name = 'op.activity.rooms'
    _description = 'An activity has a set of preferred room'
    _rec_name = 'weight'

    activity_id = fields.Many2one(
        'op.faculty.class.list', "Activity", required=1)
    room_ids = fields.Many2many('op.classroom', 'room_activity_rel',
                                'room_id', 'activity_id', "preferred Rooms", required=1)
    weight = fields.Integer("Weight Percentage", default=100, required=1)


class ConsecutiveActivitiesSameRoom(models.Model):
    _name = 'op.consecutive.activities.same.room'
    _description = 'A set of Activities are in the same room if they are consecutive.'
    _rec_name = 'weight'

    @api.multi
    @api.constrains('activities_ids')
    def _check_activities(self):
        for rec in self:
            if len(rec.activities_ids) == 1:
                raise UserError(_("Please add atleast two activities."))

    activities_ids = fields.Many2many(
        'op.faculty.class.list', 'activity_sameroom_rel', 'activity_id', 'sameroom_id', "Activities", required=1)
    weight = fields.Integer("Weight Percentage", default=100, required=1)


class ActivitiesMaxDifferentRoom(models.Model):
    _name = 'op.activities.max.different.room'
    _description = 'A set of Activities are in the same room if they are consecutive.'
    _rec_name = 'weight'

    @api.multi
    @api.constrains('activities_ids')
    def _check_activities(self):
        for rec in self:
            if len(rec.activities_ids) == 1:
                raise UserError(_("Please add atleast two activities."))

    @api.multi
    @api.constrains('max_diff_room')
    def _check_diff_rooms(self):
        for rec in self:
            if rec.max_diff_room < 1:
                raise UserError(
                    _("Maximum different room value should be more than zero."))

    activities_ids = fields.Many2many(
        'op.faculty.class.list', 'activity_diffroom_rel', 'activity_id', 'diffroom_id', "Activities", required=1)
    max_diff_room = fields.Integer(
        "Max Different Rooms", required=1, default=1)
    weight = fields.Integer("Weight Percentage", default=100, required=1)


class SubjectTagPreferredRoom(models.Model):
    _name = 'op.subject.tag.preferred.room'
    _description = 'A subject and activity tag has a preferred room.'
    _rec_name = 'weight'

    subject_id = fields.Many2one('op.subject', "Subject", required=1)
    activity_tag_id = fields.Many2one(
        'op.activity.tags', "Activity Tag", required=1)
    room_id = fields.Many2one('op.classroom', "Preferred Room", required=1)
    weight = fields.Integer("Weight Percentage", default=100, required=1)


class SubjectTagPreferredRooms(models.Model):
    _name = 'op.subject.tag.preferred.rooms'
    _description = 'A subject and activity tag has a set of preferred rooms.'
    _rec_name = 'weight'

    subject_id = fields.Many2one('op.subject', "Subject", required=1)
    activity_tag_id = fields.Many2one(
        'op.activity.tags', "Activity Tag", required=1)
    room_ids = fields.Many2many('op.classroom', 'room_subject_rel',
                                'room_id', 'subjecttag_id', "preferred Rooms", required=1)
    weight = fields.Integer("Weight Percentage", default=100, required=1)
