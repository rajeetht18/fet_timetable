from odoo import http
from odoo.http import Response
from odoo.exceptions import UserError
from odoo.http import request
import json
from datetime import datetime
from odoo import fields, models, api
import urllib.request


class FetchLead(models.Model):
    _name = 'im.api.fetchlead'

    # @http.route("/api/fetch_lead/", auth='public', methods=['GET'], type='json')
    def call_url(self):
        
        model = self.env['im.api.integration'].search([])[0]
        if model.glusr_mobile and model.glusr_mobile_key:
            if model.timestamp_bool == False and model.date1 and model.date2:
                print ("helloooooooo111")
                d1 = datetime.strptime(model.date1,"%Y-%m-%d").strftime("%d-%b-%Y")
                d2 = datetime.strptime(model.date2,"%Y-%m-%d").strftime("%d-%b-%Y")
                print (d,"------->>>DDDDDDDDDDDDDDDDDDDDD")
                url = "https://mapi.indiamart.com/wservce/enquiry/listing/GLUSR_MOBILE/%s/GLUSR_MOBILE_KEY/%s/Start_Time/%s/End_Time/%s/"%(str(model.glusr_mobile),str(model.glusr_mobile_key),str(d1),str(d2))
                print (url)
                with urllib.request.urlopen(url) as response:
                    print(response,"------re----------------")
                # response = request.get(url,params=None)
                # print(url,response,"1111111111111111111111")
            elif model.timestamp_bool == True and model.time1 and model.time2:
                print (model.time1,model.time2,"helllooooooooooooooooo")
                t1 = datetime.strptime(model.time1,"%Y-%m-%d %H:%M:%S").strftime("%d-%b-%Y %H:%M:%S")
                t2 = datetime.strptime(model.time2,"%Y-%m-%d %H:%M:%S").strftime("%d-%b-%Y %H:%M:%S")
                url = "https://mapi.indiamart.com/wservce/enquiry/listing/GLUSR_MOBILE/%s/GLUSR_MOBILE_KEY/%s/Start_Time/%s/End_Time/%s/"%(str(model.glusr_mobile),str(model.glusr_mobile_key),str(t1),str(t2))
                print(url,"-----------")
                with urllib.request.urlopen(url) as response:
                    print(response,"------re----------------")
                # response = request.get(url,params=None)
                # print(url,response,"2222222222222222222222")
            else:
                url = "https://mapi.indiamart.com/wservce/enquiry/listing/GLUSR_MOBILE/%s/GLUSR_MOBILE_KEY/%s/"%(str(model.glusr_mobile),str(model.glusr_mobile_key))
                response = request.get(url,params=None)
                print(url,response,"33333333333333333333333333")
                # print (response)
            print("kooooooooooooooooooooooooi")
           
            res = [{
            "RN": "1",
            "QUERY_ID": "1143130518",
            "QTYPE": "W",
            "SENDERNAME": "Kenneth",
            "SENDEREMAIL": "kennykavilakazi@gmail.com",
            "SUBJECT": "Requirement for BGA Reballing Services",
            "name": "Requirement for BGA Reballing Services",
            "DATE_RE": "10 Oct 2019",
            "DATE_R": "10-Oct-19",
            "DATE_TIME_RE": " 10-Oct-2019 10:37:24 PM",
            "GLUSR_USR_COMPANYNAME": 'null',
            "READ_STATUS": 'null',
            "SENDER_GLUSR_USR_ID": "90137193",
            "MOB": "+27-614694643",
            "COUNTRY_FLAG": "https:\/\/1.imimg.com\/country-flags\/small\/za_flag_s.png",
            "QUERY_MODID": "TDW",
            "LOG_TIME": "20191010223724",
            "QUERY_MODREFID": "11485791233",
            "DIR_QUERY_MODREF_TYPE": "2",
            "ORG_SENDER_GLUSR_ID": "90137193",
            "ENQ_MESSAGE": "BGA Reballing Services- Send us quotation & details of 'BGA Reballing Services'.",
            "ENQ_ADDRESS": ", , , ",
            "ENQ_CALL_DURATION": 'null',
            "ENQ_RECEIVER_MOB": 'null',
            "ENQ_CITY": 'null',
            "ENQ_STATE": 'null',
            "PRODUCT_NAME": "BGA Reballing Services",
            "COUNTRY_ISO": "ZA",
            "EMAIL_ALT": 'null',
            "MOBILE_ALT": 'null',
            "PHONE": 'null',
            "PHONE_ALT": 'null',
            "IM_MEMBER_SINCE": "Jul-2019",
            "TOTAL_COUNT": "649"
            },
            {
            "RN": "2",
            "QUERY_ID": "1143102827",
            "QTYPE": "W",
            "SENDERNAME": "Imran",
            "SENDEREMAIL": 'null',
            "SUBJECT": "Requirement for Test Benches",
            "name": "Requirement for Test Benches",
            "DATE_RE": "10 Oct 2019",
            "DATE_R": "10-Oct-19",
            "DATE_TIME_RE": " 10-Oct-2019 09:32:04 PM",
            "GLUSR_USR_COMPANYNAME": 'null',
            "READ_STATUS": 'null',
            "SENDER_GLUSR_USR_ID": "93779751",
            "MOB": "+91-9640592825",
            "COUNTRY_FLAG": "https:\/\/1.imimg.com\/country-flags\/small\/in_flag_s.png",
            "QUERY_MODID": "IMOB",
            "LOG_TIME": "20191010213204",
            "QUERY_MODREFID": "11396822573",
            "DIR_QUERY_MODREF_TYPE": "2",
            "ORG_SENDER_GLUSR_ID": "93779751",
            "ENQ_MESSAGE": "I am interested in Test Benches",
            "ENQ_ADDRESS": ", , , ",
            "ENQ_CALL_DURATION": 'null',
            "ENQ_RECEIVER_MOB": 'null',
            "ENQ_CITY": 'null',
            "ENQ_STATE": 'null',
            "PRODUCT_NAME": "Test Benches",
            "COUNTRY_ISO": "IN",
            "EMAIL_ALT": 'null',
            "MOBILE_ALT": 'null',
            "PHONE": 'null',
            "PHONE_ALT": 'null',
            "IM_MEMBER_SINCE": "Sep-2019",
            "TOTAL_COUNT": "649"
            }]

            for val in res:
                res = {'name':val['name'],
                        'contact_name':val['SENDERNAME'],
                        'mobile':val['MOB'].split('-')[1],
                        'email_from':val['SENDEREMAIL'] if str(val['SENDEREMAIL']) != 'null' else False}
                # print (res,"----")
                lead = self.env['crm.lead'].create(res)
                print(lead)