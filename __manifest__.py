{
    'name': 'FET Data Export',
    'category': 'Education',
    'description': """
Export master data to generate Timetable in FET tool.

""",
    'version': '1.0',
    'depends': ['web', 'openeducat_erp'],
    'data': [
        'wizard/data_export_view.xml',
        'views/student_view.xml',
        'views/faculty_view.xml',
        'views/classroom_view.xml',
        'views/activity_tags_view.xml',
        'views/batch_view.xml',
        'views/group_view.xml',
        'views/subgroup_view.xml',
        'views/timetable_days_config_view.xml',
        'views/break_time_view.xml',
        'views/faculty_not_available.xml',
        'views/time_constraints_view.xml',
        'views/faculty_constraints_view.xml',
        'views/faculty_act_maxhr_view.xml',
        'views/student_constraint_view.xml',
        'views/all_students_constraint_view.xml',
        'views/time_activity_view.xml',
        'views/time_activities_view.xml',
        'views/space_constraints_view.xml',
        'views/menu.xml',


    ],
    'auto_install': False,
}
