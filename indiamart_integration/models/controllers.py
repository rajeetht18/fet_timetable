from odoo import http
from odoo.http import Response
from odoo.exceptions import UserError
from odoo.http import request
import json
from datetime import datetime
from odoo import fields, models, api
# import urllib.request
import requests


class FetchLead(models.Model):
    _name = 'im.api.fetchlead'

    # @http.route("/api/fetch_lead/", auth='public', methods=['GET'], type='json')
    def call_url(self):
        
        model = self.env['im.api.integration'].search([])[0]
        if model.glusr_mobile and model.glusr_mobile_key:
            if model.timestamp_bool == False and model.date1 and model.date2:
                d1 = datetime.strptime(model.date1,"%Y-%m-%d").strftime("%d-%b-%Y")
                d2 = datetime.strptime(model.date2,"%Y-%m-%d").strftime("%d-%b-%Y")
                url = "https://mapi.indiamart.com/wservce/enquiry/listing/GLUSR_MOBILE/%s/GLUSR_MOBILE_KEY/%s/Start_Time/%s/End_Time/%s/"%(str(model.glusr_mobile),str(model.glusr_mobile_key),str(d1),str(d2))
                response = requests.get(url,params=None)
                print(url,response,"1111111111111111111111")
            elif model.timestamp_bool == True and model.time1 and model.time2:
                print (model.time1,model.time2,"helllooooooooooooooooo")
                t1 = datetime.strptime(model.time1,"%Y-%m-%d %H:%M:%S").strftime("%d-%b-%Y %H:%M:%S")
                t2 = datetime.strptime(model.time2,"%Y-%m-%d %H:%M:%S").strftime("%d-%b-%Y %H:%M:%S")
                url = "https://mapi.indiamart.com/wservce/enquiry/listing/GLUSR_MOBILE/%s/GLUSR_MOBILE_KEY/%s/Start_Time/%s/End_Time/%s/"%(str(model.glusr_mobile),str(model.glusr_mobile_key),str(t1),str(t2))
                print(url,"-----------")
                response = requests.get(url,params=None)
                print(response.text,"2222222222222222222222")
            else:
                url = "https://mapi.indiamart.com/wservce/enquiry/listing/GLUSR_MOBILE/%s/GLUSR_MOBILE_KEY/%s/"%(str(model.glusr_mobile),str(model.glusr_mobile_key))
                response = requests.get(url,params=None)
                print(url,response,"33333333333333333333333333")
           
            if response:
                print(response,"res-------->>>>")
                for val in json.loads(response.text):
                    i =1
                    print(val,i,"kooooooooooooooooooooooooooi---------------->>>>>")
                    res = {'name':val['SUBJECT'] if val['SUBJECT'] else False,
                            'contact_name':val['SENDERNAME'] if val['SENDERNAME'] else False,
                            'mobile':val['MOB'] if val['MOB'] else False,
                            'email_from':val['SENDEREMAIL'] if str(val['SENDEREMAIL']) != 'null' else False}
                    # print (res,"----")
                    lead = self.env['crm.lead'].create(res)
                    print(lead)