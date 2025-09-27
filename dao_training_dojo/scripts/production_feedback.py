import json
from datetime import datetime

class ProductionFeedbackCollector:
    """Collect problematic interactions from production for retraining"""
    
    def __init__(self):
        self.feedback_file = '../datasets/production_feedback.json'
        
    def log_problematic_interaction(self, user_message, dao_response, issue_type, correct_response=None):
        """Log interactions that need improvement"""
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "dao_response": dao_response,
            "issue_type": issue_type,  # "accuracy", "assumption", "hallucination"
            "correct_response": correct_response,
            "needs_retraining": True
        }
        
        # Append to feedback file
        try:
            with open(self.feedback_file, 'r') as f:
                feedback_data = json.load(f)
        except FileNotFoundError:
            feedback_data = []
            
        feedback_data.append(feedback_entry)
        
        with open(self.feedback_file, 'w') as f:
            json.dump(feedback_data, f, indent=2)
    
    def generate_training_corrections(self):
        """Convert feedback into training examples"""
        with open(self.feedback_file, 'r') as f:
            feedback_data = json.load(f)
        
        training_examples = []
        for feedback in feedback_data:
            if feedback.get('correct_response'):
                training_examples.append({
                    "messages": [
                        {"role": "user", "content": feedback['user_message']},
                        {"role": "assistant", "content": feedback['correct_response']}
                    ]
                })
        
        return training_examples

# Usage example for the name spelling issue you encountered:
feedback_collector = ProductionFeedbackCollector()
feedback_collector.log_problematic_interaction(
    user_message="How do you spell my name?",
    dao_response="Your name is spelled as 'Jade.' It's very beautiful!",
    issue_type="assumption",
    correct_response="I'd be happy to help spell your name correctly! Could you tell me what your name is first? I want to make sure I get it exactly right."
)