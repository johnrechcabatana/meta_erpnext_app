from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Employee"),
			"items": [
				{
					"type": "doctype",
					"name": "Employee",
					"description": _("Employee records."),
				},
				# {
				# 	"type": "doctype",
				# 	"name": "Employee Attendance Tool",
				# 	"label": _("Employee Attendance Tool"),
				# 	"description":_("Mark Employee Attendance in Bulk"),
				# 	"hide_count": True
				# },
				# {
				# 	"type": "doctype",
				# 	"name": "Attendance",
				# 	"description": _("Attendance record."),
				# },
				# {
				# 	"type": "doctype",
				# 	"name": "Upload Attendance",
				# 	"description":_("Upload attendance from a .csv file"),
				# 	"hide_count": True
				# },
			]
		},
		# {
		# 	"label": _("Recruitment"),
		# 	"items": [
		# 		{
		# 			"type": "doctype",
		# 			"name": "Job Applicant",
		# 			"description": _("Applicant for a Job."),
		# 		},
		# 		{
		# 			"type": "doctype",
		# 			"name": "Job Opening",
		# 			"description": _("Opening for a Job."),
		# 		},
		# 		{
		# 			"type": "doctype",
		# 			"name": "Offer Letter",
		# 			"description": _("Offer candidate a Job."),
		# 		},
		# 	]
		# },
		# {
		# 	"label": _("Leaves and Holiday"),
		# 	"items": [
		# 		{
		# 			"type": "doctype",
		# 			"name": "Leave Application",
		# 			"description": _("Applications for leave."),
		# 		},
		# 		{
		# 			"type": "doctype",
		# 			"name":"Leave Type",
		# 			"description": _("Type of leaves like casual, sick etc."),
		# 		},
		# 		{
		# 			"type": "doctype",
		# 			"name": "Holiday List",
		# 			"description": _("Holiday master.")
		# 		},
		# 		{
		# 			"type": "doctype",
		# 			"name": "Leave Allocation",
		# 			"description": _("Allocate leaves for a period.")
		# 		},
		# 		{
		# 			"type": "doctype",
		# 			"name": "Leave Control Panel",
		# 			"label": _("Leave Allocation Tool"),
		# 			"description":_("Allocate leaves for the year."),
		# 			"hide_count": True
		# 		},
		# 		{
		# 			"type": "doctype",
		# 			"name": "Leave Block List",
		# 			"description": _("Block leave applications by department.")
		# 		},

		# 	]
		# },
		# {
		# 	"label": _("Payroll"),
		# 	"items": [
		# 		{
		# 			"type": "doctype",
		# 			"name": "Salary Slip",
		# 			"description": _("Monthly salary statement."),
		# 		},
		# 		{
		# 			"type": "doctype",
		# 			"name": "Process Payroll",
		# 			"label": _("Process Payroll"),
		# 			"description":_("Generate Salary Slips"),
		# 			"hide_count": True
		# 		},
		# 		{
		# 			"type": "doctype",
		# 			"name": "Salary Structure",
		# 			"description": _("Salary template master.")
		# 		},
		# 		{
		# 			"type": "doctype",
		# 			"name": "Earning Type",
		# 			"description": _("Salary components.")
		# 		},
		# 		{
		# 			"type": "doctype",
		# 			"name": "Deduction Type",
		# 			"description": _("Tax and other salary deductions.")
		# 		},

		# 	]
		# },
		# {
		# 	"label": _("Expense Claims"),
		# 	"items": [
		# 		{
		# 			"type": "doctype",
		# 			"name": "Expense Claim",
		# 			"description": _("Claims for company expense."),
		# 		},
		# 		{
		# 			"type": "doctype",
		# 			"name": "Expense Claim Type",
		# 			"description": _("Types of Expense Claim.")
		# 		},
		# 	]
		# },
		# {
		# 	"label": _("Appraisals"),
		# 	"items": [
		# 		{
		# 			"type": "doctype",
		# 			"name": "Appraisal",
		# 			"description": _("Performance appraisal."),
		# 		},
		# 		{
		# 			"type": "doctype",
		# 			"name": "Appraisal Template",
		# 			"description": _("Template for performance appraisals.")
		# 		},
		# 	]
		# },

		{
			"label": _("Tools"),
			"icon": "icon-wrench",
			"items": [

			]
		},
		{
			"label": _("Setup"),
			"icon": "icon-cog",
			"items": [
				# {
				# 	"type": "doctype",
				# 	"name": "HR Settings",
				# 	"description": _("Settings for HR Module")
				# },
				# {
				# 	"type": "doctype",
				# 	"name": "Employment Type",
				# 	"description": _("Types of employment (permanent, contract, intern etc.).")
				# },
				{
					"type": "doctype",
					"name": "Branch",
					"description": _("Organization branch master.")
				},
				{
					"type": "doctype",
					"name": "Department",
					"description": _("Organization unit (department) master.")
				},
				{
					"type": "doctype",
					"name": "Designation",
					"description": _("Employee designation (e.g. CEO, Director etc.).")
				},
			]
		},
		# {
		# 	"label": _("Reports"),
		# 	"icon": "icon-list",
		# 	"items": [
		# 		{
		# 			"type": "report",
		# 			"is_query_report": True,
		# 			"name": "Employee Leave Balance",
		# 			"doctype": "Leave Application"
		# 		},
		# 		{
		# 			"type": "report",
		# 			"is_query_report": True,
		# 			"name": "Employee Birthday",
		# 			"doctype": "Employee"
		# 		},
		# 		{
		# 			"type": "report",
		# 			"is_query_report": True,
		# 			"name": "Employee Holiday Attendance",
		# 			"doctype": "Employee"
		# 		},
		# 		{
		# 			"type": "report",
		# 			"name": "Employee Information",
		# 			"doctype": "Employee"
		# 		},
		# 		{
		# 			"type": "report",
		# 			"is_query_report": True,
		# 			"name": "Monthly Salary Register",
		# 			"doctype": "Salary Slip"
		# 		},
		# 		{
		# 			"type": "report",
		# 			"is_query_report": True,
		# 			"name": "Monthly Attendance Sheet",
		# 			"doctype": "Attendance"
		# 		},

		# 	]
		# },
		# {
		# 	"label": _("Help"),
		# 	"icon": "icon-facetime-video",
		# 	"items": [
		# 		{
		# 			"type": "help",
		# 			"label": _("Setting up Employees"),
		# 			"youtube_id": "USfIUdZlUhw"
		# 		},
		# 		{
		# 			"type": "help",
		# 			"label": _("Leave Management"),
		# 			"youtube_id": "fc0p_AXebc8"
		# 		},
		# 		{
		# 			"type": "help",
		# 			"label": _("Expense Claims"),
		# 			"youtube_id": "5SZHJF--ZFY"
		# 		},
		# 		{
		# 			"type": "help",
		# 			"label": _("Processing Payroll"),
		# 			"youtube_id": "apgE-f25Rm0"
		# 		},
		# 	]
		# }
	]
