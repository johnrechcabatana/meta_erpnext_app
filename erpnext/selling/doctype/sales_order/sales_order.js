// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

{% include 'selling/sales_common.js' %}

frappe.ui.form.on("Sales Order", {
	onload: function(frm) {
		erpnext.queries.setup_queries(frm, "Warehouse", function() {
			return erpnext.queries.warehouse(frm.doc);
		});
		
		cur_frm.set_query("shipping_agent", function(doc) {
			return {
				query:"erpnext.selling.doctype.sales_order.sales_order.get_user_by_role",
				filters:{
					role: "%agent%"
				}
			}
		});
	
		cur_frm.set_query("sales_person", "sales_rep", function(doc) {
				return {
					query:"erpnext.selling.doctype.sales_order.sales_order.get_sales_person_by_role",
					filters:{
						role: "%sales%"
					}
				}
			});
	}
});

erpnext.selling.SalesOrderController = erpnext.selling.SellingController.extend({
	refresh: function(doc, dt, dn) {
		this._super();
		this.frm.dashboard.reset();
		var allow_purchase = false;
		var allow_delivery = false;

		if(doc.docstatus==1) {
			if(doc.status != 'Closed') {

				for (var i in cur_frm.doc.items) {
					var item = cur_frm.doc.items[i];
					if(item.delivered_by_supplier === 1 || item.supplier){
						if(item.qty > flt(item.ordered_qty)
							&& item.qty > flt(item.delivered_qty)) {
							allow_purchase = true;
						}
					}

					if (item.delivered_by_supplier===0) {
						if(item.qty > flt(item.delivered_qty)) {
							allow_delivery = true;
						}
					}

					if (allow_delivery && allow_purchase) {
						break;
					}
				}

				if (this.frm.has_perm("submit")) {
					// close
					if(flt(doc.per_delivered, 2) < 100 || flt(doc.per_billed) < 100) {
							cur_frm.add_custom_button(__('Close'), this.close_sales_order, __("Status"))
						}
				}

				// Code Committed by Shahroz Allauddin
				// delivery note
				// if(flt(doc.per_delivered, 2) < 100 && ["Sales", "Shopping Cart"].indexOf(doc.order_type)!==-1 && allow_delivery) {
				// 	cur_frm.add_custom_button(__('Delivery'), this.make_delivery_note, __("Make"));
				// 	cur_frm.page.set_inner_btn_group_as_primary(__("Make"));
				// }

				// sales invoice
				if(flt(doc.per_billed, 2) < 100) {
					cur_frm.add_custom_button(__('Invoice'), this.make_sales_invoice, __("Make"));
				}

				// material request
				if(!doc.order_type || ["Sales", "Shopping Cart"].indexOf(doc.order_type)!==-1
					&& flt(doc.per_delivered, 2) < 100) {
						cur_frm.add_custom_button(__('Material Request'), this.make_material_request, __("Make"));
				}

				// make purchase order
				if(flt(doc.per_delivered, 2) < 100 && allow_purchase) {
					cur_frm.add_custom_button(__('Purchase Order'), cur_frm.cscript.make_purchase_order, __("Make"));
				}

				if(flt(doc.per_billed)==0) {
					cur_frm.add_custom_button(__('Payment Request'), this.make_payment_request, __("Make"));
					cur_frm.add_custom_button(__('Payment'), cur_frm.cscript.make_bank_entry, __("Make"));
				}

				// maintenance
				if(flt(doc.per_delivered, 2) < 100 && ["Sales", "Shopping Cart"].indexOf(doc.order_type)===-1) {
					cur_frm.add_custom_button(__('Maintenance Visit'), this.make_maintenance_visit, __("Make"));
					cur_frm.add_custom_button(__('Maintenance Schedule'), this.make_maintenance_schedule, __("Make"));
				}


			} else {
				if (this.frm.has_perm("submit")) {
					// un-close
					cur_frm.add_custom_button(__('Re-open'), cur_frm.cscript['Unclose Sales Order'], __("Status"));
				}
			}
		}

		if (this.frm.doc.docstatus===0) {
			cur_frm.add_custom_button(__('Quotation'),
				function() {
					frappe.model.map_current_doc({
						method: "erpnext.selling.doctype.quotation.quotation.make_sales_order",
						source_doctype: "Quotation",
						get_query_filters: {
							docstatus: 1,
							status: ["!=", "Lost"],
							order_type: cur_frm.doc.order_type,
							customer: cur_frm.doc.customer || undefined,
							company: cur_frm.doc.company
						}
					})
				}, __("Get items from"));
		}

		this.order_type(doc);
	},

	order_type: function() {
		this.frm.toggle_reqd("delivery_date", this.frm.doc.order_type == "Sales");
	},

	tc_name: function() {
		this.get_terms();
	},
	
	make_material_request: function() {
		frappe.model.open_mapped_doc({
			method: "erpnext.selling.doctype.sales_order.sales_order.make_material_request",
			frm: cur_frm
		})
	},

	make_delivery_note: function() {
		frappe.model.open_mapped_doc({
			method: "erpnext.selling.doctype.sales_order.sales_order.make_delivery_note",
			frm: cur_frm
		})
	},

	make_sales_invoice: function() {
		frappe.model.open_mapped_doc({
			method: "erpnext.selling.doctype.sales_order.sales_order.make_sales_invoice",
			frm: cur_frm
		})
	},

	make_maintenance_schedule: function() {
		frappe.model.open_mapped_doc({
			method: "erpnext.selling.doctype.sales_order.sales_order.make_maintenance_schedule",
			frm: cur_frm
		})
	},

	make_maintenance_visit: function() {
		frappe.model.open_mapped_doc({
			method: "erpnext.selling.doctype.sales_order.sales_order.make_maintenance_visit",
			frm: cur_frm
		})
	},

	make_bank_entry: function() {
		return frappe.call({
			method: "erpnext.accounts.doctype.journal_entry.journal_entry.get_payment_entry_against_order",
			args: {
				"dt": "Sales Order",
				"dn": cur_frm.doc.name
			},
			callback: function(r) {
				var doclist = frappe.model.sync(r.message);
				frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
			}
		});
	},
	make_purchase_order: function(){
		var dialog = new frappe.ui.Dialog({
			title: __("For Supplier"),
			fields: [
				{"fieldtype": "Link", "label": __("Supplier"), "fieldname": "supplier", "options":"Supplier",
					"get_query": function () {
						return {
							query:"erpnext.selling.doctype.sales_order.sales_order.get_supplier",
							filters: {'parent': cur_frm.doc.name}
						}
					}, "reqd": 1 },
				{"fieldtype": "Button", "label": __("Make Purchase Order"), "fieldname": "make_purchase_order", "cssClass": "btn-primary"},
			]
		});

		dialog.fields_dict.make_purchase_order.$input.click(function() {
			args = dialog.get_values();
			if(!args) return;
			dialog.hide();
			return frappe.call({
				type: "GET",
				method: "erpnext.selling.doctype.sales_order.sales_order.make_purchase_order_for_drop_shipment",
				args: {
					"source_name": cur_frm.doc.name,
					"for_supplier": args.supplier
				},
				freeze: true,
				callback: function(r) {
					if(!r.exc) {
						var doc = frappe.model.sync(r.message);
						frappe.set_route("Form", r.message.doctype, r.message.name);
					}
				}
			})
		});
		dialog.show();
	},
	close_sales_order: function(){
		cur_frm.cscript.update_status("Close", "Closed")
	}

});

// for backward compatibility: combine new and previous states
$.extend(cur_frm.cscript, new erpnext.selling.SalesOrderController({frm: cur_frm}));

cur_frm.cscript.new_contact = function(){
	tn = frappe.model.make_new_doc_and_get_name('Contact');
	locals['Contact'][tn].is_customer = 1;
	if(doc.customer) locals['Contact'][tn].customer = doc.customer;
	loaddoc('Contact', tn);
}

cur_frm.fields_dict['project'].get_query = function(doc, cdt, cdn) {
	return {
		query: "erpnext.controllers.queries.get_project_name",
		filters: {
			'customer': doc.customer
		}
	}
}

cur_frm.cscript.update_status = function(label, status){
	var doc = cur_frm.doc;
	frappe.ui.form.is_saving = true;
	frappe.call({
		method: "erpnext.selling.doctype.sales_order.sales_order.update_status",
		args: {status: status, name: doc.name},
		callback: function(r){
			cur_frm.reload_doc();
		},
		always: function() {
			frappe.ui.form.is_saving = false;
		}
	});
}

cur_frm.cscript['Unclose Sales Order'] = function() {
	cur_frm.cscript.update_status('Re-open', 'Draft')
}

cur_frm.cscript.on_submit = function(doc, cdt, cdn) {
	if(cint(frappe.boot.notification_settings.sales_order)) {
		cur_frm.email_doc(frappe.boot.notification_settings.sales_order_message);
	}
};

// CUSTOMISATION HERE
cur_frm.cscript.items_on_form_rendered = function(doc, cdt, cdn){
	cur_frm.cscript.toggle_reqd_fields(doc, cdt, cdn);
}

frappe.ui.form.on("Sales Order Item", "pricing_type", function(frm, cdt, cdn) {
	cur_frm.cscript.calculate_rate(frm, cdt, cdn);
});

frappe.ui.form.on("Sales Order Item", "lme_price", function(frm, cdt, cdn) {
	cur_frm.cscript.calculate_rate(frm, cdt, cdn);
});

frappe.ui.form.on("Sales Order Item", "lme_pricing", function(frm, cdt, cdn) {
	cur_frm.cscript.calculate_rate(frm, cdt, cdn);
});

cur_frm.cscript.calculate_rate = function(frm, cdt, cdn) {
	var item = locals[cdt][cdn];
	if(item.pricing_type === "LME") {
		item.rate = item.lme_pricing ? (flt(item.lme_price) * flt(item.lme_pricing) / 100) : flt(item.lme_price);
		this.set_gross_profit(item);
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

frappe.ui.form.on("Sales Order", "validate", function(frm) {
    if(frm.doc.items) {
       for(i=0; i < frm.doc.items.length; i++) {
       		if(frm.doc.items[i].pricing_type == "LME") {
	            frm.doc.items[i].rate = frm.doc.items[i].lme_pricing ? (flt(frm.doc.items[i].lme_price) * flt(frm.doc.items[i].lme_pricing) / 100) : flt(frm.doc.items[i].lme_price);
       		} else {

       		}
        }
    }
});
