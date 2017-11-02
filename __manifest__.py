{
    'name': 'FET Data Export',
    'category': 'Education',
    'description': """
Export master data to generate Timetable in FET tool.

""",
    'version': '1.0',
    'depends': ['web','openeducat_classroom','openeducat_timetable','openeducat_core',],
    'data': [ 'wizard/data_export_view.xml',
                'views/configurations_view.xml',
                'views/timing.xml',
             ],
    'auto_install': False
}
