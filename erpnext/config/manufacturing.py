from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Production"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "Production Order",
					"description": _("Orders released for production."),
				},
				{
					"type": "doctype",
					"name": "Production Planning Tool",
					"description": _("Generate Material Requests (MRP) and Production Orders."),
				},
				{
					"type": "doctype",
					"name": "Stock Entry",
				},
				{
					"type": "doctype",
					"name": "Time Log",
					"description": _("Time Logs for manufacturing."),
				},

			]
		},
		{
			"label": _("Bill of Materials"),
			"items": [
				{
					"type": "doctype",
					"name": "BOM",
					"description": _("Bill of Materials (BOM)"),
					"label": _("Bill of Materials")
				},
				{
					"type": "page",
					"name": "bom-browser",
					"icon": "icon-sitemap",
					"label": _("BOM Browser"),
					"description": _("Tree of Bill of Materials"),
					"doctype": "BOM"
				},
				{
					"type": "doctype",
					"name": "Item",
					"description": _("All Products or Services."),
				},
				{
					"type": "doctype",
					"name": "Workstation",
					"description": _("Where manufacturing operations are carried."),
				},
				{
					"type": "doctype",
					"name": "Operation",
					"description": _("Details of the operations carried out."),
				},

			]
		},
		{
			"label": _("Tools"),
			"icon": "icon-wrench",
			"items": [
				{
					"type": "doctype",
					"name": "BOM Replace Tool",
					"description": _("Replace Item / BOM in all BOMs"),
				},
			]
		},
		{
			"label": _("Setup"),
			"items": [
				{
					"type": "doctype",
					"name": "Manufacturing Settings",
					"description": _("Global settings for all manufacturing processes."),
				}
			]
		},
		# {
		# 	"label": _("Reports"),
		# 	"icon": "icon-list",
		# 	"items": [
		# 		{
		# 			"type": "report",
		# 			"is_query_report": True,
		# 			"name": "Open Production Orders",
		# 			"doctype": "Production Order"
		# 		},
		# 		{
		# 			"type": "report",
		# 			"is_query_report": True,
		# 			"name": "Production Orders in Progress",
		# 			"doctype": "Production Order"
		# 		},
		# 		{
		# 			"type": "report",
		# 			"is_query_report": True,
		# 			"name": "Issued Items Against Production Order",
		# 			"doctype": "Production Order"
		# 		},
		# 		{
		# 			"type": "report",
		# 			"is_query_report": True,
		# 			"name": "Completed Production Orders",
		# 			"doctype": "Production Order"
		# 		},
		# 		{
		# 			"type": "report",
		# 			"is_query_report": True,
		# 			"name": "BOM Search",
		# 			"doctype": "BOM"
		# 		},
		# 	]
		# },
		# {
		# 	"label": _("Help"),
		# 	"icon": "icon-facetime-video",
		# 	"items": [
		# 		{
		# 			"type": "help",
		# 			"label": _("Bill of Materials"),
		# 			"youtube_id": "hDV0c1OeWLo"
		# 		},
		# 		{
		# 			"type": "help",
		# 			"label": _("Production Planning Tool"),
		# 			"youtube_id": "CzatSl4zJ2Y"
		# 		},
		# 		{
		# 			"type": "help",
		# 			"label": _("Production Order"),
		# 			"youtube_id": "ZotgLyp2YFY"
		# 		},
		# 	]
		# }
	]
