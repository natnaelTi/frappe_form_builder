import frappe
from frappe import _
from frappe.model.document import Document

class FormResponse(Document):
    def validate(self):
        self.validate_attempt_limit()
        if self.status == "Completed":
            self.calculate_score()
    
    def validate_attempt_limit(self):
        if not self.is_new():
            return
            
        form = frappe.get_doc("Form Template", self.form)
        if form.form_type != "Quiz":
            return
            
        attempts = frappe.db.count(
            "Form Response",
            {
                "form": self.form,
                "respondent": self.respondent,
                "docstatus": 1
            }
        )
        
        if attempts >= form.max_attempts:
            frappe.throw(_("Maximum attempts reached for this quiz"))
    
    def calculate_score(self):
        if not self.responses:
            return
            
        form = frappe.get_doc("Form Template", self.form)
        if form.form_type != "Quiz":
            return
            
        total_points = 0
        earned_points = 0
        
        for response in self.responses:
            question = frappe.db.get_value(
                "Form Question",
                response.question,
                ["correct_answer", "points"],
                as_dict=True
            )
            
            if not question:
                continue
                
            total_points += question.points or 1
            if response.answer == question.correct_answer:
                earned_points += question.points or 1
        
        self.score = (earned_points / total_points * 100) if total_points else 0