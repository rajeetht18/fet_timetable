# -*- coding: utf-8 -*-
from odoo import api, fields, models
from lxml import etree
# import base64
# import datetime


class time_data_import(models.TransientModel):
    _inherit = 'fettimetable.data.export'

    def constraint_compulsory(self, root):
        time = etree.SubElement(root, "Time_Constraints_List")
        compulsory = etree.SubElement(time, "ConstraintBasicCompulsoryTime")
        weight = etree.SubElement(compulsory, "Weight_Percentage")
        weight.text = "100"
        active = etree.SubElement(compulsory, "Active")
        active.text = "True"

    # Faculty Constraints
        availability = self.faculty_notavailable(time)
        max_day = self.faculty_maxday_constraint(time)
        min_day = self.faculty_minday_constraint(time)  # fix: depends on no.of activities and
        max_gaps = self.faculty_maxgap_day(time)
        max_gaps_week = self.faculty_gapweek_constraint(time)
        maxhr = self.faculty_maxhr_daily_constraint(time)
        minhr_daily = self.faculty_minhr_daily_constraint(time)
        maxhr_cont = self.faculty_maxhr_cont_constraint(time)
        max_hr_cont_act = self.faculty_maxhr_activity_constraint(time)  # need to fix: fet rejecting
        faculty_interval = self.faculty_interval_maxdays_constraint(time)
        faculties_maxday = self.faculties_maxday(time)
        faculties_minday = self.faculties_minday(time)
        faculties_maxgap = self.faculties_maxgap(time)
        faculties_maxgap_week = self.faculties_maxgap_week(time)
        maxhr_daily = self.faculties_maxhrs(time)
        max_hrs_cont = self.faculties_maxhrs_cont(time)
        min_hrs = self.faculties_minhrs(time)
        faculties_maxhr = self.faculties_maxhr_activity(time)
        faculties_interval = self.faculties_hr_activity(time)

    # Student Time Constraints
        student_notavailable = self.student_notavailable(time)  # fix: groups and subgroups added
        student_maxday = self.student_maxday_constraint(time)
        student_maxgap_day = self.student_maxgap_day(time)
        student_maxgap_week = self.student_maxgap_week(time)
        student_secondhr = self.student_maxsecond(time)
        student_maxhr_daily = self.student_maxhr_daily(time)
        student_minhr_daily = self.student_minhr_daily(time)
        student_maxhr_cont = self.student_maxhr_cont(time)
        student_maxhr_actiivty = self.student_maxhr_activity(time)
        student_maxhr_act = self.student_maxhr_cont_daily(time)
        student_interval = self.student_set_interval(time)
        allstudents_maxday = self.allstudent_maxday_constraint(time)
        allstudent_maxgap = self.allstudent_maxgap_day(time)
        allstudent_week_maxgap = self.allstudent_maxgap_week(time)
        allstudent_maxhr_second = self.allstudent_maxsecond(time)
        allstudent_maxhr_daily = self.allstudent_maxhr_daily(time)
        allstudent_max_hr = self.allstudent_maxhr_cont(time)
        allstudents_act_cont = self.allstudent_maxhr_activity(time)
        allstudents_maxhr_act_cont = self.allstudent_maxhr_act_cont(time)
        allstudent_interval = self.allstudent_set_interval(time)
        allstudent_minhr_daily = self.allstudent_minhr_daily(time)

    # Time activity constraints
        break_time = self.break_time(time)
        activity_preferred_starting_time = self.preferred_starting_time(time)  # need fix: no activities matching in fet
        preferred_starting_times = self.preferred_starting_times(time)
        preferred_timeslots = self.preferred_timeslots(time)
        activities_preferredtimes = self.activities_preferredtimes(time)
        activities_preferred_timeslots = self.activities_preferred_timeslots(time)
        subactivities_preferredtimes = self.subactivities_preferredtimes(time)  # need fix: add subactivity
        subactivities_preferred_timeslots = self.subactivities_preferred_timeslots(time)  # need fix: add subactivity
        min_days_activities = self.min_days_activities(time)
        max_days_activities = self.max_days_activities(time)
        activity_ends_studentsday = self.activity_ends_studentsday(time)
        activities_ends_studentsday = self.activities_ends_studentsday(time)
        activities_same_startingDH = self.activities_same_startingDH(time)
        activities_same_startingH = self.activities_same_startingH(time)
        activities_same_startingD = self.activities_same_startingD(time)
        activities_max_timeslots = self.activities_max_timeslots(time)
        two_activities_ordered = self.two_activities_ordered(time)
        two_activities_consecutives = self.two_activities_consecutives(time)
        two_activities_grouped = self.two_activities_grouped(time)
        three_activities_grouped = self.three_activities_grouped(time)  # fix needed: actitivitis not accepting
        activities_not_overlapping = self.activities_not_overlapping(time)
        max_simultaneous_activities = self.max_simultaneous_activities(time)
        activities_min_gap = self.activities_min_gap(time)

    def faculty_notavailable(self, time):
        faculty = self.env['op.faculty.not.available'].search([])
        for w in faculty:
            week_days = etree.SubElement(time, "ConstraintTeacherNotAvailableTimes")
            weight = etree.SubElement(week_days, "Weight_Percentage")
            weight_per = w.weight_percent
            fac_name = w.name.name
            if w.name.middle_name:
                fac_name = '%s %s' % (fac_name, w.name.middle_name)
            if w.name.last_name:
                fac_name = '%s %s' % (fac_name, w.name.last_name)
            weight.text = str(weight_per)
            Name = etree.SubElement(week_days, "Teacher")
            Name.text = fac_name
            fac_time = self.env['op.faculty.not.available.list'].search(
                [('faculty_id', '=', w.id)])
            count = 0
            for t in fac_time:
                if t.monday == 1:
                    not_available = etree.SubElement(
                        week_days, "Not_Available_Time")
                    not_available_day = etree.SubElement(not_available, "Day")
                    not_available_day.text = 'Monday'
                    count += 1
                    hour = etree.SubElement(not_available, "Hour")
                    hour.text = t.name
                if t.tuesday == 1:
                    not_available = etree.SubElement(
                        week_days, "Not_Available_Time")
                    not_available_day = etree.SubElement(not_available, "Day")
                    not_available_day.text = 'Tuesday'
                    count += 1
                    hour = etree.SubElement(not_available, "Hour")
                    hour.text = t.name
                if t.wednesday == 1:
                    not_available = etree.SubElement(
                        week_days, "Not_Available_Time")
                    not_available_day = etree.SubElement(not_available, "Day")
                    not_available_day.text = 'Wednesday'
                    count += 1
                    hour = etree.SubElement(not_available, "Hour")
                    hour.text = t.name
                if t.thursday == 1:
                    not_available = etree.SubElement(
                        week_days, "Not_Available_Time")
                    not_available_day = etree.SubElement(not_available, "Day")
                    not_available_day.text = 'Thursday'
                    count += 1
                    hour = etree.SubElement(not_available, "Hour")
                    hour.text = t.name
                if t.friday == 1:
                    not_available = etree.SubElement(
                        week_days, "Not_Available_Time")
                    not_available_day = etree.SubElement(not_available, "Day")
                    not_available_day.text = 'Friday'
                    count += 1
                    hour = etree.SubElement(not_available, "Hour")
                    hour.text = t.name
                if t.saturday == 1:
                    not_available = etree.SubElement(
                        week_days, "Not_Available_Time")
                    not_available_day = etree.SubElement(not_available, "Day")
                    not_available_day.text = 'Saturday'
                    count += 1
                    hour = etree.SubElement(not_available, "Hour")
                    hour.text = t.name
                if t.sunday == 1:
                    not_available = etree.SubElement(
                        week_days, "Not_Available_Time")
                    not_available_day = etree.SubElement(not_available, "Day")
                    not_available_day.text = 'Sunday'
                    count += 1
                    hour = etree.SubElement(not_available, "Hour")
                    hour.text = t.name
            Number = etree.SubElement(week_days, "Number_of_Not_Available_Times")
            Number.text = str(count)
            active = etree.SubElement(week_days, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def faculty_maxday_constraint(self, time):
        faculty = self.env['op.faculty'].search([])
        for w in faculty:
            if w.max_days > 0:
                week_days = etree.SubElement(
                    time, "ConstraintTeacherMaxDaysPerWeek")
                weight = etree.SubElement(week_days, "Weight_Percentage")
                weight_per = w.weight_percent
                fac_name = w.name
                if w.middle_name:
                    fac_name = '%s %s' % (fac_name, w.middle_name)
                if w.last_name:
                    fac_name = '%s %s' % (fac_name, w.last_name)
                weight.text = str(weight_per)
                Name = etree.SubElement(week_days, "Teacher_Name")
                Name.text = fac_name
                max_day = etree.SubElement(week_days, "Max_Days_Per_Week")
                max_days = w.max_days
                max_day.text = str(max_days)
                active = etree.SubElement(week_days, "Active")
                active.text = "True"
                # comment = etree.SubElement(week_days, "Comments")
                # comment.text = "0"

    def faculty_minday_constraint(self, time):
        faculty = self.env['op.faculty'].search([])
        for w in faculty:
            if w.min_days > 0:
                week_days = etree.SubElement(
                    time, "ConstraintTeacherMinDaysPerWeek")
                weight = etree.SubElement(week_days, "Weight_Percentage")
                weight_per = w.weight_percent
                fac_name = w.name
                if w.middle_name:
                    fac_name = '%s %s' % (fac_name, w.middle_name)
                if w.last_name:
                    fac_name = '%s %s' % (fac_name, w.last_name)
                weight.text = str(weight_per)
                Name = etree.SubElement(week_days, "Teacher_Name")
                Name.text = fac_name
                min_day = etree.SubElement(week_days, "Minimum_Days_Per_Week")
                min_days = w.min_days
                min_day.text = str(min_days)
                active = etree.SubElement(week_days, "Active")
                active.text = "True"
                comment = etree.SubElement(week_days, "Comments")
                comment.text = '0'

    def faculty_maxgap_day(self, time):
        faculty = self.env['op.faculty'].search([])
        for w in faculty:
            if w.max_gaps > 0:
                week_days = etree.SubElement(
                    time, "ConstraintTeacherMaxGapsPerDay")
                weight = etree.SubElement(week_days, "Weight_Percentage")
                weight_per = w.weight_percent
                fac_name = w.name
                if w.middle_name:
                    fac_name = '%s %s' % (fac_name, w.middle_name)
                if w.last_name:
                    fac_name = '%s %s' % (fac_name, w.last_name)
                weight.text = str(weight_per)
                Name = etree.SubElement(week_days, "Teacher_Name")
                Name.text = fac_name
                maxgap_day = etree.SubElement(week_days, "Max_Gaps")
                maxgap_days = w.max_gaps
                maxgap_day.text = str(maxgap_days)
                active = etree.SubElement(week_days, "Active")
                active.text = "True"
                comment = etree.SubElement(week_days, "Comments")
                comment.text = '0'

    def faculty_gapweek_constraint(self, time):
        faculty = self.env['op.faculty'].search([])
        for w in faculty:
            if w.max_gaps_week > 0:
                week_days = etree.SubElement(
                    time, "ConstraintTeacherMaxGapsPerWeek")
                weight = etree.SubElement(week_days, "Weight_Percentage")
                weight_per = w.weight_percent
                fac_name = w.name
                if w.middle_name:
                    fac_name = '%s %s' % (fac_name, w.middle_name)
                if w.last_name:
                    fac_name = '%s %s' % (fac_name, w.last_name)
                weight.text = str(weight_per)
                Name = etree.SubElement(week_days, "Teacher_Name")
                Name.text = fac_name
                max_gap_week = etree.SubElement(week_days, "Max_Gaps")
                min_gap = w.max_gaps_week
                max_gap_week.text = str(min_gap)
                active = etree.SubElement(week_days, "Active")
                active.text = "True"
                # comment = etree.SubElement(week_days, "Comments")
                # comment.text = "0"

    def faculty_maxhr_daily_constraint(self, time):
        faculty = self.env['op.faculty'].search([])
        for w in faculty:
            if w.max_hrs > 0:
                week_days = etree.SubElement(
                    time, "ConstraintTeacherMaxHoursDaily")
                weight = etree.SubElement(week_days, "Weight_Percentage")
                weight_per = w.weight_percent
                fac_name = w.name
                if w.middle_name:
                    fac_name = '%s %s' % (fac_name, w.middle_name)
                if w.last_name:
                    fac_name = '%s %s' % (fac_name, w.last_name)
                weight.text = str(weight_per)
                Name = etree.SubElement(week_days, "Teacher_Name")
                Name.text = fac_name
                maxhr_daily = etree.SubElement(
                    week_days, "Maximum_Hours_Daily")
                max_hr = w.max_hrs
                maxhr_daily.text = str(max_hr)
                active = etree.SubElement(week_days, "Active")
                active.text = "True"
                # comment = etree.SubElement(week_days, "Comments")
                # comment.text = "0"

    def faculty_minhr_daily_constraint(self, time):
        faculty = self.env['op.faculty'].search([])
        for w in faculty:
            if w.min_hrs > 0:
                week_days = etree.SubElement(
                    time, "ConstraintTeacherMinHoursDaily")
                weight = etree.SubElement(week_days, "Weight_Percentage")
                weight_per = w.weight_percent
                fac_name = w.name
                if w.middle_name:
                    fac_name = '%s %s' % (fac_name, w.middle_name)
                if w.last_name:
                    fac_name = '%s %s' % (fac_name, w.last_name)
                weight.text = str(weight_per)
                Name = etree.SubElement(week_days, "Teacher_Name")
                Name.text = fac_name
                minhr_daily = etree.SubElement(
                    week_days, "Minimum_Hours_Daily")
                min_hr = w.min_hrs
                minhr_daily.text = str(min_hr)
                active = etree.SubElement(week_days, "Active")
                active.text = "True"
                # comment = etree.SubElement(week_days, "Comments")
                # comment.text = "0"

    def faculty_maxhr_cont_constraint(self, time):
        faculty = self.env['op.faculty'].search([])
        for w in faculty:
            if w.max_hrs_cont > 0:
                week_days = etree.SubElement(
                    time, "ConstraintTeacherMaxHoursContinuously")
                weight = etree.SubElement(week_days, "Weight_Percentage")
                weight_per = w.weight_percent
                fac_name = w.name
                if w.middle_name:
                    fac_name = '%s %s' % (fac_name, w.middle_name)
                if w.last_name:
                    fac_name = '%s %s' % (fac_name, w.last_name)
                weight.text = str(weight_per)
                Name = etree.SubElement(week_days, "Teacher_Name")
                Name.text = fac_name
                maxhr_cont = etree.SubElement(
                    week_days, "Maximum_Hours_Continuously")
                max_hr_ct = w.max_hrs_cont
                maxhr_cont.text = str(max_hr_ct)
                active = etree.SubElement(week_days, "Active")
                active.text = "True"
                # comment = etree.SubElement(week_days, "Comments")
                # comment.text = "0"

    def faculty_maxhr_activity_constraint(self, time):
        faculty = self.env['op.faculty'].search([])
        for w in faculty:
            if w.max_hr_cont_act > 0:
                week_days = etree.SubElement(
                    time, "ConstraintTeacherActivityTagMaxHoursDaily")
                weight = etree.SubElement(week_days, "Weight_Percentage")
                weight_per = w.weight_percent
                fac_name = w.name
                if w.middle_name:
                    fac_name = '%s %s' % (fac_name, w.middle_name)
                if w.last_name:
                    fac_name = '%s %s' % (fac_name, w.last_name)
                weight.text = str(weight_per)
                Name = etree.SubElement(week_days, "Teacher_Name")
                Name.text = fac_name
                activity_tag = etree.SubElement(week_days, "Activity_Tag_Name")
                activity = w.activity_name.name or ''
                activity_tag.text = activity
                maxhr_cont_act = etree.SubElement(
                    week_days, "Maximum_Hours_Daily")
                max_hr_act_con = w.max_hr_cont_act
                maxhr_cont_act.text = str(max_hr_act_con)
                active = etree.SubElement(week_days, "Active")
                active.text = "True"
                # comment = etree.SubElement(week_days, "Comments")
                # comment.text = "0"

    def faculty_interval_maxdays_constraint(self, time):
        faculty = self.env['op.faculty'].search([])
        for w in faculty:
            if w.max_days > 0 and w.interval_start and w.interval_end:
                week_days = etree.SubElement(
                    time, "ConstraintTeacherIntervalMaxDaysPerWeek")
                weight = etree.SubElement(week_days, "Weight_Percentage")
                weight_per = w.weight_percent
                fac_name = w.name
                if w.middle_name:
                    fac_name = '%s %s' % (fac_name, w.middle_name)
                if w.last_name:
                    fac_name = '%s %s' % (fac_name, w.last_name)
                weight.text = str(weight_per)
                Name = etree.SubElement(week_days, "Teacher_Name")
                Name.text = fac_name
                interval_st = etree.SubElement(
                    week_days, "Interval_Start_Hour")
                interval_starts = w.interval_start.name
                interval_st.text = str(interval_starts)
                interval_en = etree.SubElement(week_days, "Interval_End_Hour")
                interval_ends = w.interval_end.name
                interval_en.text = str(interval_ends)
                max_day = etree.SubElement(week_days, "Max_Days_Per_Week")
                max_days = w.max_days
                max_day.text = str(max_days)
                active = etree.SubElement(week_days, "Active")
                active.text = "True"
                # comment = etree.SubElement(week_days, "Comments")
                # comment.text = "0"

    # All Faculties Constraints
    def faculties_maxday(self, time):
        faculties = self.env['op.all.faculty.constraints'].search([])
        for f in faculties:
            if f.max_days_per_week:
                week_days = etree.SubElement(
                    time, "ConstraintTeachersMaxDaysPerWeek")
                weight_percent = etree.SubElement(
                    week_days, "Weight_Percentage")
                weight = f.weight_percent
                weight_percent.text = str(weight)
                max_days_per_week = etree.SubElement(
                    week_days, "Max_Days_Per_Week")
                max_day = f.max_days_per_week
                max_days_per_week.text = str(max_day)
                active = etree.SubElement(week_days, "Active")
                active.text = "True"
                # comment = etree.SubElement(week_days, "Comments")
                # comment.text = "0"

    def faculties_minday(self, time):
        faculties = self.env['op.all.faculty.constraints'].search([])
        for f in faculties:
            if f.min_days_per_week:
                week_days = etree.SubElement(
                    time, "ConstraintTeachersMinDaysPerWeek")
                weight_percent = etree.SubElement(
                    week_days, "Weight_Percentage")
                weight = f.weight_percent
                weight_percent.text = str(weight)
                min_days_per_week = etree.SubElement(
                    week_days, "Min_Days_Per_Week")
                min_day = f.min_days_per_week
                min_days_per_week.text = str(min_day)
                active = etree.SubElement(week_days, "Active")
                active.text = "True"
                # comment = etree.SubElement(week_days, "Comments")
                # comment.text = "0"

    def faculties_maxgap(self, time):
        faculties = self.env['op.all.faculty.constraints'].search([])
        for f in faculties:
            if f.max_gaps_per_day:
                week_days = etree.SubElement(
                    time, "ConstraintTeachersMaxGapsPerDay")
                weight_percent = etree.SubElement(
                    week_days, "Weight_Percentage")
                weight = f.weight_percent
                weight_percent.text = str(weight)
                max_gaps = etree.SubElement(week_days, "Max_Gaps")
                max_gap = f.max_gaps_per_day
                max_gaps.text = str(max_gap)
                active = etree.SubElement(week_days, "Active")
                active.text = "True"
                # comment = etree.SubElement(week_days, "Comments")
                # comment.text = "0"

    def faculties_maxgap_week(self, time):
        faculties = self.env['op.all.faculty.constraints'].search([])
        for f in faculties:
            if f.max_gaps_per_week:
                week_days = etree.SubElement(
                    time, "ConstraintTeachersMaxGapsPerWeek")
                weight_percent = etree.SubElement(
                    week_days, "Weight_Percentage")
                weight = f.weight_percent
                weight_percent.text = str(weight)
                max_gaps_week = etree.SubElement(week_days, "Max_Gaps")
                max_gap = f.max_gaps_per_week
                max_gaps_week.text = str(max_gap)
                active = etree.SubElement(week_days, "Active")
                active.text = "True"
                # comment = etree.SubElement(week_days, "Comments")
                # comment.text = "0"

    def faculties_maxhrs(self, time):
        faculties = self.env['op.all.faculty.constraints'].search([])
        for f in faculties:
            if f.max_hrs_daily > 0:
                week_days = etree.SubElement(
                    time, "ConstraintTeachersMaxHoursDaily")
                weight_percent = etree.SubElement(
                    week_days, "Weight_Percentage")
                weight = f.weight_percent
                weight_percent.text = str(weight)
                max_hrs_daily = etree.SubElement(
                    week_days, "Maximum_Hours_Daily")
                max_hrs = f.max_hrs_daily
                max_hrs_daily.text = str(max_hrs)
                active = etree.SubElement(week_days, "Active")
                active.text = "True"
                # comment = etree.SubElement(week_days, "Comments")
                # comment.text = "0"

    def faculties_minhrs(self, time):
        faculties = self.env['op.all.faculty.constraints'].search([])
        for f in faculties:
            if f.min_hrs_daily > 0:
                week_days = etree.SubElement(
                    time, "ConstraintTeachersMinHoursDaily")
                weight_percent = etree.SubElement(
                    week_days, "Weight_Percentage")
                weight = f.weight_percent
                weight_percent.text = str(weight)
                min_hrs_daily = etree.SubElement(
                    week_days, "Minimum_Hours_Daily")
                min_hrs = f.min_hrs_daily
                min_hrs_daily.text = str(min_hrs)
                active = etree.SubElement(week_days, "Active")
                active.text = "True"
                # comment = etree.SubElement(week_days, "Comments")
                # comment.text = "0"

    def faculties_maxhrs_cont(self, time):
        faculties = self.env['op.all.faculty.constraints'].search([])
        for f in faculties:
            if f.max_hrs_cont_tr > 0:
                week_days = etree.SubElement(
                    time, "ConstraintTeachersMaxHoursContinuously")
                weight_percent = etree.SubElement(
                    week_days, "Weight_Percentage")
                weight = f.weight_percent
                weight_percent.text = str(weight)
                max_hrs_cont = etree.SubElement(
                    week_days, "Maximum_Hours_Continuously")
                max_hrs = f.max_hrs_cont_tr
                max_hrs_cont.text = str(max_hrs)
                active = etree.SubElement(week_days, "Active")
                active.text = "True"
                # comment = etree.SubElement(week_days, "Comments")
                # comment.text = "0"

    def faculties_maxhr_activity(self, time):
        faculties = self.env['op.faculty.activity.maxhrs'].search([])
        for w in faculties:
            if w.max_hrs_cont_tr_act > 0:
                week_days = etree.SubElement(
                    time, "ConstraintTeachersActivityTagMaxHoursContinuously")
                weight = etree.SubElement(week_days, "Weight_Percentage")
                weight_per = w.weight_percent
                weight.text = str(weight_per)
                activity_tag = etree.SubElement(week_days, "Activity_Tag_Name")
                activity = w.act_tag_name.name or ''
                activity_tag.text = activity
                maxhr_cont_act = etree.SubElement(
                    week_days, "Maximum_Hours_Continuously")
                max_hr_act_con = w.max_hrs_cont_tr_act
                maxhr_cont_act.text = str(max_hr_act_con)
                active = etree.SubElement(week_days, "Active")
                active.text = "True"
                # comment = etree.SubElement(week_days, "Comments")
                # comment.text = "0"

    def faculties_hr_activity(self, time):
        faculties = self.env['op.all.faculty.constraints'].search([])
        for w in faculties:
            if w.max_days_per_week > 0 and w.interval_start and w.interval_end:
                week_days = etree.SubElement(
                    time, "ConstraintTeachersIntervalMaxDaysPerWeek")
                weight = etree.SubElement(week_days, "Weight_Percentage")
                weight_per = w.weight_percent
                weight.text = str(weight_per)
                interval_st = etree.SubElement(
                    week_days, "Interval_Start_Hour")
                interval_starts = w.interval_start.name
                interval_st.text = str(interval_starts)
                interval_en = etree.SubElement(week_days, "Interval_End_Hour")
                interval_ends = w.interval_end.name
                interval_en.text = str(interval_ends)
                max_day = etree.SubElement(week_days, "Max_Days_Per_Week")
                max_hr_act_con = w.max_days_per_week
                max_day.text = str(max_hr_act_con)
                active = etree.SubElement(week_days, "Active")
                active.text = "True"
                # comment = etree.SubElement(week_days, "Comments")
                # comment.text = "0"

    # Student Time Constraints
    def student_notavailable(self, time):
        batch = self.env['op.batch.constraints'].search([])
        week_days = etree.SubElement(time, "ConstraintStudentsSetNotAvailableTimes")
        for b in batch:
            weight = etree.SubElement(week_days, "Weight_Percentage")
            weight_per = b.weight
            batch_name = b.student_id.name
            weight.text = str(weight_per)
            Name = etree.SubElement(week_days, "Students")
            if b.division:
                batch_name = '%s %s' % (batch_name, b.division.name)
            if b.subdivision:
                batch_name = '%s %s' % (batch_name, b.subdivision.name)
            Name.text = batch_name
            stud_time = self.env['op.breaks.constraints.line'].search([('batch_constraint_id', '=', b.id)])
            count = 0
            for t in stud_time:
                if t.monday == 1:
                    not_available = etree.SubElement(week_days, "Not_Available_Time")
                    not_available_day = etree.SubElement(not_available, "Day")
                    not_available_day.text = 'Monday'
                    count += 1
                    hour = etree.SubElement(not_available, "Hour")
                    hour.text = t.name
                if t.tuesday == 1:
                    not_available = etree.SubElement(week_days, "Not_Available_Time")
                    not_available_day = etree.SubElement(not_available, "Day")
                    not_available_day.text = 'Tuesday'
                    count += 1
                    hour = etree.SubElement(not_available, "Hour")
                    hour.text = t.name
                if t.wednesday == 1:
                    not_available = etree.SubElement(week_days, "Not_Available_Time")
                    not_available_day = etree.SubElement(not_available, "Day")
                    not_available_day.text = 'Wednesday'
                    count += 1
                    hour = etree.SubElement(not_available, "Hour")
                    hour.text = t.name
                if t.thursday == 1:
                    not_available = etree.SubElement(week_days, "Not_Available_Time")
                    not_available_day = etree.SubElement(not_available, "Day")
                    not_available_day.text = 'Thursday'
                    count += 1
                    hour = etree.SubElement(not_available, "Hour")
                    hour.text = t.name
                if t.friday == 1:
                    not_available = etree.SubElement(week_days, "Not_Available_Time")
                    not_available_day = etree.SubElement(not_available, "Day")
                    not_available_day.text = 'Friday'
                    count += 1
                    hour = etree.SubElement(not_available, "Hour")
                    hour.text = t.name
                if t.saturday == 1:
                    not_available = etree.SubElement(week_days, "Not_Available_Time")
                    not_available_day = etree.SubElement(not_available, "Day")
                    not_available_day.text = 'Saturday'
                    count += 1
                    hour = etree.SubElement(not_available, "Hour")
                    hour.text = t.name
                if t.sunday == 1:
                    not_available = etree.SubElement(week_days, "Not_Available_Time")
                    not_available_day = etree.SubElement(not_available, "Day")
                    not_available_day.text = 'Sunday'
                    count += 1
                    hour = etree.SubElement(not_available, "Hour")
                    hour.text = t.name
            Number = etree.SubElement(week_days, "Number_of_Not_Available_Times")
            Number.text = str(count)
            active = etree.SubElement(week_days, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def student_maxday_constraint(self, time):
        batch = self.env['student.time.constraints'].search([])
        for b in batch:
            week_days = etree.SubElement(
                time, "ConstraintStudentsSetMaxDaysPerWeek")
            weight = etree.SubElement(week_days, "Weight_Percentage")
            weight_per = b.weight_percent
            weight.text = str(weight_per)
            batch_name = b.name.name
            if b.group_name:
                batch_name = '%s %s' % (batch_name, b.group_name.name)
            if b.subgroup_name:
                batch_name = '%s %s' % (batch_name, b.subgroup_name.name)
            Name = etree.SubElement(week_days, "Students")
            Name.text = batch_name
            max_day = etree.SubElement(week_days, "Max_Days_Per_Week")
            max_days = b.max_days_week
            max_day.text = str(max_days)
            active = etree.SubElement(week_days, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def student_maxgap_day(self, time):
        batch = self.env['student.time.constraints'].search([])
        for b in batch:
            week_days = etree.SubElement(
                time, "ConstraintStudentsSetMaxGapsPerDay")
            weight = etree.SubElement(week_days, "Weight_Percentage")
            weight_per = b.weight_percent
            weight.text = str(weight_per)
            maxgap_day = etree.SubElement(week_days, "Max_Gaps")
            max_gap_days = b.max_gaps_day
            maxgap_day.text = str(max_gap_days)
            batch_name = b.name.name
            if b.group_name:
                batch_name = '%s %s' % (batch_name, b.group_name.name)
            if b.subgroup_name:
                batch_name = '%s %s' % (batch_name, b.subgroup_name.name)
            Name = etree.SubElement(week_days, "Students")
            Name.text = batch_name
            active = etree.SubElement(week_days, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def student_maxgap_week(self, time):
        batch = self.env['student.time.constraints'].search([])
        for b in batch:
            week_days = etree.SubElement(
                time, "ConstraintStudentsSetMaxGapsPerWeek")
            weight = etree.SubElement(week_days, "Weight_Percentage")
            weight_per = b.weight_percent
            weight.text = str(weight_per)
            batch_name = b.name.name
            if b.group_name:
                batch_name = '%s %s' % (batch_name, b.group_name.name)
            if b.subgroup_name:
                batch_name = '%s %s' % (batch_name, b.subgroup_name.name)
            Name = etree.SubElement(week_days, "Students")
            Name.text = batch_name
            maxgap_day = etree.SubElement(week_days, "Max_Gaps")
            max_gap_days = b.max_gaps_week
            maxgap_day.text = str(max_gap_days)
            active = etree.SubElement(week_days, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def student_maxsecond(self, time):
        batch = self.env['student.time.constraints'].search([])
        for b in batch:
            week_days = etree.SubElement(
                time, "ConstraintStudentsSetEarlyMaxBeginningsAtSecondHour")
            weight = etree.SubElement(week_days, "Weight_Percentage")
            weight_per = b.weight_percent
            weight.text = str(weight_per)
            maxgap_day = etree.SubElement(
                week_days, "Max_Beginnings_At_Second_Hour")
            max_gap_days = b.max_gaps_day
            maxgap_day.text = str(max_gap_days)
            batch_name = b.name.name
            if b.group_name:
                batch_name = '%s %s' % (batch_name, b.group_name.name)
            if b.subgroup_name:
                batch_name = '%s %s' % (batch_name, b.subgroup_name.name)
            Name = etree.SubElement(week_days, "Students")
            Name.text = batch_name
            active = etree.SubElement(week_days, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def student_maxhr_daily(self, time):
        batch = self.env['student.time.constraints'].search([])
        for b in batch:
            week_days = etree.SubElement(
                time, "ConstraintStudentsSetMaxHoursDaily")
            weight = etree.SubElement(week_days, "Weight_Percentage")
            weight_per = b.weight_percent
            weight.text = str(weight_per)
            max_hrs_daily = etree.SubElement(week_days, "Maximum_Hours_Daily")
            max_hr = b.max_hrs_daily
            max_hrs_daily.text = str(max_hr)
            batch_name = b.name.name
            if b.group_name:
                batch_name = '%s %s' % (batch_name, b.group_name.name)
            if b.subgroup_name:
                batch_name = '%s %s' % (batch_name, b.subgroup_name.name)
            Name = etree.SubElement(week_days, "Students")
            Name.text = batch_name
            active = etree.SubElement(week_days, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def student_maxhr_activity(self, time):
        batch = self.env['student.time.constraints'].search([])
        for b in batch:
            week_days = etree.SubElement(
                time, "ConstraintStudentsSetActivityTagMaxHoursDaily")
            weight = etree.SubElement(week_days, "Weight_Percentage")
            weight_per = b.weight_percent
            weight.text = str(weight_per)
            max_hrs_daily = etree.SubElement(week_days, "Maximum_Hours_Daily")
            max_hr = b.max_hrs_daily
            max_hrs_daily.text = str(max_hr)
            batch_name = b.name.name
            if b.group_name:
                batch_name = '%s %s' % (batch_name, b.group_name.name)
            if b.subgroup_name:
                batch_name = '%s %s' % (batch_name, b.subgroup_name.name)
            Name = etree.SubElement(week_days, "Students")
            Name.text = batch_name
            activity_name = etree.SubElement(week_days, "Activity_Tag")
            activity = b.activity_name.name
            activity_name.text = activity
            active = etree.SubElement(week_days, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def student_minhr_daily(self, time):
        batch = self.env['student.time.constraints'].search([])
        for b in batch:
            week_days = etree.SubElement(
                time, "ConstraintStudentsSetMinHoursDaily")
            weight = etree.SubElement(week_days, "Weight_Percentage")
            weight_per = b.weight_percent
            weight.text = str(weight_per)
            min_hrs_daily = etree.SubElement(week_days, "Minimum_Hours_Daily")
            min_hr = b.min_hrs_daily
            min_hrs_daily.text = str(min_hr)
            batch_name = b.name.name
            if b.group_name:
                batch_name = '%s %s' % (batch_name, b.group_name.name)
            if b.subgroup_name:
                batch_name = '%s %s' % (batch_name, b.subgroup_name.name)
            Name = etree.SubElement(week_days, "Students")
            Name.text = batch_name
            empty_days = etree.SubElement(week_days, "Allow_Empty_Days")
            empty_days.text = "true"
            active = etree.SubElement(week_days, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def student_maxhr_cont(self, time):
        batch = self.env['student.time.constraints'].search([])
        for b in batch:
            week_days = etree.SubElement(
                time, "ConstraintStudentsSetMaxHoursContinuously")
            weight = etree.SubElement(week_days, "Weight_Percentage")
            weight_per = b.weight_percent
            weight.text = str(weight_per)
            max_hrs_con = etree.SubElement(
                week_days, "Maximum_Hours_Continuously")
            max_hr_conti = b.max_hr_cont
            max_hrs_con.text = str(max_hr_conti)
            batch_name = b.name.name
            if b.group_name:
                batch_name = '%s %s' % (batch_name, b.group_name.name)
            if b.subgroup_name:
                batch_name = '%s %s' % (batch_name, b.subgroup_name.name)
            Name = etree.SubElement(week_days, "Students")
            Name.text = batch_name
            active = etree.SubElement(week_days, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def student_maxhr_cont_daily(self, time):
        batch = self.env['student.time.constraints'].search([])
        for b in batch:
            week_days = etree.SubElement(
                time, "ConstraintStudentsSetActivityTagMaxHoursContinuously")
            weight = etree.SubElement(week_days, "Weight_Percentage")
            weight_per = b.weight_percent
            weight.text = str(weight_per)
            max_hrs_con = etree.SubElement(
                week_days, "Maximum_Hours_Continuously")
            max_hr_conti = b.max_hr_cont
            max_hrs_con.text = str(max_hr_conti)
            batch_name = b.name.name
            if b.group_name:
                batch_name = '%s %s' % (batch_name, b.group_name.name)
            if b.subgroup_name:
                batch_name = '%s %s' % (batch_name, b.subgroup_name.name)
            Name = etree.SubElement(week_days, "Students")
            Name.text = batch_name
            activity_name = etree.SubElement(week_days, "Activity_Tag")
            activity = b.activity_name.name
            activity_name.text = activity
            active = etree.SubElement(week_days, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def student_set_interval(self, time):
        batch = self.env['student.time.constraints'].search([])
        for b in batch:
            week_days = etree.SubElement(
                time, "ConstraintStudentsSetIntervalMaxDaysPerWeek")
            weight = etree.SubElement(week_days, "Weight_Percentage")
            weight_per = b.weight_percent
            weight.text = str(weight_per)
            max_days_week = etree.SubElement(week_days, "Max_Days_Per_Week")
            max_day = b.max_days_week
            max_days_week.text = str(max_day)
            batch_name = b.name.name
            if b.group_name:
                batch_name = '%s %s' % (batch_name, b.group_name.name)
            if b.subgroup_name:
                batch_name = '%s %s' % (batch_name, b.subgroup_name.name)
            Name = etree.SubElement(week_days, "Students")
            Name.text = batch_name
            interval_st = etree.SubElement(
                week_days, "Interval_Start_Hour")
            interval_starts = b.interval_start.name
            interval_st.text = str(interval_starts)
            interval_en = etree.SubElement(week_days, "Interval_End_Hour")
            interval_ends = b.interval_end.name
            interval_en.text = str(interval_ends)
            active = etree.SubElement(week_days, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    # All Students
    def allstudent_maxday_constraint(self, time):
        batch = self.env['all.student.constraints'].search([])
        for b in batch:
            week_days = etree.SubElement(
                time, "ConstraintStudentsSetMaxDaysPerWeek")
            weight = etree.SubElement(week_days, "Weight_Percentage")
            weight_per = b.weight_percent
            weight.text = str(weight_per)
            max_day = etree.SubElement(week_days, "Max_Days_Per_Week")
            max_days = b.max_days_week
            max_day.text = str(max_days)
            active = etree.SubElement(week_days, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def allstudent_maxgap_day(self, time):
        batch = self.env['all.student.constraints'].search([])
        for b in batch:
            week_days = etree.SubElement(
                time, "ConstraintStudentsSetMaxGapsPerDay")
            weight = etree.SubElement(week_days, "Weight_Percentage")
            weight_per = b.weight_percent
            weight.text = str(weight_per)
            maxgap_day = etree.SubElement(week_days, "Max_Gaps")
            max_gap_days = b.max_gaps_per_day
            maxgap_day.text = str(max_gap_days)
            active = etree.SubElement(week_days, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def allstudent_maxgap_week(self, time):
        batch = self.env['all.student.constraints'].search([])
        for b in batch:
            week_days = etree.SubElement(
                time, "ConstraintStudentsSetMaxGapsPerWeek")
            weight = etree.SubElement(week_days, "Weight_Percentage")
            weight_per = b.weight_percent
            weight.text = str(weight_per)
            maxgap_day = etree.SubElement(week_days, "Max_Gaps")
            max_gap_days = b.max_gaps_per_week
            maxgap_day.text = str(max_gap_days)
            active = etree.SubElement(week_days, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def allstudent_maxsecond(self, time):
        batch = self.env['all.student.constraints'].search([])
        for b in batch:
            week_days = etree.SubElement(
                time, "ConstraintStudentsSetEarlyMaxBeginningsAtSecondHour")
            weight = etree.SubElement(week_days, "Weight_Percentage")
            weight_per = b.weight_percent
            weight.text = str(weight_per)
            maxgap_day = etree.SubElement(
                week_days, "Max_Beginnings_At_Second_Hour")
            max_gap_days = b.max_beginnings
            maxgap_day.text = str(max_gap_days)
            active = etree.SubElement(week_days, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def allstudent_maxhr_daily(self, time):
        batch = self.env['all.student.constraints'].search([])
        for b in batch:
            week_days = etree.SubElement(
                time, "ConstraintStudentsSetMaxHoursDaily")
            weight = etree.SubElement(week_days, "Weight_Percentage")
            weight_per = b.weight_percent
            weight.text = str(weight_per)
            max_hrs_daily = etree.SubElement(week_days, "Maximum_Hours_Daily")
            max_hr = b.max_hr_daily
            max_hrs_daily.text = str(max_hr)
            active = etree.SubElement(week_days, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def allstudent_maxhr_activity(self, time):
        batch = self.env['all.student.constraints'].search([])
        for b in batch:
            week_days = etree.SubElement(
                time, "ConstraintStudentsActivityTagMaxHoursDaily")
            weight = etree.SubElement(week_days, "Weight_Percentage")
            weight_per = b.weight_percent
            weight.text = str(weight_per)
            max_hrs_daily = etree.SubElement(week_days, "Maximum_Hours_Daily")
            max_hr = b.max_hr_daily_act
            max_hrs_daily.text = str(max_hr)
            activity_name = etree.SubElement(week_days, "Activity_Tag")
            activity = b.activity.name
            activity_name.text = activity
            active = etree.SubElement(week_days, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def allstudent_minhr_daily(self, time):
        batch = self.env['all.student.constraints'].search([])
        for b in batch:
            week_days = etree.SubElement(
                time, "ConstraintStudentsSetMinHoursDaily")
            weight = etree.SubElement(week_days, "Weight_Percentage")
            weight_per = b.weight_percent
            weight.text = str(weight_per)
            min_hrs_daily = etree.SubElement(week_days, "Minimum_Hours_Daily")
            min_hr = b.min_hr_daily
            min_hrs_daily.text = str(min_hr)
            empty_days = etree.SubElement(week_days, "Allow_Empty_Days")
            empty_days.text = "true"
            active = etree.SubElement(week_days, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def allstudent_maxhr_cont(self, time):
        batch = self.env['all.student.constraints'].search([])
        for b in batch:
            week_days = etree.SubElement(
                time, "ConstraintStudentsSetActivityTagMaxHoursContinuously")
            weight = etree.SubElement(week_days, "Weight_Percentage")
            weight_per = b.weight_percent
            weight.text = str(weight_per)
            max_hrs_con = etree.SubElement(
                week_days, "Maximum_Hours_Continuously")
            max_hr_conti = b.max_hr_cont
            max_hrs_con.text = str(max_hr_conti)
            activity_name = etree.SubElement(week_days, "Activity_Tag")
            activity = b.activity.name
            activity_name.text = activity
            active = etree.SubElement(week_days, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def allstudent_maxhr_act_cont(self, time):
        batch = self.env['all.student.constraints'].search([])
        for b in batch:
            week_days = etree.SubElement(
                time, "ConstraintStudentsActivityTagMaxHoursContinuously")
            weight = etree.SubElement(week_days, "Weight_Percentage")
            weight_per = b.weight_percent
            weight.text = str(weight_per)
            max_hrs_daily = etree.SubElement(
                week_days, "Maximum_Hours_Continuously")
            max_hr = b.max_hr_daily
            max_hrs_daily.text = str(max_hr)
            activity_name = etree.SubElement(week_days, "Activity_Tag")
            activity = b.activity.name
            activity_name.text = activity
            active = etree.SubElement(week_days, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def allstudent_set_interval(self, time):
        batch = self.env['all.student.constraints'].search([])
        for b in batch:
            week_days = etree.SubElement(
                time, "ConstraintStudentsSetIntervalMaxDaysPerWeek")
            weight = etree.SubElement(week_days, "Weight_Percentage")
            weight_per = b.weight_percent
            weight.text = str(weight_per)
            max_days_week = etree.SubElement(week_days, "Max_Days_Per_Week")
            max_day = b.max_days_week
            max_days_week.text = str(max_day)
            interval_st = etree.SubElement(
                week_days, "Interval_Start_Hour")
            interval_starts = b.start_time.name
            interval_st.text = str(interval_starts)
            interval_en = etree.SubElement(week_days, "Interval_End_Hour")
            interval_ends = b.end_time.name
            interval_en.text = str(interval_ends)
            active = etree.SubElement(week_days, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

# Break
    def break_time(self, time):
        breaks = self.env['op.break.time'].search([])
        for rec in breaks:
            preferred_times = etree.SubElement(time, "ConstraintBreakTimes")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            c = 0
            for line in rec.break_line_ids:
                if line.monday:
                    preferred_starting_time = etree.SubElement(preferred_times, "Break_Time")
                    preferred_starting_day = etree.SubElement(preferred_starting_time, "Day")
                    preferred_starting_day.text = 'Monday'
                    preferred_starting_hour = etree.SubElement(preferred_starting_time, "Hour")
                    preferred_starting_hour.text = line.name
                    c += 1
                if line.tuesday:
                    preferred_starting_time = etree.SubElement(preferred_times, "Break_Time")
                    preferred_starting_day = etree.SubElement(preferred_starting_time, "Day")
                    preferred_starting_day.text = 'Tuesday'
                    preferred_starting_hour = etree.SubElement(preferred_starting_time, "Hour")
                    preferred_starting_hour.text = line.name
                    c += 1
                if line.wednesday:
                    preferred_starting_time = etree.SubElement(preferred_times, "Break_Time")
                    preferred_starting_day = etree.SubElement(preferred_starting_time, "Day")
                    preferred_starting_day.text = 'Wednesday'
                    preferred_starting_hour = etree.SubElement(preferred_starting_time, "Hour")
                    preferred_starting_hour.text = line.name
                    c += 1
                if line.thursday:
                    preferred_starting_time = etree.SubElement(preferred_times, "Break_Time")
                    preferred_starting_day = etree.SubElement(preferred_starting_time, "Day")
                    preferred_starting_day.text = 'Thursday'
                    preferred_starting_hour = etree.SubElement(preferred_starting_time, "Hour")
                    preferred_starting_hour.text = line.name
                    c += 1
                if line.friday:
                    preferred_starting_time = etree.SubElement(preferred_times, "Break_Time")
                    preferred_starting_day = etree.SubElement(preferred_starting_time, "Day")
                    preferred_starting_day.text = 'Friday'
                    preferred_starting_hour = etree.SubElement(preferred_starting_time, "Hour")
                    preferred_starting_hour.text = line.name
                    c += 1
                if line.saturday:
                    preferred_starting_time = etree.SubElement(preferred_times, "Break_Time")
                    preferred_starting_day = etree.SubElement(preferred_starting_time, "Day")
                    preferred_starting_day.text = 'Saturday'
                    preferred_starting_hour = etree.SubElement(preferred_starting_time, "Hour")
                    preferred_starting_hour.text = line.name
                    c += 1
                if line.sunday:
                    preferred_starting_time = etree.SubElement(preferred_times, "Break_Time")
                    preferred_starting_day = etree.SubElement(preferred_starting_time, "Day")
                    preferred_starting_day.text = 'Sunday'
                    preferred_starting_hour = etree.SubElement(preferred_starting_time, "Hour")
                    preferred_starting_hour.text = line.name
                    c += 1
            num = etree.SubElement(preferred_times, "Number_of_Break_Times")
            num.text = str(c)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

# ActivityPreferredStartingTime
    def preferred_starting_time(self, time):
        preferred_time_obj = self.env['op.activity.preferred.starting.time'].search([])
        for rec in preferred_time_obj:
            preferred_time = etree.SubElement(time, "ConstraintActivityPreferredStartingTime")
            weight = etree.SubElement(preferred_time, "Weight_Percentage")
            weight.text = str(rec.weight)
            activity_id = etree.SubElement(preferred_time, "Activity_Id")
            activity_id.text = str(rec.id)
            preferred_day = etree.SubElement(preferred_time, "Preferred_Day")
            preferred_day.text = str(rec.day)
            preferred_hour = etree.SubElement(preferred_time, "Preferred_Hour")
            preferred_hour.text = str(rec.hours.name)
            locked = etree.SubElement(preferred_time, "Permanently_Locked")
            locked.text = 'true' if rec.lock else 'false'
            active = etree.SubElement(preferred_time, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_time, "Comments")
            comments.text = "Comments"

# An activity has a set of preferred starting times
    def preferred_starting_times(self, time):
        starting_time_obj = self.env['op.activity.starting.time'].search([])
        for rec in starting_time_obj:
            preferred_times = etree.SubElement(time, "ConstraintActivityPreferredStartingTimes")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            activity_id = etree.SubElement(preferred_times, "Activity_Id")
            activity_id.text = str(rec.activity_id.id)
            c = 0
            for line in rec.activity_starting_line_ids:

                if line.monday:
                    preferred_starting_time = etree.SubElement(preferred_times, "Preferred_Starting_Time")
                    preferred_starting_day = etree.SubElement(preferred_starting_time, "Preferred_Starting_Day")
                    preferred_starting_day.text = 'Monday'
                    preferred_starting_hour = etree.SubElement(preferred_starting_time, "Preferred_Starting_Hour")
                    preferred_starting_hour.text = line.name
                    c += 1
                if line.tuesday:
                    preferred_starting_time = etree.SubElement(preferred_times, "Preferred_Starting_Time")
                    preferred_starting_day = etree.SubElement(preferred_starting_time, "Preferred_Starting_Day")
                    preferred_starting_day.text = 'Tuesday'
                    preferred_starting_hour = etree.SubElement(preferred_starting_time, "Preferred_Starting_Hour")
                    preferred_starting_hour.text = line.name
                    c += 1
                if line.wednesday:
                    preferred_starting_time = etree.SubElement(preferred_times, "Preferred_Starting_Time")
                    preferred_starting_day = etree.SubElement(preferred_starting_time, "Preferred_Starting_Day")
                    preferred_starting_day.text = 'Wednesday'
                    preferred_starting_hour = etree.SubElement(preferred_starting_time, "Preferred_Starting_Hour")
                    preferred_starting_hour.text = line.name
                    c += 1
                if line.thursday:
                    preferred_starting_time = etree.SubElement(preferred_times, "Preferred_Starting_Time")
                    preferred_starting_day = etree.SubElement(preferred_starting_time, "Preferred_Starting_Day")
                    preferred_starting_day.text = 'Thursday'
                    preferred_starting_hour = etree.SubElement(preferred_starting_time, "Preferred_Starting_Hour")
                    preferred_starting_hour.text = line.name
                    c += 1
                if line.friday:
                    preferred_starting_time = etree.SubElement(preferred_times, "Preferred_Starting_Time")
                    preferred_starting_day = etree.SubElement(preferred_starting_time, "Preferred_Starting_Day")
                    preferred_starting_day.text = 'Friday'
                    preferred_starting_hour = etree.SubElement(preferred_starting_time, "Preferred_Starting_Hour")
                    preferred_starting_hour.text = line.name
                    c += 1
                if line.saturday:
                    preferred_starting_time = etree.SubElement(preferred_times, "Preferred_Starting_Time")
                    preferred_starting_day = etree.SubElement(preferred_starting_time, "Preferred_Starting_Day")
                    preferred_starting_day.text = 'Saturday'
                    preferred_starting_hour = etree.SubElement(preferred_starting_time, "Preferred_Starting_Hour")
                    preferred_starting_hour.text = line.name
                    c += 1
                if line.sunday:
                    preferred_starting_time = etree.SubElement(preferred_times, "Preferred_Starting_Time")
                    preferred_starting_day = etree.SubElement(preferred_starting_time, "Preferred_Starting_Day")
                    preferred_starting_day.text = 'Sunday'
                    preferred_starting_hour = etree.SubElement(preferred_starting_time, "Preferred_Starting_Hour")
                    preferred_starting_hour.text = line.name
                    c += 1
            num = etree.SubElement(preferred_times, "Number_of_Preferred_Starting_Times")
            num.text = str(c)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"


# An activity has a set of preferred timeslots
    def preferred_timeslots(self, time):
        timeslot_obj = self.env['op.activity.timeslots'].search([])
        for rec in timeslot_obj:
            activity_preferred_timeslots = etree.SubElement(time, "ConstraintActivityPreferredTimeSlots")
            weight = etree.SubElement(activity_preferred_timeslots, "Weight_Percentage")
            weight.text = str(rec.weight)
            activity_id = etree.SubElement(activity_preferred_timeslots, "Activity_Id")
            activity_id.text = str(rec.activity_id.id)
            c = 0
            for line in rec.activity_timeslots_line_ids:
                if line.monday:
                    preferred_timeslots = etree.SubElement(activity_preferred_timeslots, "Preferred_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Day")
                    preferred_day.text = 'Monday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.tuesday:
                    preferred_timeslots = etree.SubElement(activity_preferred_timeslots, "Preferred_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Day")
                    preferred_day.text = 'Tuesday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.wednesday:
                    preferred_timeslots = etree.SubElement(activity_preferred_timeslots, "Preferred_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Day")
                    preferred_day.text = 'Wednesday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.thursday:
                    preferred_timeslots = etree.SubElement(activity_preferred_timeslots, "Preferred_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Day")
                    preferred_day.text = 'Thursday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.friday:
                    preferred_timeslots = etree.SubElement(activity_preferred_timeslots, "Preferred_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Day")
                    preferred_day.text = 'Friday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.saturday:
                    preferred_timeslots = etree.SubElement(activity_preferred_timeslots, "Preferred_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Day")
                    preferred_day.text = 'Saturday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.sunday:
                    preferred_timeslots = etree.SubElement(activity_preferred_timeslots, "Preferred_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Day")
                    preferred_day.text = 'Sunday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Hour")
                    preferred_hour.text = line.name
                    c += 1
            num = etree.SubElement(activity_preferred_timeslots, "Number_of_Preferred_Time_Slots")
            num.text = str(c)
            active = etree.SubElement(activity_preferred_timeslots, "Active")
            active.text = "true"
            comments = etree.SubElement(activity_preferred_timeslots, "Comments")
            comments.text = "Comments"

# Set of activities has a set of preferred starting time
    def activities_preferredtimes(self, time):
        time_obj = self.env['op.activities.starting.time'].search([])
        for rec in time_obj:
            preferred_times = etree.SubElement(time, "ConstraintActivitiesPreferredStartingTimes")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            teacher = etree.SubElement(preferred_times, "Teacher_Name")
            teacher.text = rec.faculty_id.name
            student = etree.SubElement(preferred_times, "Students_Name")
            student.text = rec.student_id.name
            subject = etree.SubElement(preferred_times, "Subject_Name")
            subject.text = rec.subject_id.name
            tag = etree.SubElement(preferred_times, "Activity_Tag_Name")
            tag.text = rec.activity_tag_id.name
            duration = etree.SubElement(preferred_times, "Duration")
            duration.text = str(rec.duration) if rec.duration else ""
            c = 0
            for line in rec.activities_starting_time_line_ids:
                if line.monday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Starting_Time")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Starting_Day")
                    preferred_day.text = 'Monday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Starting_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.tuesday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Starting_Time")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Starting_Day")
                    preferred_day.text = 'Tuesday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Starting_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.wednesday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Starting_Time")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Starting_Day")
                    preferred_day.text = 'Wednesday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Starting_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.thursday:
                    preferred_day = etree.SubElement(preferred_times, "Preferred_Starting_Day")
                    preferred_day.text = 'Thursday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Starting_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.friday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Starting_Time")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Starting_Day")
                    preferred_day.text = 'Friday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Starting_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.saturday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Starting_Time")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Starting_Day")
                    preferred_day.text = 'Saturday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Starting_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.sunday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Starting_Time")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Starting_Day")
                    preferred_day.text = 'Sunday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Starting_Hour")
                    preferred_hour.text = line.name
                    c += 1
            number = etree.SubElement(preferred_times, "Number_of_Preferred_Starting_Times")
            number.text = str(c)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"


# Set of activities has a set of preferred time slots
    def activities_preferred_timeslots(self, time):
        time_obj = self.env['op.activities.timeslots'].search([])
        for rec in time_obj:
            preferred_times = etree.SubElement(time, "ConstraintActivitiesPreferredTimeSlots")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            teacher = etree.SubElement(preferred_times, "Teacher_Name")
            teacher.text = rec.faculty_id.name
            student = etree.SubElement(preferred_times, "Students_Name")
            student.text = rec.student_id.name
            subject = etree.SubElement(preferred_times, "Subject_Name")
            subject.text = rec.subject_id.name
            tag = etree.SubElement(preferred_times, "Activity_Tag_Name")
            tag.text = rec.activity_tag_id.name
            duration = etree.SubElement(preferred_times, "Duration")
            duration.text = str(rec.duration) if rec.duration else ""
            c = 0
            for line in rec.activities_timeslots_line_ids:
                if line.monday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Day")
                    preferred_day.text = 'Monday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.tuesday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Day")
                    preferred_day.text = 'Tuesday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.wednesday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Day")
                    preferred_day.text = 'Wednesday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.thursday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Day")
                    preferred_day.text = 'Thursday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.friday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Day")
                    preferred_day.text = 'Friday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.saturday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Day")
                    preferred_day.text = 'Saturday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.sunday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Day")
                    preferred_day.text = 'Sunday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Hour")
                    preferred_hour.text = line.name
                    c += 1
            number = etree.SubElement(preferred_times, "Number_of_Preferred_Time_Slots")
            number.text = str(c)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

# Set of subactivities has a set of preferred starting time
    def subactivities_preferredtimes(self, time):
        time_obj = self.env['op.subactivity.starting.time'].search([])
        for rec in time_obj:
            preferred_times = etree.SubElement(time, "ConstraintSubactivitiesPreferredStartingTimes")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            component = etree.SubElement(preferred_times, "Component_Number")
            component.text = str(rec.split_count)
            teacher = etree.SubElement(preferred_times, "Teacher_Name")
            teacher.text = rec.faculty_id.name
            student = etree.SubElement(preferred_times, "Students_Name")
            batch_name = rec.student_id.name
            if rec.group_id:
                batch_name = '%s %s' % (batch_name, rec.group_id.name)
            if rec.subgroup_id:
                batch_name = '%s %s' % (batch_name, rec.subgroup_id.name)
            student.text = batch_name
            subject = etree.SubElement(preferred_times, "Subject_Name")
            subject.text = rec.subject_id.name
            tag = etree.SubElement(preferred_times, "Activity_Tag_Name")
            tag.text = rec.activity_tag_id.name
            c = 0
            for line in rec.subactivity_starting_line_ids:
                if line.monday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Starting_Time")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Starting_Day")
                    preferred_day.text = 'Monday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Starting_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.tuesday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Starting_Time")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Starting_Day")
                    preferred_day.text = 'Tuesday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Starting_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.wednesday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Starting_Time")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Starting_Day")
                    preferred_day.text = 'Wednesday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Starting_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.thursday:
                    preferred_day = etree.SubElement(preferred_times, "Preferred_Starting_Day")
                    preferred_day.text = 'Thursday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Starting_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.friday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Starting_Time")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Starting_Day")
                    preferred_day.text = 'Friday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Starting_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.saturday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Starting_Time")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Starting_Day")
                    preferred_day.text = 'Saturday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Starting_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.sunday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Starting_Time")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Starting_Day")
                    preferred_day.text = 'Sunday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Starting_Hour")
                    preferred_hour.text = line.name
                    c += 1
            number = etree.SubElement(preferred_times, "Number_of_Preferred_Starting_Times")
            number.text = str(c)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

# Set of subactivity has a set of preferred time slots
    def subactivities_preferred_timeslots(self, time):
        time_obj = self.env['op.subactivities.timeslots'].search([])
        for rec in time_obj:
            preferred_times = etree.SubElement(time, "ConstraintSubactivitiesPreferredTimeSlots")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            component = etree.SubElement(preferred_times, "Component_Number")
            component.text = str(rec.split_count)
            teacher = etree.SubElement(preferred_times, "Teacher_Name")
            teacher.text = rec.faculty_id.name
            student = etree.SubElement(preferred_times, "Students_Name")
            batch_name = rec.student_id.name
            if rec.group_id:
                batch_name = '%s %s' % (batch_name, rec.group_id.name)
            if rec.subgroup_id:
                batch_name = '%s %s' % (batch_name, rec.subgroup_id.name)
            student.text = batch_name
            subject = etree.SubElement(preferred_times, "Subject_Name")
            subject.text = rec.subject_id.name
            tag = etree.SubElement(preferred_times, "Activity_Tag_Name")
            tag.text = rec.activity_tag_id.name
            c = 0
            for line in rec.subactivities_timeslots_line_ids:
                if line.monday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Day")
                    preferred_day.text = 'Monday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.tuesday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Day")
                    preferred_day.text = 'Tuesday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.wednesday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Day")
                    preferred_day.text = 'Wednesday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.thursday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Day")
                    preferred_day.text = 'Thursday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.friday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Day")
                    preferred_day.text = 'Friday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.saturday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Day")
                    preferred_day.text = 'Saturday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.sunday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Preferred_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Preferred_Day")
                    preferred_day.text = 'Sunday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Preferred_Hour")
                    preferred_hour.text = line.name
                    c += 1
            number = etree.SubElement(preferred_times, "Number_of_Preferred_Time_Slots")
            number.text = str(c)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

# Min days between a set of activities
    def min_days_activities(self, time):
        time_obj = self.env['op.mindays.activities'].search([])
        for rec in time_obj:
            preferred_times = etree.SubElement(time, "ConstraintMinDaysBetweenActivities")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            consecutive = etree.SubElement(preferred_times, "Consecutive_If_Same_Day")
            consecutive.text = 'true' if rec.same_day else 'false'
            number = etree.SubElement(preferred_times, "Number_of_Activities")
            number.text = str(len(rec.activities_ids))
            for act in rec.activities_ids:
                activity = etree.SubElement(preferred_times, "Activity_Id")
                activity.text = str(act.id)
            min_days = etree.SubElement(preferred_times, "MinDays")
            min_days.text = str(rec.min_days)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

# Max days between a set of activities
    def max_days_activities(self, time):
        time_obj = self.env['op.maxdays.activities'].search([])
        for rec in time_obj:
            preferred_times = etree.SubElement(time, "ConstraintMaxDaysBetweenActivities")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            number = etree.SubElement(preferred_times, "Number_of_Activities")
            number.text = str(len(rec.activities_ids))
            for act in rec.activities_ids:
                activity = etree.SubElement(preferred_times, "Activity_Id")
                activity.text = str(act.id)
            min_days = etree.SubElement(preferred_times, "MaxDays")
            min_days.text = str(rec.max_days)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

# An Activity ends Students day
    def activity_ends_studentsday(self, time):
        time_obj = self.env['op.activity.ends.day'].search([])
        for rec in time_obj:
            preferred_times = etree.SubElement(time, "ConstraintActivityEndsStudentsDay")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            activity = etree.SubElement(preferred_times, "Activity_Id")
            activity.text = str(rec.id)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

# A Set of Activities ends Students day
    def activities_ends_studentsday(self, time):
        time_obj = self.env['op.activities.ends.day'].search([])
        for rec in time_obj:
            preferred_times = etree.SubElement(time, "ConstraintActivitiesEndStudentsDay")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            teacher = etree.SubElement(preferred_times, "Teacher_Name")
            teacher.text = rec.faculty_id.name
            student = etree.SubElement(preferred_times, "Students_Name")
            student.text = rec.student_id.name
            subject = etree.SubElement(preferred_times, "Subject_Name")
            subject.text = rec.subject_id.name
            tag = etree.SubElement(preferred_times, "Activity_Tag_Name")
            tag.text = rec.activity_tag_id.name
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

# A set of activies have same starting time(day+hr)
    def activities_same_startingDH(self, time):
        time_obj = self.env['op.activities.same.starting.time'].search([])
        for rec in time_obj:
            preferred_times = etree.SubElement(time, "ConstraintActivitiesSameStartingTime")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            number = etree.SubElement(preferred_times, "Number_of_Activities")
            number.text = str(len(rec.activities_ids))
            for act in rec.activities_ids:
                activity = etree.SubElement(preferred_times, "Activity_Id")
                activity.text = str(act.id)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

# A set of activies have same starting time(any hr)
    def activities_same_startingH(self, time):
        time_obj = self.env['op.activities.same.starting.day'].search([])
        for rec in time_obj:
            preferred_times = etree.SubElement(time, "ConstraintActivitiesSameStartingDay")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            number = etree.SubElement(preferred_times, "Number_of_Activities")
            number.text = str(len(rec.activities_ids))
            for act in rec.activities_ids:
                activity = etree.SubElement(preferred_times, "Activity_Id")
                activity.text = str(act.id)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

# A set of activies have same starting time(any day)
    def activities_same_startingD(self, time):
        time_obj = self.env['op.activities.same.starting.hour'].search([])
        for rec in time_obj:
            preferred_times = etree.SubElement(time, "ConstraintActivitiesSameStartingHour")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            number = etree.SubElement(preferred_times, "Number_of_Activities")
            number.text = str(len(rec.activities_ids))
            for act in rec.activities_ids:
                activity = etree.SubElement(preferred_times, "Activity_Id")
                activity.text = str(act.id)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

# A set of activities takes max timeslots from selection
    def activities_max_timeslots(self, time):
        time_obj = self.env['op.activities.max.time.slots'].search([])
        for rec in time_obj:
            preferred_times = etree.SubElement(time, "ConstraintActivitiesOccupyMaxTimeSlotsFromSelection")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            number = etree.SubElement(preferred_times, "Number_of_Activities")
            number.text = str(len(rec.activities_ids))
            for act in rec.activities_ids:
                activity = etree.SubElement(preferred_times, "Activity_Id")
                activity.text = str(act.id)
            c = 0
            for line in rec.activities_max_timeslots_line_ids:
                if line.monday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Selected_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Selected_Day")
                    preferred_day.text = 'Monday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Selected_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.tuesday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Selected_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Selected_Day")
                    preferred_day.text = 'Tuesday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Selected_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.wednesday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Selected_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Selected_Day")
                    preferred_day.text = 'Wednesday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Selected_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.thursday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Selected_Time_Slot")
                    preferred_day = etree.SubElement(preferred_times, "Selected_Day")
                    preferred_day.text = 'Thursday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Selected_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.friday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Selected_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Selected_Day")
                    preferred_day.text = 'Friday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Selected_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.saturday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Selected_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Selected_Day")
                    preferred_day.text = 'Saturday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Selected_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.sunday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Selected_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Selected_Day")
                    preferred_day.text = 'Sunday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Selected_Hour")
                    preferred_hour.text = line.name
                    c += 1
            number = etree.SubElement(preferred_times, "Number_of_Selected_Time_Slots")
            number.text = str(c)
            max_num = etree.SubElement(preferred_times, "Max_Number_of_Occupied_Time_Slots")
            max_num.text = str(rec.max_occupied)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

# 2 Activities are ordered
    def two_activities_ordered(self, time):
        time_obj = self.env['op.two_activities.ordered'].search([])
        for rec in time_obj:
            preferred_times = etree.SubElement(time, "ConstraintTwoActivitiesOrdered")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            first = etree.SubElement(preferred_times, "First_Activity_Id")
            first.text = str(rec.activities_ids[0].id)
            second = etree.SubElement(preferred_times, "Second_Activity_Id")
            second.text = str(rec.activities_ids[1].id)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

# 2 Activities are consecutives
    def two_activities_consecutives(self, time):
        time_obj = self.env['op.two_activities.consecutive'].search([])
        for rec in time_obj:
            preferred_times = etree.SubElement(time, "ConstraintTwoActivitiesConsecutive")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            first = etree.SubElement(preferred_times, "First_Activity_Id")
            first.text = str(rec.activities_ids[0].id)
            second = etree.SubElement(preferred_times, "Second_Activity_Id")
            second.text = str(rec.activities_ids[1].id)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

# 2 Activities are grouped
    def two_activities_grouped(self, time):
        time_obj = self.env['op.two_activities.grouped'].search([])
        for rec in time_obj:
            preferred_times = etree.SubElement(time, "ConstraintTwoActivitiesGrouped")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            first = etree.SubElement(preferred_times, "First_Activity_Id")
            first.text = str(rec.activities_ids[0].id)
            second = etree.SubElement(preferred_times, "Second_Activity_Id")
            second.text = str(rec.activities_ids[1].id)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

# 3 Activities are grouped
    def three_activities_grouped(self, time):
        time_obj = self.env['op.three_activities.grouped'].search([])
        for rec in time_obj:
            preferred_times = etree.SubElement(time, "ConstraintThreeActivitiesGrouped")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            first = etree.SubElement(preferred_times, "First_Activity_Id")
            first.text = str(rec.activities_ids[0].id)
            second = etree.SubElement(preferred_times, "Second_Activity_Id")
            second.text = str(rec.activities_ids[1].id)
            third = etree.SubElement(preferred_times, "Second_Activity_Id")
            third.text = str(rec.activities_ids[2].id)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

# A set of Activities are not overlapping
    def activities_not_overlapping(self, time):
        time_obj = self.env['op.activities.not_overlap'].search([])
        for rec in time_obj:
            preferred_times = etree.SubElement(time, "ConstraintActivitiesNotOverlapping")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            number = etree.SubElement(preferred_times, "Number_of_Activities")
            number.text = str(len(rec.activities_ids))
            for act in rec.activities_ids:
                activity = etree.SubElement(preferred_times, "Activity_Id")
                activity.text = str(act.id)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

# A Max simultaneous activities from a set in selected timeslots
    def max_simultaneous_activities(self, time):
        time_obj = self.env['op.activities.max.simultaneous'].search([])
        for rec in time_obj:
            preferred_times = etree.SubElement(time, "ConstraintActivitiesMaxSimultaneousInSelectedTimeSlots")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            number = etree.SubElement(preferred_times, "Number_of_Activities")
            number.text = str(len(rec.activities_ids))
            for act in rec.activities_ids:
                activity = etree.SubElement(preferred_times, "Activity_Id")
                activity.text = str(act.id)
            c = 0
            for line in rec.activities_max_simultaneous_line_ids:
                if line.monday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Selected_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Selected_Day")
                    preferred_day.text = 'Monday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Selected_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.tuesday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Selected_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Selected_Day")
                    preferred_day.text = 'Tuesday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Selected_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.wednesday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Selected_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Selected_Day")
                    preferred_day.text = 'Wednesday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Selected_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.thursday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Selected_Time_Slot")
                    preferred_day = etree.SubElement(preferred_times, "Selected_Day")
                    preferred_day.text = 'Thursday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Selected_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.friday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Selected_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Selected_Day")
                    preferred_day.text = 'Friday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Selected_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.saturday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Selected_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Selected_Day")
                    preferred_day.text = 'Saturday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Selected_Hour")
                    preferred_hour.text = line.name
                    c += 1
                if line.sunday:
                    preferred_timeslots = etree.SubElement(preferred_times, "Selected_Time_Slot")
                    preferred_day = etree.SubElement(preferred_timeslots, "Selected_Day")
                    preferred_day.text = 'Sunday'
                    preferred_hour = etree.SubElement(preferred_timeslots, "Selected_Hour")
                    preferred_hour.text = line.name
                    c += 1
            number = etree.SubElement(preferred_times, "Number_of_Selected_Time_Slots")
            number.text = str(c)
            max_num = etree.SubElement(preferred_times, "Max_Number_of_Simultaneous_Activities")
            max_num.text = str(rec.max_simultaneous)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

    # Min gaps between a set of activities
    def activities_min_gap(self, time):
        time_obj = self.env['op.activities.min_gap'].search([])
        for rec in time_obj:
            preferred_times = etree.SubElement(time, "ConstraintMinGapsBetweenActivities")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            number = etree.SubElement(preferred_times, "Number_of_Activities")
            number.text = str(len(rec.activities_ids))
            for act in rec.activities_ids:
                activity = etree.SubElement(preferred_times, "Activity_Id")
                activity.text = str(act.id)
            min_gap = etree.SubElement(preferred_times, "MinGaps")
            min_gap.text = str(rec.min_gap)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

    # Space Constraints
    def spaceconstraint_compulsory(self, root):
        space = etree.SubElement(root, "Space_Constraints_List")
        compulsory = etree.SubElement(space, "ConstraintBasicCompulsorySpace")
        weight = etree.SubElement(compulsory, "Weight_Percentage")
        weight.text = "100"
        active = etree.SubElement(compulsory, "Active")
        active.text = "True"

    # Faculty Space Constraints
        homeroom = self.faculty_homeroom(space)
        set_of_homeroom = self.faculty_setof_homeroom(space)
        building_change = self.faculty_maxbuild_day(space)
        max_building_day = self.faculty_maxbuild_day(space)
        max_building_week = self.faculty_maxbuild_week(space)
        min_gaps_build = self.faculty_mingap(space)
        faculties_max_build = self.faculties_maxbuild(space)
        faculties_build_week = self.faculties_buildweek(space)
        faculties_mingap = self.faculties_mingaps(space)

    # Student Space Constraints
        student_homeroom = self.student_homeroom(space)
        student_set_of_homeroom = self.student_setof_homeroom(space)
        student_maxbuild_day = self.student_maxbuild_day(space)
        student_maxbuild_week = self.student_maxbuild_week(space)
        student_min_gap_build = self.student_min_gap_build(space)
        allstudents_maxbuild_day = self.allstudents_maxbuild_day(space)
        allstudents_min_gap_build = self.allstudents_min_gap_build(space)

    # Room,activity,tag_activity Space Constarints
        not_available_rooms = self.not_available_rooms(space)
        activity_room = self.activity_room(space)
        activity_rooms = self.activity_rooms(space)
        activities_sameroom = self.activities_sameroom(space)
        activities_diffroom = self.activities_diffroom(space)
        tag_activity_room = self.tag_activity_room(space)
        tag_activity_rooms = self.tag_activity_rooms(space)

    def faculty_homeroom(self, space):
        faculty = self.env['op.faculty'].search([])
        for r in faculty:
            if r.room.name > 0:
                room = etree.SubElement(space, "ConstraintTeacherHomeRoom")
                weight = etree.SubElement(room, "Weight_Percentage")
                weight_per = r.room_weight
                fac_name = r.name
                if r.middle_name:
                    fac_name = '%s %s' % (fac_name, r.middle_name)
                if r.last_name:
                    fac_name = '%s %s' % (fac_name, r.last_name)
                weight.text = str(weight_per)
                Name = etree.SubElement(room, "Teacher")
                Name.text = fac_name
                room_name = etree.SubElement(room, "Room")
                home_room = r.room.name
                room_name.text = str(home_room)
                active = etree.SubElement(room, "Active")
                active.text = "True"
                # comment = etree.SubElement(room, "Comments")
                # comment.text = "0"

    def faculty_setof_homeroom(self, space):
        faculty = self.env['op.faculty'].search([])
        for r in faculty:
            room = etree.SubElement(space, "ConstraintTeacherHomeRooms")
            weight = etree.SubElement(room, "Weight_Percentage")
            weight_per = r.room_weight
            fac_name = r.name
            if r.middle_name:
                fac_name = '%s %s' % (fac_name, r.middle_name)
            if r.last_name:
                fac_name = '%s %s' % (fac_name, r.last_name)
            weight.text = str(weight_per)
            Name = etree.SubElement(room, "Teacher")
            Name.text = fac_name
            c = 0
            if r.set_of_room:
                Number = etree.SubElement(room, "Number_of_Preferred_Rooms")
                for s in r.set_of_room:
                    room_name = etree.SubElement(room, "Preferred_Room")
                    set_of_homeroom = s.name
                    room_name.text = str(set_of_homeroom)
                    c += 1
                Number.text = str(c)
            active = etree.SubElement(room, "Active")
            active.text = "True"
            # comment = etree.SubElement(room, "Comments")
            # comment.text = "0"

    def faculty_maxbuild_day(self, space):
        faculty = self.env['op.faculty'].search([])
        for r in faculty:
            if r.max_building > 0:
                room = etree.SubElement(
                    space, "ConstraintTeacherMaxBuildingChangesPerDay")
                weight = etree.SubElement(room, "Weight_Percentage")
                weight_per = r.room_weight
                fac_name = r.name
                if r.middle_name:
                    fac_name = '%s %s' % (fac_name, r.middle_name)
                if r.last_name:
                    fac_name = '%s %s' % (fac_name, r.last_name)
                weight.text = str(weight_per)
                Name = etree.SubElement(room, "Teacher")
                Name.text = fac_name
                building_name = etree.SubElement(
                    room, "Max_Building_Changes_Per_Week")
                build_name = r.max_building
                building_name.text = str(build_name)
                active = etree.SubElement(room, "Active")
                active.text = "True"
                # comment = etree.SubElement(room, "Comments")
                # comment.text = "0"

    def faculty_maxbuild_week(self, space):
        faculty = self.env['op.faculty'].search([])
        for r in faculty:
            if r.max_build_week > 0:
                room = etree.SubElement(
                    space, "ConstraintTeacherMaxBuildingChangesPerWeek")
                weight = etree.SubElement(room, "Weight_Percentage")
                weight_per = r.room_weight
                weight.text = str(weight_per)
                building_name = etree.SubElement(
                    room, "Max_Building_Changes_Per_Week")
                max_build = r.max_build_week
                building_name.text = str(max_build)
                active = etree.SubElement(room, "Active")
                active.text = "True"
                # comment = etree.SubElement(room, "Comments")
                # comment.text = "0"

    def faculty_mingap(self, space):
        faculty = self.env['op.faculty'].search([])
        for r in faculty:
            if r.min_gap_build > 0:
                room = etree.SubElement(
                    space, "ConstraintTeacherMinGapsBetweenBuildingChanges")
                weight = etree.SubElement(room, "Weight_Percentage")
                weight_per = r.room_weight
                fac_name = r.name
                if r.middle_name:
                    fac_name = '%s %s' % (fac_name, r.middle_name)
                if r.last_name:
                    fac_name = '%s %s' % (fac_name, r.last_name)
                weight.text = str(weight_per)
                Name = etree.SubElement(room, "Teacher")
                Name.text = fac_name
                building_name = etree.SubElement(
                    room, "Min_Gaps_Between_Building_Changes")
                min_build_gap = r.min_gap_build
                building_name.text = str(min_build_gap)
                active = etree.SubElement(room, "Active")
                active.text = "True"
                # comment = etree.SubElement(room, "Comments")
                # comment.text = "0"

    def faculties_maxbuild(self, space):
        faculty = self.env['op.all.faculty.constraints'].search([])
        for r in faculty:
            if r.max_building_change > 0:
                room = etree.SubElement(
                    space, "ConstraintTeachersMaxBuildingChangesPerDay")
                weight = etree.SubElement(room, "Weight_Percentage")
                weight_per = r.weight_percent
                weight.text = str(weight_per)
                building_name = etree.SubElement(
                    room, "Max_Building_Changes_Per_Day")
                max_building_changes = r.max_building_change
                building_name.text = str(max_building_changes)
                active = etree.SubElement(room, "Active")
                active.text = "True"
                # comment = etree.SubElement(room, "Comments")
                # comment.text = "0"

    def faculties_buildweek(self, space):
        faculty = self.env['op.all.faculty.constraints'].search([])
        for r in faculty:
            if r.max_building_week > 0:
                room = etree.SubElement(
                    space, "ConstraintTeachersMaxBuildingChangesPerWeek")
                weight = etree.SubElement(room, "Weight_Percentage")
                weight_per = r.weight_percent
                weight.text = str(weight_per)
                building_name = etree.SubElement(
                    room, "Max_Building_Changes_Per_Week")
                max_building_changes = r.max_building_week
                building_name.text = str(max_building_changes)
                active = etree.SubElement(room, "Active")
                active.text = "True"
                # comment = etree.SubElement(room, "Comments")
                # comment.text = "0"

    def faculties_mingaps(self, space):
        faculty = self.env['op.all.faculty.constraints'].search([])
        for r in faculty:
            if r.min_gap_building > 0:
                room = etree.SubElement(
                    space, "ConstraintTeachersMinGapsBetweenBuildingChanges")
                weight = etree.SubElement(room, "Weight_Percentage")
                weight_per = r.weight_percent
                weight.text = str(weight_per)
                building_name = etree.SubElement(
                    room, "Min_Gaps_Between_Building_Changes")
                max_building_changes = r.min_gap_building
                building_name.text = str(max_building_changes)
                active = etree.SubElement(room, "Active")
                active.text = "True"
                # comment = etree.SubElement(room, "Comments")
                # comment.text = "0"

    def student_homeroom(self, space):
        student = self.env['student.time.constraints'].search([])
        for s in student:
            room = etree.SubElement(
                space, "ConstraintStudentsSetHomeRoom")
            weight = etree.SubElement(room, "Weight_Percentage")
            weight_per = s.weight_percent
            weight.text = str(weight_per)
            Name = etree.SubElement(room, "Students")
            batch_name = s.name.name
            if s.group_name:
                batch_name = '%s %s' % (batch_name, s.group_name.name)
            if s.subgroup_name:
                batch_name = '%s %s' % (batch_name, s.subgroup_name.name)
            Name.text = batch_name
            room_name = etree.SubElement(room, "Room")
            rooms = s.student_homeroom.name
            room_name.text = str(rooms)
            active = etree.SubElement(room, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def student_setof_homeroom(self, space):
        student = self.env['student.time.constraints'].search([])
        for r in student:
            room = etree.SubElement(space, "ConstraintStudentsSetHomeRooms")
            weight = etree.SubElement(room, "Weight_Percentage")
            weight_per = r.weight_percent
            weight.text = str(weight_per)
            Name = etree.SubElement(room, "Students")
            batch_name = r.name.name
            if r.group_name:
                batch_name = '%s %s' % (batch_name, r.group_name.name)
            if r.subgroup_name:
                batch_name = '%s %s' % (batch_name, r.subgroup_name.name)
            Name.text = batch_name
            c = 0
            if r.student_set_of_homerooms:
                Number = etree.SubElement(room, "Number_of_Preferred_Rooms")
                for s in r.student_set_of_homerooms:
                    room_name = etree.SubElement(room, "Preferred_Room")
                    set_of_homeroom = s.name
                    room_name.text = str(set_of_homeroom)
                    c += 1
                Number.text = str(c)
            active = etree.SubElement(room, "Active")
            active.text = "True"
            # comment = etree.SubElement(room, "Comments")
            # comment.text = "0"

    def student_maxbuild_day(self, space):
        student = self.env['student.time.constraints'].search([])
        for s in student:
            room = etree.SubElement(
                space, "ConstraintStudentsSetMaxBuildingChangesPerDay")
            weight = etree.SubElement(room, "Weight_Percentage")
            weight_per = s.weight_percent
            weight.text = str(weight_per)
            Name = etree.SubElement(room, "Students")
            batch_name = s.name.name
            if s.group_name:
                batch_name = '%s %s' % (batch_name, s.group_name.name)
            if s.subgroup_name:
                batch_name = '%s %s' % (batch_name, s.subgroup_name.name)
            Name.text = batch_name
            building_change = etree.SubElement(
                room, "Max_Building_Changes_Per_Day")
            max_building_change = s.max_building_changes
            building_change.text = str(max_building_change)
            active = etree.SubElement(room, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def student_maxbuild_week(self, space):
        student = self.env['student.time.constraints'].search([])
        for s in student:
            room = etree.SubElement(
                space, "ConstraintStudentsSetMaxBuildingChangesPerWeek")
            weight = etree.SubElement(room, "Weight_Percentage")
            weight_per = s.weight_percent
            weight.text = str(weight_per)
            Name = etree.SubElement(room, "Students")
            batch_name = s.name.name
            if s.group_name:
                batch_name = '%s %s' % (batch_name, s.group_name.name)
            if s.subgroup_name:
                batch_name = '%s %s' % (batch_name, s.subgroup_name.name)
            Name.text = batch_name
            building_change = etree.SubElement(
                room, "Max_Building_Changes_Per_Week")
            max_building_week = s.max_build_week
            building_change.text = str(max_building_week)
            active = etree.SubElement(room, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def student_min_gap_build(self, space):
        student = self.env['student.time.constraints'].search([])
        for s in student:
            room = etree.SubElement(
                space, "ConstraintStudentsSetMinGapsBetweenBuildingChanges")
            weight = etree.SubElement(room, "Weight_Percentage")
            weight_per = s.weight_percent
            weight.text = str(weight_per)
            Name = etree.SubElement(room, "Students")
            batch_name = s.name.name
            if s.group_name:
                batch_name = '%s %s' % (batch_name, s.group_name.name)
            if s.subgroup_name:
                batch_name = '%s %s' % (batch_name, s.subgroup_name.name)
            Name.text = batch_name
            building_change = etree.SubElement(
                room, "Min_Gaps_Between_Building_Changes")
            min_gap_building = s.min_gaps_building
            building_change.text = str(min_gap_building)
            active = etree.SubElement(room, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def allstudents_maxbuild_day(self, space):
        student = self.env['all.student.constraints'].search([])
        for s in student:
            room = etree.SubElement(
                space, "ConstraintStudentsMaxBuildingChangesPerDay")
            weight = etree.SubElement(room, "Weight_Percentage")
            weight_per = s.weight_percent
            weight.text = str(weight_per)
            building_change_day = etree.SubElement(
                room, "Max_Building_Changes_Per_Day")
            max_build_day = s.max_build
            building_change_day.text = str(max_build_day)
            active = etree.SubElement(room, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def allstudents_maxbuild_week(self, space):
        student = self.env['all.student.constraints'].search([])
        for s in student:
            room = etree.SubElement(
                space, "ConstraintStudentsMaxBuildingChangesPerWeek")
            weight = etree.SubElement(room, "Weight_Percentage")
            weight_per = s.weight_percent
            weight.text = str(weight_per)
            building_change_day = etree.SubElement(
                room, "Max_Building_Changes_Per_Day")
            max_build_day = s.max_build
            building_change_day.text = str(max_build_day)
            active = etree.SubElement(room, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def allstudents_min_gap_build(self, space):
        student = self.env['all.student.constraints'].search([])
        for s in student:
            room = etree.SubElement(
                space, "ConstraintStudentsMinGapsBetweenBuildingChanges")
            weight = etree.SubElement(room, "Weight_Percentage")
            weight_per = s.weight_percent
            weight.text = str(weight_per)
            building_change = etree.SubElement(
                room, "Min_Gaps_Between_Building_Changes")
            min_gap_building = s.min_gaps_build
            building_change.text = str(min_gap_building)
            active = etree.SubElement(room, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    # A rooms not available
    def not_available_rooms(self, space):
        room_obj = self.env['op.room.not.available'].search([])
        for rec in room_obj:
            not_rooms = etree.SubElement(space, "ConstraintRoomNotAvailableTimes")
            weight = etree.SubElement(not_rooms, "Weight_Percentage")
            weight.text = str(rec.weight)
            room = etree.SubElement(not_rooms, "Room")
            room.text = str(rec.room_id.name)
            c = 0
            for line in rec.room_not_available_line_ids:
                if line.monday:
                    preferred_starting_time = etree.SubElement(not_rooms, "Not_Available_Time")
                    preferred_starting_day = etree.SubElement(preferred_starting_time, "Day")
                    preferred_starting_day.text = 'Monday'
                    preferred_starting_hour = etree.SubElement(preferred_starting_time, "Hour")
                    preferred_starting_hour.text = line.name
                    c += 1
                if line.tuesday:
                    preferred_starting_time = etree.SubElement(not_rooms, "Not_Available_Time")
                    preferred_starting_day = etree.SubElement(preferred_starting_time, "Day")
                    preferred_starting_day.text = 'Tuesday'
                    preferred_starting_hour = etree.SubElement(preferred_starting_time, "Hour")
                    preferred_starting_hour.text = line.name
                    c += 1
                if line.wednesday:
                    preferred_starting_time = etree.SubElement(not_rooms, "Not_Available_Time")
                    preferred_starting_day = etree.SubElement(preferred_starting_time, "Day")
                    preferred_starting_day.text = 'Wednesday'
                    preferred_starting_hour = etree.SubElement(preferred_starting_time, "Hour")
                    preferred_starting_hour.text = line.name
                    c += 1
                if line.thursday:
                    preferred_starting_time = etree.SubElement(not_rooms, "Not_Available_Time")
                    preferred_starting_day = etree.SubElement(preferred_starting_time, "Day")
                    preferred_starting_day.text = 'Thursday'
                    preferred_starting_hour = etree.SubElement(preferred_starting_time, "Hour")
                    preferred_starting_hour.text = line.name
                    c += 1
                if line.friday:
                    preferred_starting_time = etree.SubElement(not_rooms, "Not_Available_Time")
                    preferred_starting_day = etree.SubElement(preferred_starting_time, "Day")
                    preferred_starting_day.text = 'Friday'
                    preferred_starting_hour = etree.SubElement(preferred_starting_time, "Hour")
                    preferred_starting_hour.text = line.name
                    c += 1
                if line.saturday:
                    preferred_starting_time = etree.SubElement(not_rooms, "Not_Available_Time")
                    preferred_starting_day = etree.SubElement(preferred_starting_time, "Day")
                    preferred_starting_day.text = 'Saturday'
                    preferred_starting_hour = etree.SubElement(preferred_starting_time, "Hour")
                    preferred_starting_hour.text = line.name
                    c += 1
                if line.sunday:
                    preferred_starting_time = etree.SubElement(not_rooms, "Not_Available_Time")
                    preferred_starting_day = etree.SubElement(preferred_starting_time, "Day")
                    preferred_starting_day.text = 'Sunday'
                    preferred_starting_hour = etree.SubElement(preferred_starting_time, "Hour")
                    preferred_starting_hour.text = line.name
                    c += 1
            num = etree.SubElement(not_rooms, "Number_of_Not_Available_Times")
            num.text = str(c)
            active = etree.SubElement(not_rooms, "Active")
            active.text = "true"
            comments = etree.SubElement(not_rooms, "Comments")
            comments.text = "Comments"

    # Subject has preferred Room
    def subject_room(self, space):
        subject_obj = self.env['op.subject.room'].search([])
        for rec in subject_obj:
            preferred_times = etree.SubElement(space, "ConstraintSubjectPreferredRoom")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            subject = etree.SubElement(preferred_times, "Subject")
            subject.text = rec.subject_id.name
            room = etree.SubElement(preferred_times, "Room")
            room.text = rec.room_id.name
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

    # Subject has a set of preferred rooms
    def subject_rooms(self, space):
        subject_obj = self.env['op.subject.rooms'].search([])
        for rec in subject_obj:
            preferred_times = etree.SubElement(space, "ConstraintSubjectPreferredRooms")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            subject = etree.SubElement(preferred_times, "Subject")
            subject.text = rec.subject_id.name
            number = etree.SubElement(preferred_times, "Number_of_Preferred_Rooms")
            number.text = str(len(rec.room_ids))
            for sub in rec.room_ids:
                activity = etree.SubElement(preferred_times, "Preferred_Room")
                activity.text = str(sub.name)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

    # Tag has preferred Room
    def tag_room(self, space):
        tag_obj = self.env['op.tag.room'].search([])
        for rec in tag_obj:
            preferred_times = etree.SubElement(space, "ConstraintActivityTagPreferredRoom")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            tag = etree.SubElement(preferred_times, "Activity_Tag")
            tag.text = rec.tag_id.name
            room = etree.SubElement(preferred_times, "Room")
            room.text = rec.room_id.name
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

    # Tag has a set of preferred rooms
    def tag_rooms(self, space):
        tag_obj = self.env['op.tag.rooms'].search([])
        for rec in tag_obj:
            preferred_times = etree.SubElement(space, "ConstraintActivityTagPreferredRooms")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            tag = etree.SubElement(preferred_times, "Activity_Tag")
            tag.text = rec.tag_id.name
            number = etree.SubElement(preferred_times, "Number_of_Preferred_Rooms")
            number.text = str(len(rec.room_ids))
            for sub in rec.room_ids:
                activity = etree.SubElement(preferred_times, "Preferred_Room")
                activity.text = str(sub.name)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

    # Activity has preferred Room
    def activity_room(self, space):
        activity_obj = self.env['op.activity.room'].search([])
        for rec in activity_obj:
            preferred_times = etree.SubElement(space, "ConstraintActivityPreferredRoom")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            activity = etree.SubElement(preferred_times, "Activity_Id")
            activity.text = str(rec.id)
            room = etree.SubElement(preferred_times, "Room")
            room.text = rec.room_id.name
            lock = etree.SubElement(preferred_times, "Permanently_Locked")
            lock.text = 'true' if rec.locked else 'false'
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

    # Activity has a set of preferred rooms
    def activity_rooms(self, space):
        activity_obj = self.env['op.activity.rooms'].search([])
        for rec in activity_obj:
            preferred_times = etree.SubElement(space, "ConstraintActivityPreferredRooms")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            activity = etree.SubElement(preferred_times, "Activity_Id")
            activity.text = str(rec.id)
            number = etree.SubElement(preferred_times, "Number_of_Preferred_Rooms")
            number.text = str(len(rec.room_ids))
            for act in rec.room_ids:
                activity = etree.SubElement(preferred_times, "Preferred_Room")
                activity.text = str(act.name)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

    # A Set of activities has same room if they are consecutive
    def activities_sameroom(self, space):
        activity_obj = self.env['op.consecutive.activities.same.room'].search([])
        for rec in activity_obj:
            preferred_times = etree.SubElement(space, "ConstraintActivitiesSameRoomIfConsecutive")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            number = etree.SubElement(preferred_times, "Number_of_Activities")
            number.text = str(len(rec.activities_ids))
            for act in rec.activities_ids:
                activity = etree.SubElement(preferred_times, "Activity_Id")
                activity.text = str(act.id)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

    # A Set of activities have max different room
    def activities_diffroom(self, space):
        activity_obj = self.env['op.activities.max.different.room'].search([])
        for rec in activity_obj:
            preferred_times = etree.SubElement(space, "ConstraintActivitiesOccupyMaxDifferentRooms")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            number = etree.SubElement(preferred_times, "Number_of_Activities")
            number.text = str(len(rec.activities_ids))
            for act in rec.activities_ids:
                activity = etree.SubElement(preferred_times, "Activity_Id")
                activity.text = str(act.id)
            max_num = etree.SubElement(preferred_times, "Max_Number_of_Different_Rooms")
            max_num.text = str(rec.max_diff_room)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

    # A Tag n Activity have preferred room
    def tag_activity_room(self, space):
        activity_obj = self.env['op.subject.tag.preferred.room'].search([])
        for rec in activity_obj:
            preferred_times = etree.SubElement(space, "ConstraintSubjectActivityTagPreferredRoom")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            subject = etree.SubElement(preferred_times, "Subject")
            subject.text = rec.subject_id.name
            tag = etree.SubElement(preferred_times, "Activity_Tag")
            tag.text = rec.activity_tag_id.name
            room = etree.SubElement(preferred_times, "Room")
            room.text = rec.room_id.name
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"

    # A Tag n Activity have set of preferred rooms
    def tag_activity_rooms(self, space):
        activity_obj = self.env['op.subject.tag.preferred.rooms'].search([])
        for rec in activity_obj:
            preferred_times = etree.SubElement(space, "ConstraintSubjectActivityTagPreferredRooms")
            weight = etree.SubElement(preferred_times, "Weight_Percentage")
            weight.text = str(rec.weight)
            subject = etree.SubElement(preferred_times, "Subject")
            subject.text = rec.subject_id.name
            tag = etree.SubElement(preferred_times, "Activity_Tag")
            tag.text = rec.activity_tag_id.name
            number = etree.SubElement(preferred_times, "Number_of_Preferred_Rooms")
            number.text = str(len(rec.room_ids))
            for act in rec.room_ids:
                room = etree.SubElement(preferred_times, "Preferred_Room")
                room.text = str(act.id)
            active = etree.SubElement(preferred_times, "Active")
            active.text = "true"
            comments = etree.SubElement(preferred_times, "Comments")
            comments.text = "Comments"
