# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Altanmya WooCommerce Automated Workflow 13.0',
    'version': '13.0',
    'category': 'Sales/WooCommerce',
    'summary': 'Edit Taxable Values',
    'website': 'https://www.odoo.com/app/sales',
    'depends': ['sale', 'stock', 'account','woo_commerce_ept',],
    'data': ['views/create_invoice_button.xml'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
