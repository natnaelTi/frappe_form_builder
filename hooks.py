app_name = "form_builder"
app_title = "Form Builder"
app_publisher = "Your Organization"
app_description = "Interactive Form and Quiz Builder"
app_email = "your@email.com"
app_license = "MIT"

# Includes in <head>
app_include_css = ["/assets/form_builder/css/form_builder.css"]
app_include_js = ["/assets/form_builder/js/form_builder.js"]

# Include fixtures
fixtures = [
    {
        "doctype": "Form Template",
        "filters": [["modified", ">", "2023-01-01"]]
    },
    {
        "doctype": "Form Question",
        "filters": [["modified", ">", "2023-01-01"]]
    }
]

# Document Events
doc_events = {
    "Form Response": {
        "after_insert": "form_builder.form_builder.doctype.form_response.form_response.process_response"
    }
}