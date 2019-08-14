# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _

class LeadBrand(models.Model):
    _name = 'lead.brand'

    name = fields.Char("Name")
    desc = fields.Char("Description")
    avail = fields.Boolean("Available")

class LeadSeries(models.Model):
    _name = 'lead.series'

    name = fields.Char("Name")
    desc = fields.Char("Description")
    avail = fields.Boolean("Available")

class LeadCapacity(models.Model):
    _name = 'lead.capacity'

    name = fields.Char("Name")
    desc = fields.Char("Description")
    avail = fields.Boolean("Available")

class LeadFault(models.Model):
    _name = 'lead.fault'

    name = fields.Char("Name")
    desc = fields.Char("Description")
    avail = fields.Boolean("Available")

class LeadSolution(models.Model):
    _name = 'lead.solution'

    name = fields.Char("Name")
    desc = fields.Char("Description")
    avail = fields.Boolean("Available")


class Lead(models.Model):
    _inherit = 'crm.lead'

    service_ids = fields.Many2one('service.agreement',compute='_compute_service', string='Services')
    service_count = fields.Integer("Service Count",compute='_compute_service')
    brand = fields.Many2one('lead.brand',"Brand")
    series = fields.Many2one('lead.series',"Series")
    capacity = fields.Many2one('lead.capacity',"Capacity")
    fault = fields.Many2one('lead.fault',"Fault")
    solution = fields.Many2one('lead.solution',"Solution")
    cust_exist = fields.Boolean("Existing Customer")
    exist_partner_id = fields.Many2one("res.partner","Customer")
    # partner_id = fields.Many2one('res.partner', string='Customer', track_visibility='always', index=True,
    #     help="Linked partner (optional). Usually created when converting the lead.")

    @api.multi
    def action_service_agree_view(self):
        lead = self.env['crm.lead'].browse(self._context['active_id'])
        self_def_user = self.with_context(default_user_id=self.user_id.id)
        # partner_id = self_def_user._create_partner(
        #     lead.id, self.action, lead.partner_id.id)

        view_id = self.env.ref('deltatech_service.view_service_agreement_tree').id
        form_view_id = self.env.ref('deltatech_service.view_service_agreement_form').id
        context = self._context.copy()
        context['default_lead_id'] = self.id
        context['default_partner_id'] = self.partner_id.id
        return {
            'name':'Service Agreement',
            'view_type':'form',
            'view_mode':'tree',
            'res_model':'service.agreement',
            'view_id':view_id,
            'views':[(form_view_id,'form')],
            'type':'ir.actions.act_window',
            'target':'current',
            'context':context,
        }

    @api.multi
    def _compute_service(self):
        for lead in self:
            services = self.env['service.agreement'].search([('lead_id','=',lead.id)])
            # for line in order.order_line:
            #     invoices |= line.invoice_lines.mapped('invoice_id')
            lead.service_ids = services
            lead.service_count = len(services)

    @api.multi
    def action_view_services(self):
        if self.service_ids:
            return {
                    'name': _('Service Agreement'),
                    'type': 'ir.actions.act_window',
                    'res_model': 'service.agreement',
                    'views': [(False, 'form')],
                    'res_id': self.service_ids.id,
                    'target': 'current',
                    'context': {},
                }

# class Lead2OpportunityPartner(models.TransientModel):
#     _inherit = 'crm.lead2opportunity.partner'
#
#     @api.multi
#     def action_service_agree_view(self):
#         lead = self.env['crm.lead'].browse(self._context['active_id'])
#         self_def_user = self.with_context(default_user_id=self.user_id.id)
#         partner_id = self_def_user._create_partner(
#             lead.id, self.action, lead.partner_id.id)
#
#         view_id = self.env.ref('deltatech_service.view_service_agreement_tree').id
#         form_view_id = self.env.ref('deltatech_service.view_service_agreement_form').id
#         context = self._context.copy()
#         context['default_lead_id'] = context['active_id']
#         context['default_partner_id'] = partner_id if self.action == 'create' else self.partner_id.id
#         return {
#             'name':'Service Agreement',
#             'view_type':'form',
#             'view_mode':'tree',
#             'res_model':'service.agreement',
#             'view_id':view_id,
#             'views':[(form_view_id,'form')],
#             'type':'ir.actions.act_window',
#             'target':'current',
#             'context':context,
#         }

# class PartnerBinding(models.TransientModel):
#     _inherit = 'crm.partner.binding'
#
#     action = fields.Selection([
#         ('exist', 'Link to an existing customer'),
#         ('create', 'Create a new customer')
#     ], 'Related Customer', required=True)
#     partner_id = fields.Many2one('res.partner', 'Customer')
