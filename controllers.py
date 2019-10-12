from odoo import http
from odoo.http import Response
from odoo.exceptions import UserError
from odoo.http import request
import mimetypes
import json


class FetchLead(http.Controller):
    @http.route("/api/fetch_lead/", auth='public', methods=['POST'], type='json')
    def index(self, **kw):
        try:
            token = "MTU3MDI3OTQ0Ni44MjEylzE3NDQzOTY="
            try:
                if kw['GLUSR_MOBILE_KEY'] != token:
                    raise UserError("CRM key that you are using is incorrect. Kindly use the correct CRM key as provided in email or sms.")
            except:
                raise UserError("Invalid CRM Key. Please try with a valid one.")

            if kw.get('GLUSR_MOBILE') and kw.get('GLUSR_MOBILE_KEY'):
                if kw.get('Start_Time') and kw['Start_Time'] == datetime.strptime(kw['Start_Time'], "%d-%b-%Y %H-%M-%S").strftime('%d-%b-%Y %H-%M-%S') and if kw.get('End_Time') and kw['End_Time'] == datetime.strptime(kw['End_Time'], "%d-%b-%Y %H-%M-%S").strftime('%d-%b-%Y %H-%M-%S'):
                    url = "https://mapi.indiamart.com/wservce/enquiry/listing/GLUSR_MOBILE/%s/GLUSR_MOBILE_KEY/%s/Start_Time/%s/End_Time/%s/"%(str(kw['GLUSR_MOBILE']),str(kw.['GLUSR_MOBILE']),str(kw['Start_Time']),str(kw['End_Time']))
                    response = requests.get(url,params=None)
                    return response

                elif kw.get('Start_Time') and kw['Start_Time'] == datetime.strptime(kw['Start_Time'], "%d-%b-%Y ").strftime('%d-%b-%Y') and if kw.get('End_Time') and kw['End_Time'] == datetime.strptime(kw['End_Time'], "%d-%b-%Y").strftime('%d-%b-%Y'):

                else:

                        
            url = "https://mapi.indiamart.com/wservce/enquiry/listing/GLUSR_MOBILE/%s/GLUSR_MOBILE_KEY/%s/Start_Time/%s/End_Time/%s/"%(str(kw['GLUSR_MOBILE']),str(kw.['GLUSR_MOBILE']),str(kw['Start_Time']),str(kw['End_Time']))
            response = requests.get(url,params=None)
            return {"id": record.id, "LSQID": kw.get('lsq_id'), "status": "Record is created successfully"}
        except Exception as e:
            return e
