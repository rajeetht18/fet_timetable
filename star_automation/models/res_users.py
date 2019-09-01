# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _

class UsersCategory(models.Model):
    _name = 'users.category'

    name = fields.Char("Name")
    desc = fields.Char("Description")

class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_category_id = fields.Many2one('users.category',"Partner Category")
    partner_reference = fields.Char("Reference",readonly="1")

    # @api.multi
    # def name_get(self):
    #     res = super(ResPartner, self).name_get()
    #     ret_value = []
    #     for value in res:
    #         mobile_rec = self.browse(value[0])
    #         if mobile_rec.mobile:
    #            ret_value.append((value[0], "%s [%s]"%(value[1], mobile_rec.mobile)))
    #         else:
    #             ret_value.append((value[0], "%s "%(value[1])))
    #     return ret_value


    @api.multi
    def name_get(self):
        res = super(ResPartner, self).name_get()
        result = []
        for record in self:
            name = record.name+'('+ str(record.partner_reference) +'-'+ str(record.city) +'-'+str(record.state_id.name) +')'
            result.append((record.id,name))
        print (result)
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            if self.search([('city','ilike',name)] + args, limit=limit):
                recs = self.search([('city','ilike',name)] + args, limit=limit)
            elif self.search([('state_id.name','ilike',name)] + args, limit=limit):
                recs = self.search([('state_id.name','ilike',name)] + args, limit=limit)
        if not recs:
            recs = self.search([('name', operator, name)] + args, limit=limit)
        return recs.name_get()

    @api.model
    def create(self,vals):
        vals['partner_reference'] = self.env['ir.sequence'].next_by_code('partner.reference') or _('New')
        return super(ResPartner, self).create(vals)

class ResUsers(models.Model):
    _inherit = 'res.users'

    front_office = fields.Selection([('user','User'),('manager','Manager')],'Front Office')
    app_dptmnt = fields.Selection([('user','User'),('manager','Manager')],'Application  Department')
    hw_dptmnt = fields.Selection([('user','User'),('manager','Manager')],'Hardware Department')
    purchase_dptmnt = fields.Selection([('user','User'),('manager','Manager')],'Purchase Department')
    testing_dptmnt = fields.Selection([('user','User'),('manager','Manager')],'Testing Department')
    accnt_dptmnt = fields.Selection([('user','User'),('manager','Manager')],'Accounts Department')
    packing_dptmnt = fields.Selection([('user','User'),('manager','Manager')],'Packing Department')
    administrator = fields.Selection([('user','User'),('manager','Manager')],'Administrator')




    @api.multi
    def _update_user_groups_view(self):
        """ Modify the view with xmlid ``base.user_groups_view``, which inherits
            the user form view, and introduces the reified group fields.
        """
        if self._context.get('install_mode'):
            # use installation/admin language for translatable names in the view
            user_context = self.env['res.users'].context_get()
            self = self.with_context(**user_context)

        # We have to try-catch this, because at first init the view does not
        # exist but we are already creating some basic groups.
        view = self.env.ref('base.user_groups_view', raise_if_not_found=False)
        if view and view.exists() and view._name == 'ir.ui.view':
            group_no_one = view.env.ref('base.group_no_one')
            xml1, xml2 = [], []
            xml1.append(E.separator(string=_('Application Accesses'), colspan="2"))
            for app, kind, gs in self.get_groups_by_application():
                # hide groups in categories 'Hidden' and 'Extra' (except for group_no_one)
                attrs = {}
                if app.xml_id in ('base.module_category_hidden', 'base.module_category_extra', 'base.module_category_usability'):
                    attrs['groups'] = 'base.group_no_one'

                if kind == 'selection':
                    # application name with a selection field
                    field_name = name_selection_groups(gs.ids)
                    xml1.append(E.field(name=field_name, **attrs))
                    xml1.append(E.newline())
                else:
                    # application separator with boolean fields
                    app_name = app.name or _('Other')
                    xml2.append(E.separator(string=app_name, colspan="4", **attrs))
                    for g in gs:
                        field_name = name_boolean_group(g.id)
                        your_grp = view.env.ref('account.group_account_invoice')
                        if g == group_no_one or g == your_grp:
                            # make the group_no_one invisible in the form view
                            xml2.append(E.field(name=field_name, invisible="1", **attrs))
                        else:
                            xml2.append(E.field(name=field_name, **attrs))

            xml2.append({'class': "o_label_nowrap"})
            xml = E.field(E.group(*(xml1), col="2"), E.group(*(xml2), col="4"), name="groups_id", position="replace")
            xml.addprevious(etree.Comment("GENERATED AUTOMATICALLY BY GROUPS"))
            xml_content = etree.tostring(xml, pretty_print=True, encoding="unicode")
            if not view.check_access_rights('write',  raise_exception=False):
                # erp manager has the rights to update groups/users but not
                # to modify ir.ui.view
                if self.env.user.has_group('base.group_erp_manager'):
                    view = view.sudo()

            new_context = dict(view._context)
            new_context.pop('install_mode_data', None)  # don't set arch_fs for this computed view
            new_context['lang'] = None
            view.with_context(new_context).write({'arch': xml_content})
