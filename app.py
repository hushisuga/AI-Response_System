import json

# ----------------------------
# Intent Detection
# ----------------------------
def detect_intent(message):
    message = message.lower()
    
    if not message.strip():
        return "error_empty"
    
    if "water" in message or "leak" in message:
        return "maintenance_issue"
    elif "electric" in message or "power" in message:
        return "electrical_issue"
    elif "bill" in message or "payment" in message:
        return "billing_issue"
    elif len(message.split()) < 5:
        return "unclear_request"
    else:
        return "other"

# ----------------------------
# Urgency & Risk Detection
# ----------------------------
def detect_urgency_and_risk(message):
    message = message.lower()
    
    urgency = "low"
    risk = "low"
    
    # Urgency
    if any(word in message for word in ["emergency", "urgent", "fire", "flooding", "gas leak"]):
        urgency = "critical"
    elif any(word in message for word in ["severe", "immediate", "soon", "quick"]):
        urgency = "high"
    elif any(word in message for word in ["soon", "quick", "immediate"]):
        urgency = "medium"
    
    # Risk
    if any(word in message for word in ["fire", "gas", "electric", "flooding"]):
        risk = "high"
    elif any(word in message for word in ["minor", "medium", "moderate"]):
        risk = "medium"
    if any(word in message for word in ["hospital", "injury", "sick"]):
        risk = "medical_sensitive"
        urgency = "critical"
    if any(word in message for word in ["lawyer", "legal", "court", "complaint"]):
        risk = "legal_sensitive"
        urgency = "high"
    
    return urgency, risk

# ----------------------------
# Missing Information Detection
# ----------------------------
def detect_missing_information(message):
    message = message.lower()
    missing = []

    if not any(word in message for word in ["kitchen", "bathroom", "room", "ceiling", "wall"]):
        missing.append("Exact location of the issue")
    
    if not any(word in message for word in ["today", "yesterday", "morning", "evening", "hours", "days"]):
        missing.append("When the issue started")
    
    if not any(word in message for word in ["severe", "minor", "small", "large", "serious"]):
        missing.append("Severity level of the issue")

    return missing

# ----------------------------
# Mock LLM Response (Deterministic)
# ----------------------------
def mock_llm_response(intent, urgency, risk):

    # Acknowledgement & reply
    if urgency == "critical":
        acknowledgement = "This is a critical situation. Immediate action is advised."
        reply = "Our team has been alerted and will prioritize this issue immediately."
        next_steps = [
            "Avoid the affected area immediately.",
            "Contact emergency services if necessary."
        ]
    elif urgency == "high":
        acknowledgement = "We understand this is urgent and requires prompt attention."
        reply = "Our team will address this as soon as possible."
        next_steps = [
            "Monitor the situation closely.",
            "Share photos if possible."
        ]
    elif urgency == "medium":
        acknowledgement = "Thank you for the details. We will review this soon."
        reply = "Our team will schedule a review at the earliest availability."
        next_steps = [
            "Please monitor the situation.",
            "Provide additional details if available."
        ]
    else:  # low
        acknowledgement = "Thank you for reaching out. We understand your concern."
        reply = "Our team will review this and guide you with next steps shortly."
        next_steps = [
            "Please share additional details.",
            "Avoid using the affected area until reviewed."
        ]

    # Fallback for unclear information
    if intent == "unclear_request" or intent == "other":
        reply = "Information insufficient. Please provide more details."
    
    return {
        "intent": intent,
        "urgency_level": urgency,
        "risk_level": risk,
        "acknowledgement": acknowledgement,
        "analysis_summary": f"The issue appears related to {intent}.",
        "reply_draft": reply,
        "follow_up_questions": [
            "When did this issue first occur?",
            "Has this happened before?"
        ],
        "missing_information": [],
        "recommended_next_steps": next_steps,
        "explainability": {
            "intent_detected": intent,
            "urgency_reasoning": "Keyword-based detection",
            "risk_reasoning": "High-risk keyword scan"
        }
    }

# ----------------------------
# Process Customer Query
# ----------------------------
def process_query(customer_message):
    if not customer_message.strip():
        return {"error": "Empty query received."}

    intent = detect_intent(customer_message)
    urgency, risk = detect_urgency_and_risk(customer_message)
    missing_info = detect_missing_information(customer_message)

    structured_response = mock_llm_response(intent, urgency, risk)
    structured_response["missing_information"] = missing_info

    return structured_response

# ----------------------------
# Test
# ----------------------------
if __name__ == "__main__":
    test_messages = [
        "Small leak under sink",
        "Power outage in kitchen",
        "I have an unpaid bill",
        "Hi",
        "Patient fainted after using AC",
        "Lawyer complaint about contract",
        "Just wanted to ask a question"
    ]
    
    for msg in test_messages:
        result = process_query(msg)
        print(json.dumps(result, indent=4))
        print("\n---\n")