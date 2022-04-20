// Added By Shahroz Allauddin

frappe.ui.form.on("Consigments", "delivery_note", function (frm) {
    if(!frm.doc.delivery_note) return;

    cur_frm.set_query("packing_number", function() {
        return {
            "filters": {
                "delivery_note": frm.doc.delivery_note
            }
        };
    });
});

frappe.ui.form.on("Consigments", "packing_number", function (frm) {
    if(!frm.doc.packing_number) return;

    frappe.call({
        "method": "frappe.client.get",
        args: {
            doctype: "Packing Slip",
            name: frm.doc.packing_number
        },
        callback: function (data) {
            if(!data && !data.message) return;
            var doc_packing = data.message;

            if(doc_packing.items.length > 0){
                var items = doc_packing.items;
                 $.each(items, function (index, row) {
                    if(row.container_number) {
                        //cur_frm.script_manager.trigger("container_number", "Consigment Packing Item", row.container_number);
                        var child = cur_frm.add_child("items");
                        child.container_number = row.container_number; 
                        //frappe.model.set_value(child.doctype, child, "container_number", row.container_number);
                        cur_frm.refresh_field("items");
                    }
                 });
            }
        }
    });
});