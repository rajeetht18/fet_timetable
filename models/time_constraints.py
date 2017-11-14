# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
from odoo.exceptions import UserError


class BatchConstraints(models.Model):
    _name = 'op.batch.constraints'
    _description = 'A Students set not available times'
    _rec_name = 'student_id'

    @api.model
    def create(self, values):
        if len(values['batch_constraints_line_ids']) == 0:
            raise UserError(_("Please configure Timetable Days to create your Batch Time Constraint."))
        res = super(BatchConstraints, self).create(values)
        return res

    @api.multi
    @api.constrains('weight')
    def check_weight_percentage(self):
        for rec in self:
            if rec.weight != 100:
                raise UserError(_("Please set the weight percentage to 100."))

    @api.model
    def default_line(self):
        period_list = []
        period_dict = {}
        day_config = self.env['timetable.days.config'].search([], order='id desc', limit=1)
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
    @api.constrains('batch_constraints_line_ids')
    def _check_batch_constraints_line(self):
        for record in self:
            flag = False
            for line in record.batch_constraints_line_ids:
                if line.monday != 0 and line.monday != 1:
                    flag = True
                if line.tuesday != 0 and line.tuesday != 1:
                    flag = True
                if line.wednesday != 0 and line.wednesday != 1:
                    flag = True
                if line.thursday != 0 and line.thursday != 1:
                    flag = True
                if line.friday != 0 and line.friday != 1:
                    flag = True
                if line.saturday != 0 and line.saturday != 1:
                    flag = True
                if line.sunday != 0 and line.sunday != 1:
                    flag = True
            if flag:
                raise UserError(_("Break value should be 1 or 0."))

    _sql_constraints = [
        ('unique_batch',
         'unique(student_id)', 'You cannot create a Batch Constraint again with the same batch!')]

    student_id = fields.Many2one('op.batch', "Batch", required=1)
    weight = fields.Integer("Weight Percentage", default=100)
    batch_constraints_line_ids = fields.One2many('op.breaks.constraints.line', 'batch_constraint_id', "Batch Constraints", default=default_line)


class BatchConstraintsLine(models.Model):
    _name = 'op.breaks.constraints.line'
    _description = 'Batch constraints Line'

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
    batch_constraint_id = fields.Many2one('op.batch.constraints', "Batch Constraints")



class ActivityStartingTime(models.Model):
    _name = 'op.activity.starting.time'
    _description = 'An activity has a set of preferred starting time.'
    _rec_name = 'activity_id'

    @api.model
    def create(self, values):
        if len(values['activity_starting_line_ids']) == 0:
            raise UserError(_("Please configure Timetable Days to create your Activity Starting Time."))
        res = super(ActivityStartingTime, self).create(values)
        return res

    @api.model
    def default_line(self):
        period_list = []
        period_dict = {}
        day_config = self.env['timetable.days.config'].search([], order='id desc', limit=1)
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
    @api.constrains('activity_starting_line_ids')
    def _check_activity_starting_time_line(self):
        for record in self:
            flag = False
            for line in record.activity_starting_line_ids:
                if line.monday != 0 and line.monday != 1:
                    flag = True
                if line.tuesday != 0 and line.tuesday != 1:
                    flag = True
                if line.wednesday != 0 and line.wednesday != 1:
                    flag = True
                if line.thursday != 0 and line.thursday != 1:
                    flag = True
                if line.friday != 0 and line.friday != 1:
                    flag = True
                if line.saturday != 0 and line.saturday != 1:
                    flag = True
                if line.sunday != 0 and line.sunday != 1:
                    flag = True
            if flag:
                raise UserError(_("The Value should be 1 or 0."))

    _sql_constraints = [
        ('unique_activity',
         'unique(activity_id)', 'The constraint for the selected activity already exist. Please select another activity!')]

    activity_id = fields.Many2one('op.faculty.class.list', "Activity", required=1)
    weight = fields.Integer("Weight Percentage", default=100)
    activity_starting_line_ids = fields.One2many('op.activity.starting.time.line', 'activity_starting_time_id', "Activity Startimg Time Line", default=default_line)


class ActivityStartingTimeLine(models.Model):
    _name = 'op.activity.starting.time.line'
    _description = 'Activity Starting Time Line'

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
    activity_starting_time_id = fields.Many2one('op.activity.starting.time', "Activity Starting Time")


class ActivityTimeSlots(models.Model):
    _name = 'op.activity.timeslots'
    _description = 'An activity has a set of preferred time slots.'
    _rec_name = 'activity_id'

    @api.model
    def create(self, values):
        if len(values['activity_timeslots_line_ids']) == 0:
            raise UserError(_("Please configure Timetable Days to create your activity time slots."))
        res = super(ActivityTimeSlots, self).create(values)
        return res

    @api.model
    def default_line(self):
        period_list = []
        period_dict = {}
        day_config = self.env['timetable.days.config'].search([], order='id desc', limit=1)
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
    @api.constrains('activity_timeslots_line_ids')
    def _check_activity_timeslots_line(self):
        for record in self:
            flag = False
            for line in record.activity_timeslots_line_ids:
                if line.monday != 0 and line.monday != 1:
                    flag = True
                if line.tuesday != 0 and line.tuesday != 1:
                    flag = True
                if line.wednesday != 0 and line.wednesday != 1:
                    flag = True
                if line.thursday != 0 and line.thursday != 1:
                    flag = True
                if line.friday != 0 and line.friday != 1:
                    flag = True
                if line.saturday != 0 and line.saturday != 1:
                    flag = True
                if line.sunday != 0 and line.sunday != 1:
                    flag = True
            if flag:
                raise UserError(_("The Value should be 1 or 0."))

    _sql_constraints = [
        ('unique_activity',
         'unique(activity_id)', 'The constraint for the selected activity already exist. Please select another activity!')]

    activity_id = fields.Many2one('op.faculty.class.list', "Activity", required=1)
    weight = fields.Integer("Weight Percentage", default=100)
    activity_timeslots_line_ids = fields.One2many('op.activity.timeslots.line', 'activity_timeslots_id', "Activity Time Slots Line", default=default_line)


class ActivityTimeSlotsLine(models.Model):
    _name = 'op.activity.timeslots.line'
    _description = 'Activity Time Slots Line'

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
    activity_timeslots_id = fields.Many2one('op.activity.timeslots', "Activity Time Slots")



class ActivitiesStartingTime(models.Model):
    _name = 'op.activities.starting.time'
    _description = 'A set of activities has a set of preferred starting times.'
    _rec_name = 'faculty_id'

    @api.model
    def create(self, values):
        if len(values['Activities_starting_time_line_ids']) == 0:
            raise UserError(_("Please configure Timetable Days to create your Activities Time Constraint."))
        res = super(ActivitiesStartingTime, self).create(values)
        return res

    @api.model
    def default_line(self):
        period_list = []
        period_dict = {}
        day_config = self.env['timetable.days.config'].search([], order='id desc', limit=1)
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
    @api.constrains('Activities_starting_time_line_ids')
    def _check_Activities_starting_time_line(self):
        for record in self:
            flag = False
            for line in record.Activities_starting_time_line_ids:
                if line.monday != 0 and line.monday != 1:
                    flag = True
                if line.tuesday != 0 and line.tuesday != 1:
                    flag = True
                if line.wednesday != 0 and line.wednesday != 1:
                    flag = True
                if line.thursday != 0 and line.thursday != 1:
                    flag = True
                if line.friday != 0 and line.friday != 1:
                    flag = True
                if line.saturday != 0 and line.saturday != 1:
                    flag = True
                if line.sunday != 0 and line.sunday != 1:
                    flag = True
            if flag:
                raise UserError(_("The value should be 1 or 0."))

    faculty_id = fields.Many2one('op.faculty',"Faculty")
    student_id = fields.Many2one('op.batch',"Students")
    subject_id = fields.Many2one('op.subject',"Subject")
    activity_tag_id = fields.Many2one('op.activity.tags',"Activity Tag")
    duration = fields.Integer("Duration",default=1)
    weight = fields.Integer("Weight Percentage",default=100)
    Activities_starting_time_line_ids = fields.One2many('op.activities.starting.time.line', 'activities_starting_time_id', "Activities Starting Time", default=default_line)


class ActivitiesStartingTimeLine(models.Model):
    _name = 'op.activities.starting.time.line'
    _description = 'Activities Starting Time Line'

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
    activities_starting_time_id = fields.Many2one('op.activities.starting.time', "Activity Time Slots")


class ActivitiesTimeSlots(models.Model):
    _name = 'op.activities.timeslots'
    _description = 'An activity has a set of preferred time slots.'
    _rec_name = 'faculty_id'

    @api.model
    def create(self, values):
        if len(values['activities_timeslots_line_ids']) == 0:
            raise UserError(_("Please configure Timetable Days to create your activity time slots."))
        res = super(ActivitiesTimeSlots, self).create(values)
        return res

    @api.model
    def default_line(self):
        period_list = []
        period_dict = {}
        day_config = self.env['timetable.days.config'].search([], order='id desc', limit=1)
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
    @api.constrains('activities_timeslots_line_ids')
    def _check_activities_timeslots_line(self):
        for record in self:
            flag = False
            for line in record.activities_timeslots_line_ids:
                if line.monday != 0 and line.monday != 1:
                    flag = True
                if line.tuesday != 0 and line.tuesday != 1:
                    flag = True
                if line.wednesday != 0 and line.wednesday != 1:
                    flag = True
                if line.thursday != 0 and line.thursday != 1:
                    flag = True
                if line.friday != 0 and line.friday != 1:
                    flag = True
                if line.saturday != 0 and line.saturday != 1:
                    flag = True
                if line.sunday != 0 and line.sunday != 1:
                    flag = True
            if flag:
                raise UserError(_("The Value should be 1 or 0."))

    faculty_id = fields.Many2one('op.faculty',"Faculty")
    student_id = fields.Many2one('op.batch',"Students")
    subject_id = fields.Many2one('op.subject',"Subject")
    activity_tag_id = fields.Many2one('op.activity.tags',"Activity Tag")
    duration = fields.Integer("Duration",default=1)
    weight = fields.Integer("Weight Percentage",default=100)
    activities_timeslots_line_ids = fields.One2many('op.activities.timeslots.line', 'activities_timeslots_id', "Activities Time Slots Line", default=default_line)


class ActivitiesTimeSlotsLine(models.Model):
    _name = 'op.activities.timeslots.line'
    _description = 'Activity Time Slots Line'

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
    activities_timeslots_id = fields.Many2one('op.activities.timeslots', "Activities Time Slots")
