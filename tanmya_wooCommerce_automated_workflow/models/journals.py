# from odoo import models, api, fields
#
# class WooCommerceJournals(models.Model):
#     name = "woocommerce.journals"
#
#     payment_getway_id = fields.Char(string="Payment Getway ID")
#
#     journal_id = fields.Many2one(
#         comodel_name='account.journal',
#         string='Journal',
#         domain="[('type', 'in', ('bank','cash')), ('company_id', '=', company_id), ('id', '!=', journal_id)]",
#         check_company=True,
#     )
#
