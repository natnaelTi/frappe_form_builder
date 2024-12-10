import frappe
from frappe import _
from frappe.model.document import Document
import random

class FormTemplate(Document):
    def validate(self):
        self.validate_questions()
    
    def validate_questions(self):
        if not self.questions:
            frappe.throw(_("At least one question is required"))
            
        if self.form_type == "Quiz":
            for question in self.questions:
                if not question.correct_answer:
                    frappe.throw(_("Question {0} requires a correct answer for quiz forms").format(question.idx))
    
    def get_next_question(self, user, previous_question=None):
        """Get next random question based on skip count and previous responses"""
        if not self.questions:
            return None
            
        # Get all questions answered by user
        answered_questions = frappe.get_all(
            "Form Answer",
            filters={
                "form": self.name,
                "respondent": user
            },
            pluck="question"
        )
        
        # Filter available questions
        available_questions = [q for q in self.questions if q.name not in answered_questions]
        
        if previous_question and self.skip_count:
            # Find index of previous question and skip required number of questions
            try:
                prev_idx = next(i for i, q in enumerate(self.questions) if q.name == previous_question)
                skip_to = prev_idx + self.skip_count
                available_questions = [q for q in available_questions if self.questions.index(q) > skip_to]
            except (StopIteration, ValueError):
                pass
        
        if not available_questions:
            return None
            
        # Return random question if shuffle is enabled, otherwise first available
        return random.choice(available_questions) if self.shuffle_questions else available_questions[0]