frappe.listview_settings['Form Template'] = {
    add_fields: ["form_type", "title"],
    get_indicator: function(doc) {
        if (doc.form_type === "Quiz") {
            return [__("Quiz"), "blue", "form_type,=,Quiz"];
        } else {
            return [__("Survey"), "green", "form_type,=,Survey"];
        }
    }
};