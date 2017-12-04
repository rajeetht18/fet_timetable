# -*- coding: utf-8 -*-
from odoo import api, fields, models
from lxml import etree
import base64
import datetime
import odoo.tools.config as config


class fettimetable_data_export(models.TransientModel):
    _name = 'fettimetable.data.export'

    version = fields.Char("FET Version", default='5.28.6',required=True, help="Fill the FET version in which you are using currently.")
    filedata = fields.Binary('File', readonly=True)

    def export_days(self, root):
        days = self.env['generate.time.table'].search([])
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        Days_List = etree.SubElement(root, "Days_List")
        Number_of_Days = etree.SubElement(Days_List, "Number_of_Days")
        Number_of_Days.text = "5"
        for rec in days:
            Days = etree.SubElement(Days_List, "Day")
            Name = etree.SubElement(Days, "Name")
            Name.text = rec

    def export_hours(self, root):
        timings = self.env['op.timing'].search([], order='sequence')
        total_hours = len(timings)
        Hours_List = etree.SubElement(root, "Hours_List")
        Number_of_Hours = etree.SubElement(Hours_List, "Number_of_Hours")
        Number_of_Hours.text = str(total_hours)
        for records in timings:
            hr_name = records.name
            Hours = etree.SubElement(Hours_List, "Hour")
            Name = etree.SubElement(Hours, "Name")
            Name.text = str(hr_name)

    def export_students(self, root):
        batch = self.env['op.batch'].search([])
        current_date = str(datetime.date.today())
        Students_List = etree.SubElement(root, "Students_List")
        for rec in batch:
            start_date = rec.start_date
            end_date = rec.end_date
            if start_date <= current_date <= end_date:
                Year = etree.SubElement(Students_List, "Year")
                Name = etree.SubElement(Year, "Name")
                Name.text = rec.name
                students = self.env['op.student.course'].search_count(
                    [('batch_id', '=', rec.id)])
                Number_of_Students = etree.SubElement(
                    Year, "Number_of_Students")
                Number_of_Students.text = str(students)
            for g in rec.group_ids:
                group = '%s %s' % (rec.name, g.name)
                group_list = etree.SubElement(Year, "Group")
                group_name = etree.SubElement(group_list, "Name")
                group_name.text = group
                group_of_students = etree.SubElement(
                    group_list, "Number_of_Students")
                group_students = self.env['op.student.course'].search_count(
                    [('batch_id', '=', rec.id), ('group_id', '=', g.id)])
                group_of_students.text = str(group_students)
                for s in g.subgroup_ids:
                    subgroup = '%s %s %s' % (rec.name, g.name, s.name)
                    subgroup_list = etree.SubElement(group_list, "Subgroup")
                    subgroup_name = etree.SubElement(subgroup_list, "Name")
                    subgroup_name.text = subgroup
                    subgroup_of_students = etree.SubElement(
                        subgroup_list, "Number_of_Students")
                    subgroup_students = self.env['op.student.course'].search_count(
                        [('batch_id', '=', rec.id), ('group_id', '=', g.id), ('subgroup_id', '=', s.id)])
                    subgroup_of_students.text = str(subgroup_students)

    def export_faculties(self, root):
        faculties = self.env['op.faculty'].search([])
        Teachers_List = etree.SubElement(root, "Teachers_List")
        for records in faculties:
            fac_name = records.name
            if records.middle_name:
                fac_name = '%s %s' % (fac_name, records.middle_name)
            if records.last_name:
                fac_name = '%s %s' % (fac_name, records.last_name)
            Teacher = etree.SubElement(Teachers_List, "Teacher")
            Name = etree.SubElement(Teacher, "Name")
            Name.text = fac_name

    def export_courses(self, root):
        subjects = self.env['op.subject'].search([])
        Subjects_List = etree.SubElement(root, "Subjects_List")
        for subject in subjects:
            Subject = etree.SubElement(Subjects_List, "Subject")
            Name = etree.SubElement(Subject, "Name")
            Name.text = subject.name

    def activity_tag_list(self, root):
        activity_tag_list = etree.SubElement(root, "Activity_Tags_List")
        activity_tag = etree.SubElement(activity_tag_list,  "Activity_Tag")
        name = etree.SubElement(activity_tag, "Name")
        name.text = "Teaching"

    def activities(self, root):
        activities_list = etree.SubElement(root, "Activities_List")
        sessions = self.env['op.faculty'].search([])
        for s in sessions:
            for line in s.class_details:
                activity = etree.SubElement(activities_list, "Activity")
                teacher = etree.SubElement(activity, "Teacher")
                fac_name = s.name
                if s.middle_name:
                    fac_name = '%s %s' % (fac_name, s.middle_name)
                if s.last_name:
                    fac_name = '%s %s' % (fac_name, s.last_name)
                teacher.text = fac_name
                subject = etree.SubElement(activity, "Subject")
                subject.text = line.subject_id.name
                activity_tag = etree.SubElement(activity, "Activity_Tag")
                activity_tag.text = "Teaching"
                students = etree.SubElement(activity,"Students")
                students.text = line.batch_id.name
                duration = etree.SubElement(activity, "Duration")
                duration.text = "1"
                total_duration = etree.SubElement(activity, "Total_Duration")
                total_duration.text = "1"
                id_count = etree.SubElement(activity, "Id")
                id_count.text = str(line.id)
                activity_group_id = etree.SubElement(activity, "Activity_Group_Id")
                activity_group_id.text = "0"
                active = etree.SubElement(activity, "Active")
                active.text = "true"
                comments = etree.SubElement(activity, "Comments")
                #comments.text = " "


    def rooms(self, root):
        buildings = etree.SubElement(root, "Buildings_List")
        room_list = etree.SubElement(root, "Rooms_List")
        rooms = self.env['op.classroom'].search([])
        for r in rooms:
            room = etree.SubElement(room_list, "Room")
            room_name = etree.SubElement(room, "Name")
            room_name.text = r.name
            building = etree.SubElement(room, "Building")
            capacity = etree.SubElement(room, "Capacity")
            capacity.text = str(r.capacity)

    def export_file(self):
        root = etree.Element("fet")
        root.set("version", self.version)
        inst_name = etree.SubElement(root, "Institution_Name")
        user = self.env['res.users'].search([('id', '=', self.env.uid)])
        inst_name.text = user.partner_id.company_name
        comment = etree.SubElement(root, "Comments")
        comment.text = "comment"

        Days_List = self.export_days(root)
        Hours_List = self.export_hours(root)
        Students_List = self.export_students(root)
        Teachers_List = self.export_faculties(root)
        Subjects_List = self.export_courses(root)
        time_compulsory = self.constraint_compulsory(root)
        space_compulsory = self.spaceconstraint_compulsory(root)
        self.activity_tag_list(root)
        self.activities(root)
        self.rooms(root)

        xmlstr = etree.tostring(root, encoding="utf-8", xml_declaration=True)
        file = base64.encodestring(xmlstr)
        self.filedata = file
        # set up your output file url:
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        file_url = base_url + \
            "/web/content?model=fettimetable.data.export&field=filedata&id=%s" % (
                self.id)
        return {
            'type': 'ir.actions.act_url',
            'url': file_url,
            'target': 'current',
        }
