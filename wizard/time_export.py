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
        # availability = self.faculty_notavailable(time)
        # max_day = self.faculty_maxday_constraint(time)
        # min_day = self.faculty_minday_constraint(time)
        # max_gaps = self.faculty_maxgap_day(time)
        # max_gaps_week = self.faculty_gapweek_constraint(time)
        # maxhr = self.faculty_maxhr_daily_constraint(time)
        # minhr_daily = self.faculty_minhr_daily_constraint(time)
        # maxhr_cont = self.faculty_maxhr_cont_constraint(time)
        # max_hr_cont_act = self.faculty_maxhr_activity_constraint(time)
        # faculty_interval = self.faculty_interval_maxdays_constraint(time)
        # faculties_maxday = self.faculties_maxday(time)
        # faculties_minday = self.faculties_minday(time)
        # faculties_maxgap = self.faculties_maxgap(time)
        # faculties_maxgap_week = self.faculties_maxgap_week(time)
        # maxhr_daily = self.faculties_maxhrs(time)
        # max_hrs_cont = self.faculties_maxhrs_cont(time)
        # min_hrs = self.faculties_minhrs(time)
        # faculties_maxhr = self.faculties_maxhr_activity(time)
        # faculties_interval = self.faculties_hr_activity(time)

    # Student Time Constraints
        student_notavailable = self.student_notavailable(time)
        student_maxday = self.student_maxday_constraint(time)
        student_maxgap_day = self.student_maxgap_day(time)
        # student_maxgap_week = self.student_maxgap_week(time)
        # student_secondhr = self.student_maxsecond(time)
        # student_maxhr_daily = self.student_maxhr_daily(time)
        # student_minhr_daily = self.student_minhr_daily(time)
        # student_maxhr_cont = self.student_maxhr_cont(time)
        # student_maxhr_actiivty = self.student_maxhr_activity(time)
        # student_maxhr_act = self.student_maxhr_daily(time)
        # student_interval = self.student_set_interval(time)
        # allstudents_maxday = self.allstudent_maxday_constraint(time)
        # allstudent_maxgap = self.allstudent_maxgap_day(time)
        # allstudent_week_maxgap = self.allstudent_maxgap_week(time)
        # allstudent_maxhr_second = self.allstudent_maxsecond(time)
        # allstudentm_maxhr_daily = self.allstudent_maxhr_daily(time)
        # allstudent_max_hr = self.allstudent_maxhr_cont(time)
        # allstudents_act_cont = self.allstudent_maxhr_activity(time)
        # allstudents_maxhr_act_cont = self.allstudent_maxhr_act_cont(time)
        # allstudent_interval = self.allstudent_set_interval(time)
        # allstudent_minhr_daily = self.allstudent_minhr_daily(time)

    def faculty_notavailable(self, time):
        faculty = self.env['op.faculty.not.available'].search([])
        for w in faculty:
            week_days = etree.SubElement(
                time, "ConstraintTeacherNotAvailableTimes")
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
            time = self.env['op.faculty.not.available.list'].search(
                [('faculty_id', '=', w.id)])
            count = 0
            for t in time:
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
                    time, "ConstraintTeacherActivityTagMaxHoursContinuously")
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
                    week_days, "Maximum_Hours_Continuously")
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
            if f.max_days_per_week > 0:
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
            if f.min_days_per_week > 0:
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
            if f.max_gaps_per_day > 0:
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
        for b in batch:
            week_days = etree.SubElement(
                time, "ConstraintStudentsSetNotAvailableTimes")
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
            time = self.env['op.breaks.constraints.line'].search(
                [('batch_constraint_id', '=', b.id)])
            count = 0
            for t in time:
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

    def student_maxhr_daily(self, time):
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
            max_gap_days = b.max_gaps_day
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
            max_gap_days = b.max_gaps_week
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
            max_gap_days = b.max_gaps_day
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
            max_hr = b.max_hrs_daily
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
            max_hr = b.max_hrs_daily
            max_hrs_daily.text = str(max_hr)
            activity_name = etree.SubElement(week_days, "Activity_Tag")
            activity = b.activity_name.name
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
            min_hr = b.min_hrs_daily
            min_hrs_daily.text = str(min_hr)
            batch_name = b.batch_name.name
            Name = etree.SubElement(week_days, "Students")
            Name.text = batch_name
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
            batch_name = b.batch_name.name
            Name = etree.SubElement(week_days, "Students")
            Name.text = batch_name
            activity_name = etree.SubElement(week_days, "Activity_Tag")
            activity = b.activity_name.name
            activity_name.text = activity
            active = etree.SubElement(week_days, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

    def allstudent_maxhr_act_cont(self, time):
        batch = self.env['all.student.constraints'].search([])
        for b in batch:
            week_days = etree.SubElement(
                time, "ConstraintStudentsActivityTagMaxHoursDaily")
            weight = etree.SubElement(week_days, "Weight_Percentage")
            weight_per = b.weight_percent
            weight.text = str(weight_per)
            max_hrs_daily = etree.SubElement(
                week_days, "Maximum_Hours_Continuously")
            max_hr = b.max_hrs_daily
            max_hrs_daily.text = str(max_hr)
            activity_name = etree.SubElement(week_days, "Activity_Tag")
            activity = b.activity_name.name
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
            interval_starts = b.interval_start.name
            interval_st.text = str(interval_starts)
            interval_en = etree.SubElement(week_days, "Interval_End_Hour")
            interval_ends = b.interval_end.name
            interval_en.text = str(interval_ends)
            active = etree.SubElement(week_days, "Active")
            active.text = "True"
            # comment = etree.SubElement(week_days, "Comments")
            # comment.text = "0"

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
