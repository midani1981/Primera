#from odoo import api, fields, models, _


#class WooCommerceRegisterPayment(models.TransientModel):
#    _inherit = 'account.payment.register'

#    @api.depends('can_edit_wizard', 'company_id')
#    def _compute_journal_id(self):
#        sale_order = self._get_active_sale_order()
#        # print('sssssssssssssssssssssssssssssssssss')
#        print(sale_order.id)
#        journal_id = sale_order[0]._get_journal_id()
#        for wizard in self:
#            if wizard.can_edit_wizard:
#                batch = wizard._get_batches()[0]
#                wizard.journal_id = journal_id
#            else:
#                wizard.journal_id = journal_id

#    def _get_active_sale_order(self):
#        # active_ids = self._context.get('active_ids')
#        # sale_order = self.env['sale.order'].browse(active_ids)
#        all_ids = self._context.get('active_orders')
#        sale_order = self.env['sale.order'].browse(all_ids)
#        return sale_order
