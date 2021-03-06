# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from company import WEEK_DAYS


class SubActivityStartingTime(models.Model):
    _name = 'op.subactivity.starting.time'
    _description = 'A set of subactivity has a set of preferred starting Time.'
    _rec_name = 'faculty_id'

    @api.multi
    def set_not_available(self):
        day_config = self.env['res.company'].search(
            [('id', '=', self.env.user.company_id.id)])
        if day_config:
            for l in self.subactivity_starting_line_ids:
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
            for l in self.subactivity_starting_line_ids:
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
        if len(values['subactivity_starting_line_ids']) == 0:
            raise UserError(_("Please configure Timetable Days to create your Activity Starting Time."))
        starting_obj = self.env['op.faculty.class.list'].search([('list_id', '=', values['faculty_id']), ('batch_id', '=', values['student_id']), ('subject_id', '=', values['subject_id']), ('activity_tag', 'in', values['activity_tag_id'])])
        if not starting_obj:
            raise UserError(_("There is no activity for the given details. Please choose another!."))
        res = super(SubActivityStartingTime, self).create(values)
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
    @api.constrains('subactivity_starting_line_ids')
    def _check_room_not_available_line(self):
        for record in self:
            flag = any([True for line in record.subactivity_starting_line_ids for d in WEEK_DAYS if getattr(
                line, d) != 0 and getattr(line, d) != 1])
            if flag:
                raise UserError(_("The Value should be 1 or 0."))


    @api.onchange('faculty_id')
    def onchange_faculty(self):
        res = {}
        if self.faculty_id:
            sub_list = []
            batch_list = []
            tag_list = []
            obj = self.env['op.faculty.class.list'].search([('list_id','=',self.faculty_id.id)])
            for fac in obj:
                sub_list.append(fac.subject_id.id)
                batch_list.append(fac.batch_id.id)
                for tag in fac.activity_tag:
                    tag_list.append(tag.id)
            res['domain'] = {'subject_id': [('id', 'in', sub_list)],'student_id':[('id','in',batch_list)],'activity_tag_id':[('id','in',tag_list)]}
            self.subject_id = False
            self.student_id = False
            self.activity_tag_id = False
        return res

    @api.onchange('student_id')
    def onchange_batch(self):
        res = {}
        if self.student_id:
            ids = self.student_id.group_ids.mapped('id')
            res['domain'] = {'group_id': [('id', 'in', ids)]}
            self.group_id = False
            self.subgroup_id = False
        return res

    @api.onchange('group_id')
    def onchange_group(self):
        res = {}
        if self.group_id:
            ids = self.group_id.subgroup_ids.mapped('id')
            res['domain'] = {'subgroup_id': [('id', 'in', ids)]}
            self.subgroup_id = False
        return res

    faculty_id = fields.Many2one('op.faculty', "Faculty", required=1)
    student_id = fields.Many2one('op.batch', "Batch", required=1)
    subject_id = fields.Many2one('op.subject', "Subject", required=1)
    activity_tag_id = fields.Many2one(
        'op.activity.tags', "Activity Tag", required=1)
    weight = fields.Integer("Weight Percentage", default=100)
    split_count = fields.Integer("Split Component", default=1)
    group_id = fields.Many2one('op.batch.group', "Group")
    subgroup_id = fields.Many2one('op.batch.subgroup', "Subgroup")
    subactivity_starting_line_ids = fields.One2many(
        'op.subactivity.starting.time.line', 'subactivity_starting_time_id', "Subactivity Startimg Time Line", default=default_line)


class SubActivityStartingTimeLine(models.Model):
    _name = 'op.subactivity.starting.time.line'
    _description = 'Subactivity Starting Time Line'

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
    subactivity_starting_time_id = fields.Many2one(
        'op.subactivity.starting.time', "Subactivity Starting Time")


class SubActivitiesTimeSlots(models.Model):
    _name = 'op.subactivities.timeslots'
    _description = 'A set of subactivities has a set of preferred time slots.'
    _rec_name = 'faculty_id'

    @api.multi
    def set_not_available(self):
        day_config = self.env['res.company'].search(
            [('id', '=', self.env.user.company_id.id)])
        if day_config:
            for l in self.subactivities_timeslots_line_ids:
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
            for l in self.subactivities_timeslots_line_ids:
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
        if len(values['subactivities_timeslots_line_ids']) == 0:
            raise UserError(_("Please configure Timetable Days to create your activity time slots."))
        starting_obj = self.env['op.faculty.class.list'].search([('list_id', '=', values['faculty_id']), ('batch_id', '=', values['student_id']), ('subject_id', '=', values['subject_id']), ('activity_tag', 'in', values['activity_tag_id'])])
        if not starting_obj:
            raise UserError(_("There is no activity for the given details. Please choose another!."))
        res = super(SubActivitiesTimeSlots, self).create(values)
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
    @api.constrains('subactivities_timeslots_line_ids')
    def _check_room_not_available_line(self):
        for record in self:
            flag = any([True for line in record.subactivities_timeslots_line_ids for d in WEEK_DAYS if getattr(
                line, d) != 0 and getattr(line, d) != 1])
            if flag:
                raise UserError(_("The Value should be 1 or 0."))

    @api.onchange('faculty_id')
    def onchange_faculty(self):
        res = {}
        if self.faculty_id:
            sub_list = []
            batch_list = []
            tag_list = []
            obj = self.env['op.faculty.class.list'].search([('list_id','=',self.faculty_id.id)])
            for fac in obj:
                sub_list.append(fac.subject_id.id)
                batch_list.append(fac.batch_id.id)
                for tag in fac.activity_tag:
                    tag_list.append(tag.id)
            res['domain'] = {'subject_id': [('id', 'in', sub_list)],'student_id':[('id','in',batch_list)],'activity_tag_id':[('id','in',tag_list)]}
            self.subject_id = False
            self.student_id = False
            self.activity_tag_id = False
        return res

    @api.onchange('student_id')
    def onchange_batch(self):
        res = {}
        if self.student_id:
            ids = self.student_id.group_ids.mapped('id')
            res['domain'] = {'group_id': [('id', 'in', ids)]}
            self.group_id = False
            self.subgroup_id = False
        return res

    @api.onchange('group_id')
    def onchange_group(self):
        res = {}
        if self.group_id:
            ids = self.group_id.subgroup_ids.mapped('id')
            res['domain'] = {'subgroup_id': [('id', 'in', ids)]}
            self.subgroup_id = False
        return res

    faculty_id = fields.Many2one('op.faculty', "Faculty", required=1)
    student_id = fields.Many2one('op.batch', "Batch", required=1)
    subject_id = fields.Many2one('op.subject', "Subject", required=1)
    activity_tag_id = fields.Many2one(
        'op.activity.tags', "Activity Tag", required=1)
    weight = fields.Integer("Weight Percentage", default=100)
    split_count = fields.Integer("Split Component", default=1)
    group_id = fields.Many2one('op.batch.group', "Group")
    subgroup_id = fields.Many2one('op.batch.subgroup', "Subgroup")
    subactivities_timeslots_line_ids = fields.One2many(
        'op.subactivities.timeslots.line', 'subactivities_timeslots_id', "Subactivities Time Slots Line", default=default_line)


class SubActivitiesTimeSlotsLine(models.Model):
    _name = 'op.subactivities.timeslots.line'
    _description = 'SubActivity Time Slots Line'

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
    subactivities_timeslots_id = fields.Many2one(
        'op.subactivities.timeslots', "Subactivities Time Slots")


class MinDaysBetweenActivities(models.Model):
    _name = 'op.mindays.activities'
    _description = 'Minimum days between a set of activities.'
    _rec_name = 'min_days'

    @api.multi
    @api.constrains('activities_ids')
    def check_activity_count(self):
        for rec in self:
            if len(rec.activities_ids) == 1:
                raise UserError(_("Please add more than 1 activity."))

    @api.multi
    @api.constrains('min_days')
    def check_min_days_gap(self):
        for rec in self:
            if rec.min_days < 1:
                raise UserError(_("The gap should be greater than 0"))

    activities_ids = fields.Many2many('op.faculty.class.list', 'activity_mindays_rel', 'activity_id', 'minday_id', "Activities")
    min_days = fields.Integer("Minimum Days", default=1)
    same_day = fields.Boolean("Activities are on the same day")
    weight = fields.Integer("Weight Percentage", default=100)


class MaxDaysBetweenActivities(models.Model):
    _name = 'op.maxdays.activities'
    _description = 'Maximum days between a set of activities.'
    _rec_name = 'max_days'

    @api.multi
    @api.constrains('activities_ids')
    def check_activity_count(self):
        for rec in self:
            if len(rec.activities_ids) == 1:
                raise UserError(_("Please add more than 1 activity."))

    @api.multi
    @api.constrains('max_days')
    def check_max_days_gap(self):
        for rec in self:
            if rec.max_days < 1:
                raise UserError(_("The gap should be greater than 0"))

    activities_ids = fields.Many2many('op.faculty.class.list', 'activity_maxdays_rel', 'activity_id', 'maxday_id', "Activities")
    max_days = fields.Integer("Maximum Days", default=1)
    weight = fields.Integer("Weight Percentage", default=100)
