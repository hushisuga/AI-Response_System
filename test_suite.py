from app import process_query
import json

# Define test inputs
test_inputs = [
    "Water leak in the kitchen sink",                   # maintenance_issue
    "Power outage in the living room",                  # electrical_issue
    "My bill seems too high",                            # billing_issue
    "Hi",                                               # unclear_request
    "I feel unsafe about the wiring",                   # electrical_issue, medium risk
    "Emergency! Gas leak in basement",                  # maintenance_issue, high risk
    "Just wanted to say thanks for your service"        # other / harmless
]

# Run tests and print outputs
for i, message in enumerate(test_inputs, 1):
    result = process_query(message)
    print(f"--- Test Case {i} ---")
    print(json.dumps(result, indent=4))
    print("\n")