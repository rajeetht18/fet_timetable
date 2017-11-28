# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ActivityEndsDay(models.Model):
    _name = 'op.activity.ends.day'
    _description = 'An Activity ends a Students day.'
    _rec_name = 'activity_id'

    # @api.multi
    # @api.constrains('activity_id')
    # def check_activity(self):
    #     for rec in self:
    #         activity_count = self.env['op.activity.ends.day'].search_count([('activity_id','=',rec.activity_id.id)])
    #         if activity_count > 1:
    #             raise UserError(_("This activity is already selected. Please select another activity."))

    activity_id = fields.Many2one(
        'op.faculty.class.list', "Activity", required=1)
    weight = fields.Integer("Weight Percentage", default=100)


class ActivitiesEndsDay(models.Model):
    _name = 'op.activities.ends.day'
    _description = 'A set of Activities ends a Students day.'
    _rec_name = 'faculty_id'

    faculty_id = fields.Many2one('op.faculty', "Faculty", required=1)
    student_id = fields.Many2one('op.batch', "Students", required=1)
    subject_id = fields.Many2one('op.subject', "Subject", required=1)
    activity_tag_id = fields.Many2one(
        'op.activity.tags', "Activity Tag", required=1)
    weight = fields.Integer("Weight Percentage", default=100, required=1)


class ActivitiesSameStartingTime(models.Model):
    _name = 'op.activities.same.starting.time'
    _description = 'A set of Activities has same starting time.'
    _rec_name = 'weight'

    activities_ids = fields.Many2many(
        'op.faculty.class.list', 'activity_sametime_rel', 'activity_id', 'sametime_id', "Activities", required=1)
    weight = fields.Integer("Weight Percentage", default=100, required=1)


class ActivitiesSameStartingDay(models.Model):
    _name = 'op.activities.same.starting.day'
    _description = 'A set of Activities has same starting day.'
    _rec_name = 'weight'

    activities_ids = fields.Many2many(
        'op.faculty.class.list', 'activity_sameday_rel', 'activity_id', 'sameday_id', "Activities", required=1)
    weight = fields.Integer("Weight Percentage", default=100, required=1)


class ActivitiesSameStartingHour(models.Model):
    _name = 'op.activities.same.starting.hour'
    _description = 'A set of Activities has same starting hour.'
    _rec_name = 'weight'

    activities_ids = fields.Many2many(
        'op.faculty.class.list', 'activity_samehour_rel', 'activity_id', 'samehour_id', "Activities", required=1)
    weight = fields.Integer("Weight Percentage", default=100, required=1)


class ActivitiesMaxOccupyTimeSlots(models.Model):
    _name = 'op.activities.max.time.slots'
    _description = 'A set of Activities occupies max time slots from selection'
    _rec_name = 'weight'

    @api.multi
    def set_not_available(self):
        day_config = self.env['res.company'].search(
            [('id', '=', self.env.user.company_id.id)])
        if day_config:
            for l in self.activities_max_timeslots_line_ids:
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
            for l in self.activities_max_timeslots_line_ids:
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
        if len(values['activities_max_timeslots_line_ids']) == 0:
            raise UserError(
                _("Please configure Timetable Days to create your activity time slots."))
        res = super(ActivitiesMaxOccupyTimeSlots, self).create(values)
        return res

    @api.model
    def default_line(self):
        period_list = []
        period_dict = {}
        day_config = self.env['timetable.days.config'].search(
            [], order='id desc', limit=1)
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
    @api.constrains('activities_max_timeslots_line_ids')
    def _check_subactivities_timeslots_line(self):
        for record in self:
            flag = False
            for line in record.activities_max_timeslots_line_ids:
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

    @api.multi
    @api.constrains('max_occupied')
    def _check_max_occupied(self):
        for rec in self:
            if rec.max_occupied < 1:
                raise UserError(
                    _("The Max occuppied value should be greater than 0."))

    activities_ids = fields.Many2many('op.faculty.class.list', 'activity_maxtimeslot_rel',
                                      'activity_id', 'maxtimeslot_id', "Activities", required=1)
    weight = fields.Integer("Weight Percentage", default=100, required=1)
    max_occupied = fields.Integer("maximum Occuppied", default=1, required=1)
    activities_max_timeslots_line_ids = fields.One2many(
        'op.activities.max.time.slots.line', 'activities_max_timeslots_id', "Activities Max Time Slots Line", default=default_line)


class ActivitiesMaxOccupyTimeSlotsLine(models.Model):
    _name = 'op.activities.max.time.slots.line'
    _description = 'Max activities Time Slots Line'

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
    activities_max_timeslots_id = fields.Many2one(
        'op.activities.max.time.slots', "Activities Max Time Slots")


class TwoActivitiesOrdered(models.Model):
    _name = 'op.two_activities.ordered'
    _description = 'Two activities are ordered'
    _rec_name = 'weight'

    @api.multi
    @api.constrains('activities_ids')
    def _check_min_gap(self):
        for rec in self:
            if len(rec.activities_ids) != 2:
                raise UserError(
                    _("Please make sure you've added 2 activities."))

    activities_ids = fields.Many2many(
        'op.faculty.class.list', 'activity_ordered_rel', 'activity_id', 'ordered_id', "Activities", required=1)
    weight = fields.Integer("Weight Percentage", default=100, required=1)


class TwoActivitiesConsecutive(models.Model):
    _name = 'op.two_activities.consecutive'
    _description = 'Two activities are consecutive'
    _rec_name = 'weight'

    @api.multi
    @api.constrains('activities_ids')
    def _check_min_gap(self):
        for rec in self:
            if len(rec.activities_ids) != 2:
                raise UserError(
                    _("Please make sure you've added 2 activities."))

    activities_ids = fields.Many2many('op.faculty.class.list', 'activity_consecutive_rel',
                                      'activity_id', 'consecutive_id', "Activities", required=1)
    weight = fields.Integer("Weight Percentage", default=100, required=1)


class TwoActivitiesGrouped(models.Model):
    _name = 'op.two_activities.grouped'
    _description = 'Two activities are grouped'
    _rec_name = 'weight'

    @api.multi
    @api.constrains('activities_ids')
    def _check_min_gap(self):
        for rec in self:
            if len(rec.activities_ids) != 2:
                raise UserError(
                    _("Please make sure you've added 2 activities."))

    activities_ids = fields.Many2many(
        'op.faculty.class.list', 'two_activity_grouped_rel', 'activity_id', 'grouped_id', "Activities", required=1)
    weight = fields.Integer("Weight Percentage", default=100, required=1)


class ThreeActivitiesGrouped(models.Model):
    _name = 'op.three_activities.grouped'
    _description = 'Three activities are grouped'
    _rec_name = 'weight'

    @api.multi
    @api.constrains('activities_ids')
    def _check_min_gap(self):
        for rec in self:
            if len(rec.activities_ids) != 3:
                raise UserError(
                    _("Please make sure you've added 3 activities."))

    activities_ids = fields.Many2many(
        'op.faculty.class.list', 'three_activity_grouped_rel', 'activity_id', 'grouped_id', "Activities", required=1)
    weight = fields.Integer("Weight Percentage", default=100, required=1)


class ActivitiesNotOverlapping(models.Model):
    _name = 'op.activities.not_overlap'
    _description = 'A set of activities not overlap'
    _rec_name = 'weight'

    activities_ids = fields.Many2many('op.faculty.class.list', 'activities_not_overlap_rel',
                                      'activity_id', 'not_overlap_id', "Activities", required=1)
    weight = fields.Integer("Weight Percentage", default=100, required=1)


class ActivitiesMaxSimultaneous(models.Model):
    _name = 'op.activities.max.simultaneous'
    _description = 'Maximum simulatneous activities from a selected time slot'
    _rec_name = 'weight'

    @api.multi
    def set_not_available(self):
        day_config = self.env['res.company'].search(
            [('id', '=', self.env.user.company_id.id)])
        if day_config:
            for l in self.activities_max_simultaneous_line_ids:
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
            for l in self.activities_max_simultaneous_line_ids:
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
        if len(values['activities_max_simultaneous_line_ids']) == 0:
            raise UserError(
                _("Please configure Timetable Days to create your activity time slots."))
        res = super(ActivitiesMaxSimultaneous, self).create(values)
        return res

    @api.model
    def default_line(self):
        period_list = []
        period_dict = {}
        day_config = self.env['timetable.days.config'].search(
            [], order='id desc', limit=1)
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
    @api.constrains('activities_max_simultaneous_line_ids')
    def _check_activities_max_simultaneous_line(self):
        for record in self:
            flag = False
            for line in record.activities_max_simultaneous_line_ids:
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

<<<<<<< HEAD
=======
    activities_ids = fields.Many2many(
        'op.faculty.class.list', 'activity_maxtimeslot_rel', 'activity_id', 'maxtimeslot_id', "Activities")
    weight = fields.Integer("Weight Percentage", default=100, readonly=1)
    max_occupied = fields.Integer("maximum Occuppied")
>>>>>>> a144d413c86fe269dd82413478c69bb5facf342b

    @api.multi
    @api.constrains('activities_ids')
    def _check_activities(self):
        for rec in self:
            if len(rec.activities_ids) == 1:
                raise UserError(_("Please add atleast two activities."))

    @api.multi
    @api.constrains('max_simultaneous')
    def _check_max_simultaneous(self):
        for rec in self:
            if rec.max_simultaneous < 1:
                raise UserError(_("Please add value more than zero."))

    activities_ids = fields.Many2many(
        'op.faculty.class.list', 'activity_maxsimul_rel', 'activity_id', 'maxsimul_id', "Activities", required=1)
    weight = fields.Integer("Weight Percentage",
                            default=100, readonly=1, required=1)
    max_simultaneous = fields.Integer(
        "Maximum Simultaneous", default=1, required=1)
    activities_max_simultaneous_line_ids = fields.One2many(
        'op.activities.max.simultaneous.line', 'activities_max_simultaneous_id', "Activities Max Simultaneous Line", default=default_line)


class ActivitiesMaxOccupyTimeSlotsLine(models.Model):
    _name = 'op.activities.max.simultaneous.line'
    _description = 'Activities Max Simultaneous Slots Line'

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
    activities_max_simultaneous_id = fields.Many2one(
        'op.activities.max.simultaneous', "Activities Max Simultaneous Time Slots")


class ActivitiesMinGap(models.Model):
    _name = 'op.activities.min_gap'
    _description = 'Minimum gap between activities'
    _rec_name = 'weight'

    @api.multi
    @api.constrains('min_gap')
    def _check_min_gap(self):
        for rec in self:
            if rec.min_gap < 1:
                raise UserError(
                    _("The minimum gap value should be more than zero"))

    @api.multi
    @api.constrains('activities_ids')
    def _check_activities(self):
        for rec in self:
            if len(rec.activities_ids) == 1:
                raise UserError(_("Please add atleast two activities."))

<<<<<<< HEAD
=======
    activities_ids = fields.Many2many(
        'op.faculty.class.list', 'activity_mingap_rel', 'activity_id', 'mingap_id', "Activities")
    min_gap = fields.Integer("Minimum Gap", default=1)
    weight = fields.Integer("Weight Percentage", default=100)
>>>>>>> a144d413c86fe269dd82413478c69bb5facf342b
    activities_ids = fields.Many2many(
        'op.faculty.class.list', 'activity_mingap_rel', 'activity_id', 'mingap_id', "Activities", required=1)
    min_gap = fields.Integer("Minimum Gap", default=1, required=1)
    weight = fields.Integer("Weight Percentage", default=100)
<<<<<<< HEAD

=======
>>>>>>> a144d413c86fe269dd82413478c69bb5facf342b
