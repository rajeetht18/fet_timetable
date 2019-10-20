from odoo import http
from odoo.http import Response
from odoo.exceptions import UserError
from odoo.http import request
import json
import datetime


class FetchLead(http.Controller):

    @http.route("/api/fetch_lead/", auth='public', methods=['GET'], type='json')
    def index(self, **kw):
        print("-=------------------------")
        try:
            if kw.get('GLUSR_MOBILE') and kw.get('GLUSR_MOBILE_KEY'):
                # if kw.get('Start_Time') and kw['Start_Time'] == datetime.strptime(kw['Start_Time'], "%d-%b-%Y %H-%M-%S").strftime('%d-%b-%Y %H-%M-%S') and if kw.get('End_Time') and kw['End_Time'] == datetime.strptime(kw['End_Time'], "%d-%b-%Y %H-%M-%S").strftime('%d-%b-%Y %H-%M-%S'):
                #     url = "https://mapi.indiamart.com/wservce/enquiry/listing/GLUSR_MOBILE/%s/GLUSR_MOBILE_KEY/%s/Start_Time/%s/End_Time/%s/"%(str(kw['GLUSR_MOBILE']),str(kw.['GLUSR_MOBILE']),str(kw['Start_Time']),str(kw['End_Time']))

                if kw['Start_Time'] and kw['End_Time']:
                    url = "https://mapi.indiamart.com/wservce/enquiry/listing/GLUSR_MOBILE/%s/GLUSR_MOBILE_KEY/%s/Start_Time/%s/End_Time/%s/"%(str(kw['GLUSR_MOBILE']),str(kw['GLUSR_MOBILE_KEY']),str(kw['Start_Time']),str(kw['End_Time']))
                    response = requests.get(url,params=None)
                else:
                    url = "https://mapi.indiamart.com/wservce/enquiry/listing/GLUSR_MOBILE/%s/GLUSR_MOBILE_KEY/%s/"%(str(kw['GLUSR_MOBILE']),str(kw['GLUSR_MOBILE_KEY']))
                    response = requests.get(url,params=None)

                return {"status": "Record is created successfully"}
        except Exception as e:
            return e

    if __name__ == 'odoo.addons.indiamart_integration.models.controllers':
        print(__name__,"--------------------------------")
        print ("hooooooooooooooooooooooooooooooo")
        self.index()