# -*- coding: utf-8 -*-
###################################################################################
#
#    ALTANMYA - TECHNOLOGY SOLUTIONS
#    Copyright (C) 2022-TODAY ALTANMYA - TECHNOLOGY SOLUTIONS Part of ALTANMYA GROUP.
#    ALTANMYA WooCommerce Automated Workflow.
#    Author: ALTANMYA for Technology(<https://tech.altanmya.net>)
#
#    This program is Licensed software: you can not modify
#   #
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################

{
    'name': 'ALTANMYA WooCommerce Automated Workflow 12.0',
    'version': '11.0',
    'category': 'Sales/WooCommerce',
    'summary': 'ALTANMYA WooCommerce Automated Workflow',
    'description': "Process Confirmed Sales Order collected from WooCommerce, Create Invoice and Confirm it, Register Payment on Specified Journal based on information collected from Sales Order and Create Automated Cash Statement then post it, conduct Reconciliation and finally validate Cash statement",
    'author': 'ALTANMYA - TECHNOLOGY SOLUTIONS',
    'company': 'ALTANMYA - TECHNOLOGY SOLUTIONS Part of ALTANMYA GROUP',
    'website': "https://tech.altanmya.net",
    'depends': ['sale', 'stock', 'account', 'woo_commerce_ept'],
    'data': ['views/create_invoice_button.xml'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
