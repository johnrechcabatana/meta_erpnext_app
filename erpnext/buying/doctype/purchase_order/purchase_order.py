# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe.utils import cstr, flt
from frappe import msgprint, _, throw
from frappe.model.mapper import get_mapped_doc
from erpnext.controllers.buying_controller import BuyingController
from erpnext.stock.doctype.item.item import get_last_purchase_details
from erpnext.stock.stock_balance import update_bin_qty, get_ordered_qty
from frappe.desk.notifications import clear_doctype_notifications


form_grid_templates = {
	"items": "templates/form_grid/item_grid.html"
}

class PurchaseOrder(BuyingController):
	def __init__(self, arg1, arg2=None):
		super(PurchaseOrder, self).__init__(arg1, arg2)
		self.status_updater = [{
			'source_dt': 'Purchase Order Item',
			'target_dt': 'Material Request Item',
			'join_field': 'prevdoc_detail_docname',
			'target_field': 'ordered_qty',
			'target_parent_dt': 'Material Request',
			'target_parent_field': 'per_ordered',
			'target_ref_field': 'qty',
			'source_field': 'stock_qty',
			'percent_join_field': 'prevdoc_docname',
			'overflow_type': 'order'
		}]

	def validate(self):
		super(PurchaseOrder, self).validate()

		self.set_status()
		pc_obj = frappe.get_doc('Purchase Common')
		pc_obj.validate_for_items(self)
		self.check_for_closed_status(pc_obj)

		self.validate_uom_is_integer("uom", "qty")
		self.validate_uom_is_integer("stock_uom", ["qty", "required_qty"])

		self.validate_with_previous_doc()
		self.validate_for_subcontracting()
		self.validate_minimum_order_qty()
		self.create_raw_materials_supplied("supplied_items")
		self.set_received_qty_for_drop_ship_items()

	def validate_with_previous_doc(self):
		super(PurchaseOrder, self).validate_with_previous_doc({
			"Supplier Quotation": {
				"ref_dn_field": "supplier_quotation",
				"compare_fields": [["supplier", "="], ["company", "="], ["currency", "="]],
			},
			"Supplier Quotation Item": {
				"ref_dn_field": "supplier_quotation_item",
				"compare_fields": [["rate", "="], ["project", "="], ["item_code", "="]],
				"is_child_table": True
			}
		})

	def validate_minimum_order_qty(self):
		items = list(set([d.item_code for d in self.get("items")]))

		itemwise_min_order_qty = frappe._dict(frappe.db.sql("""select name, min_order_qty
			from tabItem where name in ({0})""".format(", ".join(["%s"] * len(items))), items))

		itemwise_qty = frappe._dict()
		for d in self.get("items"):
			itemwise_qty.setdefault(d.item_code, 0)
			itemwise_qty[d.item_code] += flt(d.stock_qty)

		for item_code, qty in itemwise_qty.items():
			if flt(qty) < flt(itemwise_min_order_qty.get(item_code)):
				frappe.throw(_("Item {0}: Ordered qty {1} cannot be less than minimum order qty {2} (defined in Item).").format(item_code,
					qty, itemwise_min_order_qty.get(item_code)))

	def get_schedule_dates(self):
		for d in self.get('items'):
			if d.prevdoc_detail_docname and not d.schedule_date:
				d.schedule_date = frappe.db.get_value("Material Request Item",
						d.prevdoc_detail_docname, "schedule_date")


	def get_last_purchase_rate(self):
		"""get last purchase rates for all items"""

		conversion_rate = flt(self.get('conversion_rate')) or 1.0

		for d in self.get("items"):
			if d.item_code:
				last_purchase_details = get_last_purchase_details(d.item_code, self.name)

				if last_purchase_details:
					d.base_price_list_rate = (last_purchase_details['base_price_list_rate'] *
						(flt(d.conversion_factor) or 1.0))
					d.discount_percentage = last_purchase_details['discount_percentage']
					d.base_rate = last_purchase_details['base_rate'] * (flt(d.conversion_factor) or 1.0)
					d.price_list_rate = d.base_price_list_rate / conversion_rate
					d.rate = d.base_rate / conversion_rate
				else:
					# if no last purchase found, reset all values to 0
					for field in ("base_price_list_rate", "base_rate",
						"price_list_rate", "rate", "discount_percentage"):
							d.set(field, 0)

					item_last_purchase_rate = frappe.db.get_value("Item", d.item_code, "last_purchase_rate")
					if item_last_purchase_rate:
						d.base_price_list_rate = d.base_rate = d.price_list_rate \
							= d.rate = item_last_purchase_rate

	# Check for Closed status
	def check_for_closed_status(self, pc_obj):
		check_list =[]
		for d in self.get('items'):
			if d.meta.get_field('prevdoc_docname') and d.prevdoc_docname and d.prevdoc_docname not in check_list:
				check_list.append(d.prevdoc_docname)
				pc_obj.check_for_closed_status( d.prevdoc_doctype, d.prevdoc_docname)

	def update_requested_qty(self):
		material_request_map = {}
		for d in self.get("items"):
			if d.prevdoc_doctype and d.prevdoc_doctype == "Material Request" and d.prevdoc_detail_docname:
				material_request_map.setdefault(d.prevdoc_docname, []).append(d.prevdoc_detail_docname)

		for mr, mr_item_rows in material_request_map.items():
			if mr and mr_item_rows:
				mr_obj = frappe.get_doc("Material Request", mr)

				if mr_obj.status in ["Stopped", "Cancelled"]:
					frappe.throw(_("Material Request {0} is cancelled or stopped").format(mr), frappe.InvalidStatusError)

				mr_obj.update_requested_qty(mr_item_rows)

	def update_ordered_qty(self, po_item_rows=None):
		"""update requested qty (before ordered_qty is updated)"""
		item_wh_list = []
		for d in self.get("items"):
			if (not po_item_rows or d.name in po_item_rows) \
				and [d.item_code, d.warehouse] not in item_wh_list \
				and frappe.db.get_value("Item", d.item_code, "is_stock_item") \
				and d.warehouse and not d.delivered_by_supplier:
					item_wh_list.append([d.item_code, d.warehouse])
		for item_code, warehouse in item_wh_list:
			update_bin_qty(item_code, warehouse, {
				"ordered_qty": get_ordered_qty(item_code, warehouse)
			})

	def check_modified_date(self):
		mod_db = frappe.db.sql("select modified from `tabPurchase Order` where name = %s",
			self.name)
		date_diff = frappe.db.sql("select TIMEDIFF('%s', '%s')" % ( mod_db[0][0],cstr(self.modified)))

		if date_diff and date_diff[0][0]:
			msgprint(_("{0} {1} has been modified. Please refresh.").format(self.doctype, self.name),
				raise_exception=True)

	def update_status(self, status):
		self.check_modified_date()
		self.set_status(update=True, status=status)
		self.update_requested_qty()
		self.update_ordered_qty()
		self.notify_update()
		clear_doctype_notifications(self)

	def on_submit(self):
		if self.is_against_so():
			self.update_status_updater()

		purchase_controller = frappe.get_doc("Purchase Common")

		self.update_prevdoc_status()
		self.update_requested_qty()
		self.update_ordered_qty()

		frappe.get_doc('Authorization Control').validate_approving_authority(self.doctype,
			self.company, self.base_grand_total)

		purchase_controller.update_last_purchase_rate(self, is_submit = 1)

	def on_cancel(self):
		if self.is_against_so():
			self.update_status_updater()

		if self.has_drop_ship_item():
			self.update_delivered_qty_in_sales_order()

		pc_obj = frappe.get_doc('Purchase Common')
		self.check_for_closed_status(pc_obj)

		# Check if Purchase Receipt has been submitted against current Purchase Order
		pc_obj.check_docstatus(check = 'Next', doctype = 'Purchase Receipt', docname = self.name, detail_doctype = 'Purchase Receipt Item')

		# Check if Purchase Invoice has been submitted against current Purchase Order
		submitted = frappe.db.sql_list("""select t1.name
			from `tabPurchase Invoice` t1,`tabPurchase Invoice Item` t2
			where t1.name = t2.parent and t2.purchase_order = %s and t1.docstatus = 1""",
			self.name)
		if submitted:
			throw(_("Purchase Invoice {0} is already submitted").format(", ".join(submitted)))

		frappe.db.set(self,'status','Cancelled')

		self.update_prevdoc_status()

		# Must be called after updating ordered qty in Material Request
		self.update_requested_qty()
		self.update_ordered_qty()

		pc_obj.update_last_purchase_rate(self, is_submit = 0)

	def on_update(self):
		pass

	def update_status_updater(self):
		self.status_updater[0].update({
			"target_parent_dt": "Sales Order",
			"target_dt": "Sales Order Item",
			'target_field': 'ordered_qty',
			"target_parent_field": ''
		})

	def update_delivered_qty_in_sales_order(self):
		"""Update delivered qty in Sales Order for drop ship"""
		sales_orders_to_update = []
		for item in self.items:
			if item.prevdoc_doctype == "Sales Order" and item.delivered_by_supplier == 1:
				if item.prevdoc_docname not in sales_orders_to_update:
					sales_orders_to_update.append(item.prevdoc_docname)

		for so_name in sales_orders_to_update:
			so = frappe.get_doc("Sales Order", so_name)
			so.update_delivery_status()
			so.set_status(update=True)
			so.notify_update()

	def has_drop_ship_item(self):
		return any([d.delivered_by_supplier for d in self.items])

	def is_against_so(self):
		return any([d.prevdoc_doctype for d in self.items if d.prevdoc_doctype=="Sales Order"])

	def set_received_qty_for_drop_ship_items(self):
		for item in self.items:
			if item.delivered_by_supplier == 1:
				item.received_qty = item.qty

@frappe.whitelist()
def close_or_unclose_purchase_orders(names, status):
	if not frappe.has_permission("Purchase Order", "write"):
		frappe.throw(_("Not permitted"), frappe.PermissionError)

	names = json.loads(names)
	for name in names:
		po = frappe.get_doc("Purchase Order", name)
		if po.docstatus == 1:
			if status == "Closed":
				if po.status not in ( "Cancelled", "Closed") and (po.per_received < 100 or po.per_billed < 100):
					po.update_status(status)
			else:
				if po.status == "Closed":
					po.update_status("Draft")

	frappe.local.message_log = []

def set_missing_values(source, target):
	target.ignore_pricing_rule = 1
	target.run_method("set_missing_values")
	target.run_method("calculate_taxes_and_totals")

@frappe.whitelist()
def make_purchase_receipt(source_name, target_doc=None):
	def update_item(obj, target, source_parent):
		target.qty = flt(obj.qty) - flt(obj.received_qty)
		target.stock_qty = (flt(obj.qty) - flt(obj.received_qty)) * flt(obj.conversion_factor)
		target.amount = (flt(obj.qty) - flt(obj.received_qty)) * flt(obj.rate)
		target.base_amount = (flt(obj.qty) - flt(obj.received_qty)) * \
			flt(obj.rate) * flt(source_parent.conversion_rate)

	doc = get_mapped_doc("Purchase Order", source_name,	{
		"Purchase Order": {
			"doctype": "Purchase Receipt",
			"validation": {
				"docstatus": ["=", 1],
			}
		},
		"Purchase Order Item": {
			"doctype": "Purchase Receipt Item",
			"field_map": {
				"name": "prevdoc_detail_docname",
				"parent": "prevdoc_docname",
				"parenttype": "prevdoc_doctype",
			},
			"postprocess": update_item,
			"condition": lambda doc: abs(doc.received_qty) < abs(doc.qty) and doc.delivered_by_supplier!=1
		},
		"Purchase Taxes and Charges": {
			"doctype": "Purchase Taxes and Charges",
			"add_if_empty": True
		}
	}, target_doc, set_missing_values)

	return doc

@frappe.whitelist()
def make_purchase_invoice(source_name, target_doc=None):
	def postprocess(source, target):
		set_missing_values(source, target)
		#Get the advance paid Journal Entries in Purchase Invoice Advance
		target.get_advances()

	def update_item(obj, target, source_parent):
		target.amount = flt(obj.amount) - flt(obj.billed_amt)
		target.base_amount = target.amount * flt(source_parent.conversion_rate)
		target.qty = target.amount / flt(obj.rate) if (flt(obj.rate) and flt(obj.billed_amt)) else flt(obj.qty)

	doc = get_mapped_doc("Purchase Order", source_name,	{
		"Purchase Order": {
			"doctype": "Purchase Invoice",
			"validation": {
				"docstatus": ["=", 1],
			}
		},
		"Purchase Order Item": {
			"doctype": "Purchase Invoice Item",
			"field_map": {
				"name": "po_detail",
				"parent": "purchase_order",
			},
			"postprocess": update_item,
			"condition": lambda doc: (doc.base_amount==0 or abs(doc.billed_amt) < abs(doc.amount))
		},
		"Purchase Taxes and Charges": {
			"doctype": "Purchase Taxes and Charges",
			"add_if_empty": True
		}
	}, target_doc, postprocess)

	return doc

@frappe.whitelist()
def make_stock_entry(purchase_order, item_code):
	purchase_order = frappe.get_doc("Purchase Order", purchase_order)

	stock_entry = frappe.new_doc("Stock Entry")
	stock_entry.purpose = "Subcontract"
	stock_entry.purchase_order = purchase_order.name
	stock_entry.supplier = purchase_order.supplier
	stock_entry.supplier_name = purchase_order.supplier_name
	stock_entry.supplier_address = purchase_order.address_display
	stock_entry.company = purchase_order.company
	stock_entry.from_bom = 1
	po_item = [d for d in purchase_order.items if d.item_code == item_code][0]
	stock_entry.fg_completed_qty = po_item.qty
	stock_entry.bom_no = po_item.bom
	stock_entry.get_items()
	return stock_entry.as_dict()

@frappe.whitelist()
def update_status(status, name):
	po = frappe.get_doc("Purchase Order", name)
	po.update_status(status)
	po.update_delivered_qty_in_sales_order()

@frappe.whitelist()
def get_user_by_role(doctype, txt, searchfield, start, page_len, filters):
    sql = """SELECT u.name, u.first_name, u.last_name
              FROM tabUser AS u
              INNER JOIN tabUserRole AS ur ON ur.parent = u.`name`
              WHERE ur.role LIKE '{0}'
              AND u.enabled = 1""".format(filters.get('role'))
    users = frappe.db.sql(sql)
    if not users or len(users) < 1:
        frappe.msgprint(_("Please add at least one user having role {0}").format(filters.get('role')))
    return users

def get_sales_person_by_user(filters):
    sql = """SELECT u.name
              FROM tabUser AS u
              INNER JOIN tabUserRole AS ur ON ur.parent = u.`name`
              WHERE ur.role LIKE '{0}'
              AND u.name = '{1}'
              AND u.enabled = 1""".format(filters.get("role"), filters.get('user'))

    user = frappe.db.sql(sql, as_dict=1)
    if len(user) > 0:
        return user[0]

@frappe.whitelist()
def get_sales_person_by_role(doctype, txt, searchfield, start, page_len, filters):
    users = []
    sql = """SELECT sp.*, employee.`name`, employee.user_id FROM `tabSales Person` AS sp
              INNER JOIN tabEmployee AS employee ON employee.name = sp.employee
              WHERE employee.designation IN('Sales Person')
              AND employee.`status` = 'Active' AND employee.department IN('Sales');"""

    sales_person_list = frappe.db.sql(sql, as_dict=1)

    if len(sales_person_list) > 0:
        for sales_person in sales_person_list:
            user = get_sales_person_by_user(filters={"role": '%sales%', "user": sales_person.user_id})
            if user is not None and user.name == sales_person.user_id :
		tuple = (sales_person.sales_person_name, sales_person.name, sales_person.employee, sales_person.user_id)  
                users.append(tuple)

        return users