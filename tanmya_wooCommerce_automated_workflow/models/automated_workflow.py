from datetime import datetime, timedelta
import pytz
from odoo import api, fields, models, _

class SaleOrderAutomated(models.Model):
    _inherit = ["sale.order"]

    woo_status = 'completed'
    
    puredate =fields.Date(string="Invoice date",compute="_get_inv_date",store=True)
    @api.depends('date_order')
    def _get_inv_date(self):
        ret = None
        if self.date_order:
            rec_date_order2 = self.date_order + timedelta(hours=3)
            rec_date_order_invoice = datetime(rec_date_order2.year, rec_date_order2.month, rec_date_order2.day)
            ret= rec_date_order_invoice

        self.puredate =ret

    # def _get_journal_name(self):
    #     if self.payment_getway_id == 'Apple Pay':
    #         return 'Check Out'

    def _get_journal_id(self):
        # journal_id = self.env['account.journal'].search([('type', '=', 'bank')]).id

        print(self.payment_gateway_id)
        journal_id = self.payment_gateway_id.journal_id.id
        return journal_id

    def create_invoice_button(self):
        try:
            self._cr.autocommit(False)
            odoobot = self.env['res.users'].browse(1)
            tt=datetime.now(pytz.timezone(odoobot.env.user.tz)).strftime('%z')
            diff_hour=int(tt[1:3])+int(tt[3:])/60
            # if tt[0:1] == '+':
            #     diff_hour=-1*diff_hour
            # print('diff_hour....................:  '+str(diff_hour))
            seq_transaction=0
            rec_date_order = datetime.strptime('01/08/2015','%d/%m/%Y').date()
            for rec1 in self.ids:
                ++seq_transaction
                rec = self.browse(rec1)
                # rec_date_order=rec.date_order+timedelta(hours=diff_hour)
                rec_date_order=rec.date_order
                # print('sale order--------------')
                # print(rec_date_order)
                rec_date_order2 = rec_date_order + timedelta(hours=3)#diff_hour
                # print('rec_date_order2--------------')
                # print(rec_date_order2)
                rec_date_order_invoice =  datetime(rec_date_order2.year , rec_date_order2.month , rec_date_order2.day )
                # print('rec_date_order_invoice--------------')
                # print(rec_date_order_invoice)
                if rec.state == 'sale' and rec.woo_status=='completed':
                    try:
                       super(SaleOrderAutomated, rec)._action_cancel()
                    except:
                        super(SaleOrderAutomated, rec).action_cancel()
                    # self.action_cancel()
                    rec.action_draft()
                    # self._change_discount_value()
                    # self.order_line = self.order_line.filtered(lambda l: not set(l.product_id.name.split(" ")) & set(['discount', 'Discount']))
                    # self.action_confirm()

                    # print('before invoice')
                    # created_inv=super(SaleOrderAutomated, self)._create_invoices(final=False)
                    rec._modify_corder()

                    try:
                        rec.saletype = False
                    except:
                        pass
                    rec.action_confirm()
                    rec.date_order=rec_date_order
                    # print(created_inv)

                    super(SaleOrderAutomated, rec)._create_invoices(final=True)
                    rec.invoice_ids.invoice_date=rec_date_order_invoice
                    rec.invoice_ids.action_post()
                    inv_name=None
                    for ii in rec.invoice_ids:
                        inv_name=ii.name
                    ctx = dict(
                        active_ids=rec.invoice_ids.ids,
                        active_orders=rec.ids,
                        active_model='account.move'
                    )
                    register_payment_wizard = self.env['account.payment.register'].with_context(ctx).create(
                        {
                            'amount': rec.invoice_ids.amount_residual,
                            'currency_id': rec.invoice_ids.currency_id.id,
                            'payment_type': 'inbound',
                            'partner_type': 'customer',
                            'payment_method_line_id': 1,
                            'payment_date':rec_date_order_invoice
                        }
                    )
                    pay_action=register_payment_wizard.action_create_payments()
                    self.create_cash_statement(inv_name,pay_action)
                    if seq_transaction %10 ==0:
                        self._cr.commit()
            self._cr.commit()

        except:
            self._cr.rollback()
        self._cr.autocommit(True)





    # def _change_discount_value(self):
    #     products_lines = []
    #     discounts_lines = []
    #
    #     for line in self.order_line:
    #         if set(line.product_id.name.split(" ")) & set(['discount', 'Discount']):
    #             discounts_lines.append(line)
    #         else:
    #             products_lines.append(line)
    #
    #     for p_line in products_lines:
    #         for d_line in discounts_lines:
    #             if p_line.name.lower() in d_line.name.lower():
    #                 percent = (d_line.price_unit * -100) / (p_line.price_unit)
    #                 p_line.write({'discount': percent})
    #                 break

    # def _modify_invoice(self,moves):
    #     for invv in moves:
    #         dic_lines={}
    #         zz=None
    #         for oneline in invv.line_ids:
    #             if oneline.product_id.default_code=='DISC' : #and  oneline.product_id.id != 41
    #                 print(oneline.name[18:oneline.name.find(']', 18)])
    #                 dic_lines[oneline.id]=(oneline.name[18:oneline.name.find(']', 18)],-1*oneline.price_subtotal)
    #                 zz=oneline.id
    #                 print(oneline.product_id.id)
    #                 break
    #                 # self.env['account.move.line'].browse(oneline.id).unlink()
    #
    #         print('----------')
    #         print(zz)
    #         invv.write({'invoice_line_ids':[3,zz,False]})



                    # oneline.unlink()
                    # dic_lines[oneline.id]=[,]

    def _modify_corder(self):
        for rec1 in self:
            dic_lines={}
            zz=None
            tt=[]

            for oneline in rec1.order_line:

                if oneline.product_id.default_code=='DISC' : #and  oneline.product_id.id != 41
                    dic_lines[oneline.name]=-1*oneline.price_subtotal

                else:
                    tt.append(oneline.id)
            for oneline in rec1.order_line:

                if oneline.product_id and "Discount for "+oneline.product_id.display_name in dic_lines:
                    # filter_dic = dict(filter(lambda item: search_key in item[0], test_dict.items()))
                    oneline.discount=dic_lines["Discount for "+oneline.product_id.display_name]*100/oneline.price_subtotal

            tt.append(False)

            # self.env['sale_order_line'].browse(zz).unlink()
            rec1.order_line=tt



                    # oneline.unlink()
                    # dic_lines[oneline.id]=[,]


    def create_cash_statement(self,invoice_name,payaction):

        # last_payment=payaction

        last_payment = self.env['account.payment'].browse(payaction['res_id'])
        # last_payment = self.env['account.payment'].search([ '&',('currency_id', '=', payaction['currency_id']),('payment_type', '=', payaction['payment_type']),('partner_type', '=', payaction['partner_type'])], order='id desc', limit=1)
        # print(payaction)
        last_journal = self.env['account.bank.statement'].search([('journal_id', '=', last_payment.journal_id.id)], order='id desc', limit=1)
        lastpaymentid=last_payment.id
        journal_id = last_payment.journal_id.id
        date = last_payment.date
        nn=last_payment.name
        partner_id = last_payment.partner_id.id
        amount = last_payment.amount
        currency_id = last_payment.currency_id.id

        starting_balance = 0.00

        if last_journal:
            starting_balance = last_journal.balance_end_real
        ending_balance = starting_balance + amount
        computed_balance = amount
        line_payment_ref = last_payment.ref
        statement = self.env['account.bank.statement'].create({
            'journal_id': journal_id,
            'date': date,
            # 'balance_start': starting_balance,
            'balance_end_real': ending_balance,
            # 'balance_end': computed_balance,
            'state': 'open',
            'line_ids': [
                (0, 0, {
                    'payment_id': lastpaymentid,
                    'payment_ref': invoice_name,
                    'partner_id': last_payment.partner_id.id,
                    'amount': amount,
                    'date': date
                })
            ]

        })

        line_date = date

        line_partner_id = partner_id
        line_amount = amount
        line_journal_id = journal_id
        line_statement_id = statement.id
        # line_move_id = last_payment.reconciled_invoice_ids.id
        line_counterpart_account_id = statement.journal_id.profit_account_id.id
        # commented by iy
        # statement_line = self.env['account.bank.statement.line'].create({
        #     'date': line_date,
        #     'payment_ref': line_payment_ref,
        #     'partner_id': line_partner_id,
        #     'amount': line_amount,
        #     'journal_id': line_journal_id,
        #     'statement_id': line_statement_id,
        #     'counterpart_account_id': line_counterpart_account_id
        # })

        # statement.line_ids = [(4, statement_line.id)]
        # end commented by iy
        statement.button_post()
        statement.action_bank_reconcile_bank_statements()
        annos=self.env['account.reconcile.model'].browse(1)
        annos._apply_rules(statement.line_ids)

        statement.button_validate_or_action()
        # statement.button_validate()

class extend_connector(models.Model):
    _inherit = ["woo.payment.gateway"]
    journal_id =fields.Many2one('account.journal',string='Journal',domain="[('type', 'in', ('bank','cash'))]")


