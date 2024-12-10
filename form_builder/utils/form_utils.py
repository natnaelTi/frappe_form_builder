import frappe
from frappe import _
from typing import Optional, Dict, Any, List

def get_form_progress(form_id: str, user: str) -> Dict[str, Any]:
    """Get user's progress for a specific form"""
    form = frappe.get_doc("Form Template", form_id)
    responses = frappe.get_all(
        "Form Response",
        filters={
            "form": form_id,
            "respondent": user,
            "docstatus": 1
        },
        fields=["name", "score", "status", "attempt_count"]
    )
    
    return {
        "total_attempts": len(responses),
        "max_attempts": form.max_attempts if form.form_type == "Quiz" else None,
        "best_score": max([r.score for r in responses] or [0]) if form.form_type == "Quiz" else None,
        "completed": any(r.status == "Completed" for r in responses)
    }

def validate_response(form_id: str, question_id: str, answer: Any) -> Dict[str, Any]:
    """Validate a single question response"""
    question = frappe.get_doc("Form Question", question_id)
    
    if not question:
        frappe.throw(_("Invalid question"))
        
    is_correct = False
    feedback = ""
    
    if question.question_type in ["Single Choice", "Multiple Choice"]:
        is_correct = str(answer) == str(question.correct_answer)
    elif question.question_type in ["Text", "Number"]:
        is_correct = str(answer).strip().lower() == str(question.correct_answer).strip().lower()
        
    return {
        "is_correct": is_correct,
        "feedback": feedback,
        "points": question.points if is_correct else 0
    }