import frappe
from frappe import _
from frappe.utils import now_datetime
from typing import Dict, Any, Optional
from .utils.form_utils import get_form_progress, validate_response

@frappe.whitelist()
def get_next_question(form_id: str, previous_question: Optional[str] = None) -> Dict[str, Any]:
    """Get next question for the form"""
    if not form_id:
        frappe.throw(_("Form ID is required"))
        
    form = frappe.get_doc("Form Template", form_id)
    user = frappe.session.user
    
    # Get user's progress
    progress = get_form_progress(form_id, user)
    
    if progress["completed"] or (
        form.form_type == "Quiz" and 
        progress["total_attempts"] >= form.max_attempts
    ):
        return {"status": "completed"}
        
    next_question = form.get_next_question(user, previous_question)
    
    if not next_question:
        return {"status": "no_questions"}
        
    return {
        "status": "success",
        "question": {
            "id": next_question.name,
            "text": next_question.question_text,
            "type": next_question.question_type,
            "options": frappe.get_all(
                "Form Question Option",
                filters={"parent": next_question.name},
                fields=["option_text", "option_value"]
            ) if next_question.question_type in ["Single Choice", "Multiple Choice"] else None
        }
    }

@frappe.whitelist()
def submit_response(form_id: str, question_id: str, answer: Any) -> Dict[str, Any]:
    """Submit answer for a question"""
    if not form_id or not question_id:
        frappe.throw(_("Form ID and Question ID are required"))
        
    user = frappe.session.user
    
    # Validate response
    validation = validate_response(form_id, question_id, answer)
    
    # Create or update response
    response = frappe.get_doc({
        "doctype": "Form Response",
        "form": form_id,
        "respondent": user,
        "responses": [{
            "question": question_id,
            "answer": answer,
            "is_correct": validation["is_correct"],
            "points": validation["points"]
        }],
        "start_time": now_datetime()
    })
    
    response.insert()
    
    return {
        "status": "success",
        "validation": validation,
        "next_question": get_next_question(form_id, question_id)
    }