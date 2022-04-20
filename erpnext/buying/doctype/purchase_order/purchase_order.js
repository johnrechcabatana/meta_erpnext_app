// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.provide("erpnext.buying");

{% include 'buying/doctype/purchase_common/purchase_common.js' %};

frappe.ui.form.on("Purchase Order", {
	onload: function(frm) {
		erpnext.queries.setup_queries(frm, "Warehouse", function() {
			return erpnext.queries.warehouse(frm.doc);
		});
		cur_frm.set_query("shipping_gent", function(doc) {
			return {
				query:"erpnext.buying.doctype.purchase_order.purchase_order.get_user_by_role",
				filters:{
					role: "%agent%"
				}
			}
		});
	
		cur_frm.set_query("sales_person", "sales_rep", function(doc) {
				return {
					query:"erpnext.buying.doctype.purchase_order.purchase_order.get_sales_person_by_role",
					filters:{
						role: "%sales%"
					}
				}
			});
	}
});

erpnext.buying.PurchaseOrderController = erpnext.buying.BuyingController.extend({
	refresh: function(doc, cdt, cdn) {
		var me = this;
		this._super();
		// this.frm.dashboard.reset();
		var allow_receipt = false;
		var is_drop_ship = false;

		for (var i in cur_frm.doc.items) {
			var item = cur_frm.doc.items[i];
			if(item.delivered_by_supplier !== 1) {
				allow_receipt = true;
			}

			else {
				is_drop_ship = true
			}

			if(is_drop_ship && allow_receipt) {
				break;
			}
		}

		cur_frm.set_df_property("drop_ship", "hidden", !is_drop_ship);

		if(doc.docstatus == 1 && !in_list(["Closed", "Delivered"], doc.status)) {
			if (this.frm.has_perm("submit")) {
				if(flt(doc.per_billed, 2) < 100 || doc.per_received < 100) {
					cur_frm.add_custom_button(__('Close'), this.close_purchase_order, __("Status"));
				}
			}

			if(is_drop_ship && doc.status!="Delivered"){
				cur_frm.add_custom_button(__('Delivered'),
					 this.delivered_by_supplier, __("Status"));

				cur_frm.page.set_inner_btn_group_as_primary(__("Status"));
			}
		} else if(doc.docstatus===0) {
			cur_frm.cscript.add_from_mappers();
		}

		if(doc.docstatus == 1 && in_list(["Closed", "Delivered"], doc.status)) {
			if (this.frm.has_perm("submit")) {
				cur_frm.add_custom_button(__('Re-open'), this.unclose_purchase_order, __("Status"));
			}
		}

		if(doc.docstatus == 1 && doc.status != "Closed") {
			if(flt(doc.per_received, 2) < 100 && allow_receipt) {
				cur_frm.add_custom_button(__('Receive'), this.make_purchase_receipt, __("Make"));

				if(doc.is_subcontracted==="Yes") {
					cur_frm.add_custom_button(__('Material to Supplier'),
						function() { me.make_stock_entry(); }, __("Transfer"));
				}
			}

			if(flt(doc.per_billed, 2) < 100)
				cur_frm.add_custom_button(__('Invoice'),
					this.make_purchase_invoice, __("Make"));

			if(flt(doc.per_billed)==0 && doc.status != "Delivered") {
				cur_frm.add_custom_button(__('Payment'), cur_frm.cscript.make_bank_entry, __("Make"));
			}
			cur_frm.page.set_inner_btn_group_as_primary(__("Make"));

		}
	},

	get_items_from_open_material_requests: function() {
		frappe.model.map_current_doc({
			method: "erpnext.stock.doctype.material_request.material_request.make_purchase_order_based_on_supplier",
			source_name: this.frm.doc.supplier,
			get_query_filters: {
				docstatus: ["!=", 2],
			}
		});
	},

	make_stock_entry: function() {
		var items = $.map(cur_frm.doc.items, function(d) { return d.bom ? d.item_code : false; });
		var me = this;

		if(items.length===1) {
			me._make_stock_entry(items[0]);
			return;
		}
		frappe.prompt({fieldname:"item", options: items, fieldtype:"Select",
			label: __("Select Item for Transfer"), reqd: 1}, function(data) {
			me._make_stock_entry(data.item);
		}, __("Select Item"), __("Make"));
	},

	_make_stock_entry: function(item) {
		frappe.call({
			method:"erpnext.buying.doctype.purchase_order.purchase_order.make_stock_entry",
			args: {
				purchase_order: cur_frm.doc.name,
				item_code: item
			},
			callback: function(r) {
				var doclist = frappe.model.sync(r.message);
				frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
			}
		});
	},

	make_purchase_receipt: function() {
		frappe.model.open_mapped_doc({
			method: "erpnext.buying.doctype.purchase_order.purchase_order.make_purchase_receipt",
			frm: cur_frm
		})
	},

	make_purchase_invoice: function() {
		frappe.model.open_mapped_doc({
			method: "erpnext.buying.doctype.purchase_order.purchase_order.make_purchase_invoice",
			frm: cur_frm
		})
	},

	add_from_mappers: function() {
		cur_frm.add_custom_button(__('Material Request'),
			function() {
				frappe.model.map_current_doc({
					method: "erpnext.stock.doctype.material_request.material_request.make_purchase_order",
					source_doctype: "Material Request",
					get_query_filters: {
						material_request_type: "Purchase",
						docstatus: 1,
						status: ["!=", "Stopped"],
						per_ordered: ["<", 99.99],
						company: cur_frm.doc.company
					}
				})
			}, __("Add items from"));

		cur_frm.add_custom_button(__('Supplier Quotation'),
			function() {
				frappe.model.map_current_doc({
					method: "erpnext.buying.doctype.supplier_quotation.supplier_quotation.make_purchase_order",
					source_doctype: "Supplier Quotation",
					get_query_filters: {
						docstatus: 1,
						status: ["!=", "Stopped"],
						company: cur_frm.doc.company
					}
				})
			}, __("Add items from"));

	},

	tc_name: function() {
		this.get_terms();
	},

	items_add: function(doc, cdt, cdn) {
		var row = frappe.get_doc(cdt, cdn);
		this.frm.script_manager.copy_from_first_row("items", row, ["schedule_date"]);
	},

	make_bank_entry: function() {
		return frappe.call({
			method: "erpnext.accounts.doctype.journal_entry.journal_entry.get_payment_entry_against_order",
			args: {
				"dt": "Purchase Order",
				"dn": cur_frm.doc.name
			},
			callback: function(r) {
				var doclist = frappe.model.sync(r.message);
				frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
			}
		});
	},

	unclose_purchase_order: function(){
		cur_frm.cscript.update_status('Re-open', 'Submitted')
	},

	close_purchase_order: function(){
		cur_frm.cscript.update_status('Close', 'Closed')
	},

	delivered_by_supplier: function(){
		cur_frm.cscript.update_status('Deliver', 'Delivered')
	},

	get_last_purchase_rate: function() {
		frappe.call({
			"method": "get_last_purchase_rate",
			"doc": cur_frm.doc,
			callback: function(r, rt) {
				cur_frm.dirty();
				cur_frm.cscript.calculate_taxes_and_totals();
			}
		})
	}

});

// for backward compatibility: combine new and previous states
$.extend(cur_frm.cscript, new erpnext.buying.PurchaseOrderController({frm: cur_frm}));

cur_frm.cscript.update_status= function(label, status){
	frappe.call({
		method: "erpnext.buying.doctype.purchase_order.purchase_order.update_status",
		args: {status: status, name: cur_frm.doc.name},
		callback: function(r) {
			cur_frm.set_value("status", status);
			cur_frm.reload_doc();
		}
	})
}

cur_frm.fields_dict['supplier_address'].get_query = function(doc, cdt, cdn) {
	return {
		filters: {'supplier': doc.supplier}
	}
}

cur_frm.fields_dict['contact_person'].get_query = function(doc, cdt, cdn) {
	return {
		filters: {'supplier': doc.supplier}
	}
}

cur_frm.fields_dict['items'].grid.get_field('project').get_query = function(doc, cdt, cdn) {
	return {
		filters:[
			['Project', 'status', 'not in', 'Completed, Cancelled']
		]
	}
}

cur_frm.fields_dict['items'].grid.get_field('bom').get_query = function(doc, cdt, cdn) {
	var d = locals[cdt][cdn]
	return {
		filters: [
			['BOM', 'item', '=', d.item_code],
			['BOM', 'is_active', '=', '1'],
			['BOM', 'docstatus', '=', '1']
		]
	}
}

cur_frm.cscript.on_submit = function(doc, cdt, cdn) {
	if(cint(frappe.boot.notification_settings.purchase_order)) {
		cur_frm.email_doc(frappe.boot.notification_settings.purchase_order_message);
	}
}

cur_frm.cscript.schedule_date = function(doc, cdt, cdn) {
	erpnext.utils.copy_value_in_all_row(doc, cdt, cdn, "items", "schedule_date");
}

frappe.provide("erpnext.buying");

frappe.ui.form.on("Purchase Order", "is_subcontracted", function(frm) {
	if (frm.doc.is_subcontracted === "Yes") {
		erpnext.buying.get_default_bom(frm);
	}
});


// CUSTOMISATION HERE
cur_frm.cscript.items_on_form_rendered = function(doc, cdt, cdn){
	cur_frm.cscript.toggle_reqd_fields(doc, cdt, cdn);
}

frappe.ui.form.on("Purchase Order Item", "pricing_type", function(frm, cdt, cdn) {
	cur_frm.cscript.calculate_rate(frm, cdt, cdn);
});

frappe.ui.form.on("Purchase Order Item", "lme_price", function(frm, cdt, cdn) {
	cur_frm.cscript.calculate_rate(frm, cdt, cdn);
});

frappe.ui.form.on("Purchase Order Item", "lme_pricing", function(frm, cdt, cdn) {
	cur_frm.cscript.calculate_rate(frm, cdt, cdn);
});

cur_frm.cscript.calculate_rate = function(frm, cdt, cdn) {
	var item = locals[cdt][cdn];
	if(item.pricing_type === "LME") {
		item.rate = item.lme_pricing ? (flt(item.lme_price) * flt(item.lme_pricing) / 100) : flt(item.lme_price);
		this.calculate_taxes_and_totals();
	}
	refresh_field("rate", item.name, "items");
}

cur_frm.cscript.toggle_reqd_fields = function(doc, cdt, cdn) {
    var grid_row = cur_frm.open_grid_row();
	if(grid_row) {
		if(grid_row.doc.pricing_type === "LME") {
			grid_row.toggle_reqd("lme_date_1", true);
			grid_row.toggle_reqd("lme_date_2", true);
			grid_row.toggle_reqd("lme_price", true);
			grid_row.toggle_reqd("lme_pricing", true);
		} else {
			grid_row.toggle_reqd("lme_date_1", false);
			grid_row.toggle_reqd("lme_date_2", false);
			grid_row.toggle_reqd("lme_price", false);
			grid_row.toggle_reqd("lme_pricing", false);
		}
	}
}

cur_frm.cscript.calculate_pricing_description = function(doc, cdt, cdn) {
	var grid_row = cur_frm.open_grid_row();
	if(grid_row) {
		var item = locals[cdt][cdn];
		if(item.pricing_type === "LME") {
			if(item.lme_date_1 && item.lme_date_2) {
				var lme_date_1 = dateutil.str_to_obj(item.lme_date_1);
				var lme_date_2 = dateutil.str_to_obj(item.lme_date_2);
				var month_name1 = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][lme_date_1.getMonth()];
				var month_name2 = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][lme_date_2.getMonth()];
				var day1 = dateutil.get_day_diff(lme_date_1, moment(lme_date_1).startOf("month").format()) + 1;
				var day2 = dateutil.get_day_diff(lme_date_2, moment(lme_date_2).startOf("month").format()) + 1;
				
				if(lme_date_1.getMonth() === lme_date_2.getMonth() && dateutil.get_diff(lme_date_1, moment(lme_date_1).startOf("month").format()) === 0 && dateutil.get_diff(lme_date_2, moment(lme_date_2).endOf("month").format()) === 0) {
				    item.pricing_description = (item.lme_pricing || 0) + "% of" + " Average of " + month_name1 + " " + lme_date_1.getFullYear() + " LME - " + (item.lme_price || 0);
				} else if(dateutil.get_diff(lme_date_1, lme_date_2) === 0) {
				    item.pricing_description = (item.lme_pricing || 0) + "% of" + " Spot price of " + day1 + " " + month_name1 + " " + lme_date_1.getFullYear() + " LME - " + (item.lme_price || 0);
				} else {
				    item.pricing_description = (item.lme_pricing || 0) + "% of" + " Average of " + day1 + " " + month_name1 + " to " + day2 + " " + month_name2 + " " + lme_date_1.getFullYear() + " LME - " + (item.lme_price || 0);
				}
			}
		} else {
			item.pricing_description = "N/A";
		}
		refresh_field("pricing_description", item.name, "items");
	}
}

cur_frm.cscript.pricing_type = function(doc, cdt, cdn) {
	cur_frm.cscript.toggle_reqd_fields(doc, cdt, cdn);
	cur_frm.cscript.calculate_pricing_description(doc, cdt, cdn);
}

cur_frm.cscript.lme_date_1 = function(doc, cdt, cdn) {
	cur_frm.cscript.calculate_pricing_description(doc, cdt, cdn);
}

cur_frm.cscript.lme_date_2 = function(doc, cdt, cdn) {
	cur_frm.cscript.calculate_pricing_description(doc, cdt, cdn);
}

cur_frm.cscript.lme_price = function(doc, cdt, cdn) {
	cur_frm.cscript.calculate_pricing_description(doc, cdt, cdn);
}

cur_frm.cscript.lme_pricing = function(doc, cdt, cdn) {
	cur_frm.cscript.calculate_pricing_description(doc, cdt, cdn);
}

frappe.ui.form.on("Purchase Order", "validate", function(frm) {
    if(frm.doc.items) {
       for(i=0; i < frm.doc.items.length; i++) {
       		if(frm.doc.items[i].pricing_type == "LME") {
	            frm.doc.items[i].rate = frm.doc.items[i].lme_pricing ? (flt(frm.doc.items[i].lme_price) * flt(frm.doc.items[i].lme_pricing) / 100) : flt(frm.doc.items[i].lme_price);
       		} else {

       		}
        }
    }
});