from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Billing"),
			"items": [
				{
					"type": "doctype",
					"name": "Sales Invoice",
					"description": _("Bills raised to Customers.")
				},
				{
					"type": "doctype",
					"name": "Purchase Invoice",
					"description": _("Bills raised by Suppliers.")
				},
				{
					"type": "doctype",
					"name": "Payment Request",
					"description": _("Payment Request")
				},
				# {
				# 	"type": "report",
				# 	"name": "Accounts Receivable",
				# 	"doctype": "Sales Invoice",
				# 	"is_query_report": True
				# },
				# {
				# 	"type": "report",
				# 	"name": "Accounts Payable",
				# 	"doctype": "Purchase Invoice",
				# 	"is_query_report": True
				# },
			]

		},
		{
			"label": _("Company and Accounts"),
			"items": [
				{
					"type": "doctype",
					"name": "Company",
					"description": _("Company (not Customer or Supplier) master.")
				},
				# {
				# 	"type": "doctype",
				# 	"name": "Journal Entry",
				# 	"description": _("Accounting journal entries.")
				# },
				# {
				# 	"type": "page",
				# 	"name": "Accounts Browser",
				# 	"icon": "icon-sitemap",
				# 	"label": _("Chart of Accounts"),
				# 	"route": "Accounts Browser/Account",
				# 	"description": _("Tree of financial accounts."),
				# 	"doctype": "Account",
				# },
				# {
				# 	"type": "report",
				# 	"name":"General Ledger",
				# 	"doctype": "GL Entry",
				# 	"is_query_report": True,
				# },
			]
		},
		{
			"label": _("Masters"),
			"items": [
				{
					"type": "doctype",
					"name": "Customer",
					"description": _("Customer database.")
				},
				{
					"type": "doctype",
					"name": "Supplier",
					"description": _("Supplier database.")
				},
				{
					"type": "doctype",
					"name": "Item",
				},
			]
		},
		# {
		# 	"label": _("Accounting Statements"),
		# 	"items": [
		# 		{
		# 			"type": "report",
		# 			"name": "Trial Balance",
		# 			"doctype": "GL Entry",
		# 			"is_query_report": True,
		# 		},
		# 		{
		# 			"type": "report",
		# 			"name": "Balance Sheet",
		# 			"doctype": "GL Entry",
		# 			"is_query_report": True
		# 		},
		# 		{
		# 			"type": "report",
		# 			"name": "Cash Flow",
		# 			"doctype": "GL Entry",
		# 			"is_query_report": True
		# 		},
		# 		{
		# 			"type": "report",
		# 			"name": "Profit and Loss Statement",
		# 			"doctype": "GL Entry",
		# 			"is_query_report": True
		# 		},
		# 	]
		# },
		# {
		# 	"label": _("Banking and Payments"),
		# 	"items": [
		# 		{
		# 			"type": "doctype",
		# 			"name": "Payment Tool",
		# 			"description": _("Create Payment Entries against Orders or Invoices.")
		# 		},
		# 		{
		# 			"type": "doctype",
		# 			"label": _("Update Bank Transaction Dates"),
		# 			"name": "Bank Reconciliation",
		# 			"description": _("Update bank payment dates with journals.")
		# 		},
		# 		{
		# 			"type": "doctype",
		# 			"label": _("Match Payments with Invoices"),
		# 			"name": "Payment Reconciliation",
		# 			"description": _("Match non-linked Invoices and Payments.")
		# 		},
		# 		{
		# 			"type": "report",
		# 			"name": "Bank Reconciliation Statement",
		# 			"is_query_report": True,
		# 			"doctype": "Journal Entry"
		# 		},
		# 		{
		# 			"type": "report",
		# 			"name": "Bank Clearance Summary",
		# 			"is_query_report": True,
		# 			"doctype": "Journal Entry"
		# 		},
		# 	]
		# },
		{
			"label": _("Taxes"),
			"items": [
				# {
				# 	"type": "doctype",
				# 	"name": "Sales Taxes and Charges Template",
				# 	"description": _("Tax template for selling transactions.")
				# },
				# {
				# 	"type": "doctype",
				# 	"name": "Purchase Taxes and Charges Template",
				# 	"description": _("Tax template for buying transactions.")
				# },
				# {
				# 	"type": "doctype",
				# 	"name": "Tax Rule",
				# 	"description": _("Tax Rule for transactions.")
				# },
				{
					"type": "report",
					"name": "Sales Register",
					"doctype": "Sales Invoice",
					"is_query_report": True
				},
				{
					"type": "report",
					"name": "Purchase Register",
					"doctype": "Purchase Invoice",
					"is_query_report": True
				},
			]
		},
		# {
		# 	"label": _("Budget and Cost Center"),
		# 	"items": [
		# 		{
		# 			"type": "page",
		# 			"name": "Accounts Browser",
		# 			"icon": "icon-sitemap",
		# 			"label": _("Chart of Cost Centers"),
		# 			"route": "Accounts Browser/Cost Center",
		# 			"description": _("Tree of financial Cost Centers."),
		# 			"doctype": "Cost Center",
		# 		},
		# 		{
		# 			"type": "report",
		# 			"name": "Budget Variance Report",
		# 			"is_query_report": True,
		# 			"doctype": "Cost Center"
		# 		},
		# 		{
		# 			"type":"doctype",
		# 			"name": "Monthly Distribution",
		# 			"description": _("Seasonality for setting budgets, targets etc.")
		# 		},
		# 	]
		# },
		# {
		# 	"label": _("Tools"),
		# 	"items": [
		# 		{
		# 			"type": "doctype",
		# 			"name": "Period Closing Voucher",
		# 			"description": _("Close Balance Sheet and book Profit or Loss.")
		# 		},
		# 	]
		# },
		{
			"label": _("Setup"),
			"icon": "icon-cog",
			"items": [
				# {
				# 	"type": "doctype",
				# 	"name": "Accounts Settings",
				# 	"description": _("Default settings for accounting transactions.")
				# },
				{
					"type": "doctype",
					"name": "Fiscal Year",
					"description": _("Financial / accounting year.")
				},
				{
					"type": "doctype",
					"name": "Currency",
					"description": _("Enable / disable currencies.")
				},
				{
					"type": "doctype",
					"name": "Currency Exchange",
					"description": _("Currency exchange rate master.")
				},
				{
					"type": "doctype",
					"name": "Payment Gateway Account",
					"description": _("Setup Gateway accounts.")
				},
				# {
				# 	"type": "doctype",
				# 	"name": "POS Profile",
				# 	"label": _("Point-of-Sale Profile"),
				# 	"description": _("Rules to calculate shipping amount for a sale")
				# },
				{
					"type": "doctype",
					"name":"Terms and Conditions",
					"label": _("Terms and Conditions Template"),
					"description": _("Template of terms or contract.")
				},
				{
					"type": "doctype",
					"name":"Mode of Payment",
					"description": _("e.g. Bank, Cash, Credit Card")
				},
				{
					"type": "doctype",
					"name":"C-Form",
					"description": _("C-Form records"),
					"country": "India"
				}
			]
		},
		{
			"label": _("To Bill"),
			"items": [
				{
					"type": "report",
					"name": "Ordered Items To Be Billed",
					"is_query_report": True,
					"doctype": "Sales Invoice"
				},
				{
					"type": "report",
					"name": "Delivered Items To Be Billed",
					"is_query_report": True,
					"doctype": "Sales Invoice"
				},
				{
					"type": "report",
					"name": "Purchase Order Items To Be Billed",
					"is_query_report": True,
					"doctype": "Purchase Invoice"
				},
				{
					"type": "report",
					"name": "Received Items To Be Billed",
					"is_query_report": True,
					"doctype": "Purchase Invoice"
				},
			]

		},
		# {
		# 	"label": _("Analytics"),
		# 	"items": [
		# 		{
		# 			"type": "page",
		# 			"name": "financial-analytics",
		# 			"label": _("Financial Analytics"),
		# 			"icon": "icon-bar-chart",
		# 		},
		# 		{
		# 			"type": "report",
		# 			"name": "Gross Profit",
		# 			"doctype": "Sales Invoice",
		# 			"is_query_report": True
		# 		},
		# 		{
		# 			"type": "report",
		# 			"name": "Purchase Invoice Trends",
		# 			"is_query_report": True,
		# 			"doctype": "Purchase Invoice"
		# 		},
		# 		{
		# 			"type": "report",
		# 			"name": "Sales Invoice Trends",
		# 			"is_query_report": True,
		# 			"doctype": "Sales Invoice"
		# 		},
		# 	]
		# },
		# {
		# 	"label": _("Other Reports"),
		# 	"icon": "icon-table",
		# 	"items": [
		# 		{
		# 			"type": "report",
		# 			"name": "Trial Balance for Party",
		# 			"doctype": "GL Entry",
		# 			"is_query_report": True,
		# 		},
		# 		{
		# 			"type": "report",
		# 			"name": "Payment Period Based On Invoice Date",
		# 			"is_query_report": True,
		# 			"doctype": "Journal Entry"
		# 		},
		# 		{
		# 			"type": "report",
		# 			"name": "Sales Partners Commission",
		# 			"is_query_report": True,
		# 			"doctype": "Sales Invoice"
		# 		},
		# 		{
		# 			"type": "report",
		# 			"name": "Item-wise Sales Register",
		# 			"is_query_report": True,
		# 			"doctype": "Sales Invoice"
		# 		},
		# 		{
		# 			"type": "report",
		# 			"name": "Item-wise Purchase Register",
		# 			"is_query_report": True,
		# 			"doctype": "Purchase Invoice"
		# 		},
		# 		{
		# 			"type": "report",
		# 			"name": "Accounts Receivable Summary",
		# 			"doctype": "Sales Invoice",
		# 			"is_query_report": True
		# 		},
		# 		{
		# 			"type": "report",
		# 			"name": "Accounts Payable Summary",
		# 			"doctype": "Purchase Invoice",
		# 			"is_query_report": True
		# 		},
		# 		{
		# 			"type": "report",
		# 			"is_query_report": True,
		# 			"name": "Customer Credit Balance",
		# 			"doctype": "Customer"
		# 		},
		# 	]
		# },
		# {
		# 	"label": _("Help"),
		# 	"icon": "icon-facetime-video",
		# 	"items": [
		# 		{
		# 			"type": "help",
		# 			"label": _("Chart of Accounts"),
		# 			"youtube_id": "DyR-DST-PyA"
		# 		},
		# 		{
		# 			"type": "help",
		# 			"label": _("Opening Accounting Balance"),
		# 			"youtube_id": "kdgM20Q-q68"
		# 		},
		# 		{
		# 			"type": "help",
		# 			"label": _("Setting up Taxes"),
		# 			"youtube_id": "nQ1zZdPgdaQ"
		# 		}
		# 	]
		# }
	]
