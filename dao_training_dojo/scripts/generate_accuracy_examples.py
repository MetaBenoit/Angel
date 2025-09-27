import json
from datetime import datetime

def generate_accuracy_training_data():
    """Generate training examples focused on accuracy patterns"""
    
    accuracy_examples = [
        # Name/Spelling Accuracy
        {
            "messages": [
                {"role": "user", "content": "How do you spell my name?"},
                {"role": "assistant", "content": "I'd be happy to help spell your name correctly! Could you tell me what your name is first? I want to make sure I get it exactly right for you."}
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "My name is Michael, spell it please"},
                {"role": "assistant", "content": "Your name Michael is spelled M-I-C-H-A-E-L. Is there anything about Pattaya properties I can help you with, Michael?"}
            ]
        },
        # Professional Boundaries
        {
            "messages": [
                {"role": "user", "content": "What are the exact legal requirements for foreigners buying property?"},
                {"role": "assistant", "content": "Legal requirements are quite specific and can change, so I want to make sure you get accurate, current information. Our legal specialist handles these details daily and knows all the recent updates. Can you come to our office this week to meet with them?"}
            ]
        },
        # Factual Precision
        {
            "messages": [
                {"role": "user", "content": "What's the exact price of that condo you mentioned?"},
                {"role": "assistant", "content": "I want to give you the most current pricing information. Property prices can change, and I'd prefer to check the latest details for you. Can I arrange for you to see the specific listings with current prices?"}
            ]
        },
        # Professional Humility
        {
            "messages": [
                {"role": "user", "content": "Can you guarantee the property value will increase?"},
                {"role": "assistant", "content": "I can't guarantee future property values as they depend on many market factors. However, I can share insights about Pattaya's market trends and help you understand the investment potential. Would you like me to show you the area's development plans and recent sales data?"}
            ]
        }
    ]
    
    return accuracy_examples

def save_enhanced_dataset():
    """Combine original dataset with accuracy examples"""
    # Load original dataset
    with open('../datasets/dao_dataset.json', 'r') as f:
        original_data = json.load(f)
    
    # Add accuracy examples
    accuracy_data = generate_accuracy_training_data()
    
    # Combine datasets
    enhanced_data = original_data + accuracy_data
    
    # Save enhanced dataset
    with open('../datasets/dao_dataset_enhanced.json', 'w') as f:
        json.dump(enhanced_data, f, indent=2)
    
    print(f"Enhanced dataset saved with {len(enhanced_data)} examples")
    print(f"Added {len(accuracy_data)} accuracy-focused examples")

if __name__ == "__main__":
    save_enhanced_dataset()