frappe.ui.form.on('Form Template', {
    refresh: function(frm) {
        // Add custom buttons
        if (!frm.is_new()) {
            frm.add_custom_button(__('Preview'), function() {
                window.open('/form/' + frm.doc.name, '_blank');
            });
            
            frm.add_custom_button(__('View Responses'), function() {
                frappe.set_route('List', 'Form Response', {form: frm.doc.name});
            });
        }
    },
    
    form_type: function(frm) {
        // Show/hide quiz specific fields
        frm.trigger('toggle_quiz_fields');
    },
    
    toggle_quiz_fields: function(frm) {
        const isQuiz = frm.doc.form_type === 'Quiz';
        frm.toggle_display(['max_attempts', 'skip_count', 'shuffle_questions'], isQuiz);
    }
});