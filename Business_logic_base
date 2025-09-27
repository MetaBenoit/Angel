# backend/app/services/business_logic.py
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum

logger = logging.getLogger(__name__)

class ConversationStage(Enum):
    GREETING = "greeting"
    QUALIFICATION = "qualification"
    CONSULTATION = "consultation"
    ESCALATION = "escalation"
    CONCLUDED = "concluded"

class ResponseLength(Enum):
    SHORT = "short"      # 1-2 sentences for simple questions
    MEDIUM = "medium"    # 2-3 sentences for standard responses
    LONG = "long"        # 3-4 sentences for complex topics

class AccuracyLevel(Enum):
    FACTUAL_CRITICAL = "factual_critical"    # Names, spelling, numbers, legal facts
    PROFESSIONAL_OPINION = "professional_opinion"  # Market trends, recommendations
    CASUAL_CONVERSATION = "casual_conversation"    # General chat, preferences

class DaoBusinessLogic:
    """Advanced business process management for Dao with accuracy safeguards"""
    
    def __init__(self):
        self.max_conversation_turns = 4
        self.conversations = {}
        
        # Qualification signals to track
        self.key_qualifiers = {
            'budget': ['budget', 'price', 'cost', 'baht', 'million', 'thousand'],
            'location': ['jomtien', 'central', 'beach', 'naklua', 'pratumnak', 'area', 'location'],
            'property_type': ['condo', 'villa', 'house', 'apartment', 'townhouse'],
            'timeline': ['soon', 'quickly', 'month', 'year', 'urgent', 'when'],
            'purpose': ['live', 'living', 'investment', 'rental', 'home', 'move'],
            'experience': ['first time', 'bought before', 'new to', 'experienced']
        }
        
        # Escalation triggers (topics that should go to specialists)
        self.escalation_topics = [
            'visa', 'legal', 'tax', 'financing', 'loan', 'mortgage', 
            'ownership', 'contract', 'lawyer', 'bank', 'government'
        ]
        
        # NEW: Accuracy-critical topics that require precision
        self.factual_critical_topics = [
            'spell', 'spelling', 'name', 'number', 'price', 'cost', 'legal requirement',
            'law', 'regulation', 'tax rate', 'percentage', 'exact', 'specific'
        ]
        
        # NEW: Topics requiring clarification rather than assumptions
        self.clarification_triggers = [
            'my name', 'your name', 'how do you spell', 'what is my', 'who am i',
            'remember me', 'recall', 'you said', 'earlier you mentioned'
        ]
        
        # NEW: Professional humility triggers  
        self.uncertainty_indicators = [
            'exactly', 'precise', 'specific number', 'guarantee', 'promise',
            'legal advice', 'tax advice', 'visa requirement'
        ]

    def _determine_accuracy_level(self, user_message: str) -> AccuracyLevel:
        """Determine required accuracy level for response"""
        message_lower = user_message.lower()
        
        # Critical accuracy needed
        if any(topic in message_lower for topic in self.factual_critical_topics):
            return AccuracyLevel.FACTUAL_CRITICAL
        
        # Professional opinion acceptable  
        qualifier_keywords = [kw for sublist in self.key_qualifiers.values() for kw in sublist]
        if any(keyword in message_lower for keyword in qualifier_keywords):
            return AccuracyLevel.PROFESSIONAL_OPINION
            
        return AccuracyLevel.CASUAL_CONVERSATION

    def _needs_clarification(self, user_message: str) -> bool:
        """Check if question requires clarification rather than assumption"""
        message_lower = user_message.lower()
        return any(trigger in message_lower for trigger in self.clarification_triggers)

    def _requires_uncertainty_admission(self, user_message: str) -> bool:
        """Check if response should include uncertainty/limitation admission"""
        message_lower = user_message.lower()
        return any(indicator in message_lower for indicator in self.uncertainty_indicators)

    def analyze_conversation_context(self, conversation_id: str, user_message: str) -> Dict[str, Any]:
        """Comprehensive conversation analysis for business logic"""
        
        # Initialize or get conversation
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = {
                'stage': ConversationStage.GREETING,
                'turn_count': 0,
                'qualifications': {},
                'greeting_used': False,
                'escalation_suggested': False,
                'messages': [],
                'created_at': datetime.now()
            }
        
        conv = self.conversations[conversation_id]
        conv['turn_count'] += 1
        conv['messages'].append({
            'user': user_message,
            'timestamp': datetime.now()
        })
        
        # Analyze current message
        analysis = {
            'conversation_id': conversation_id,
            'turn_count': conv['turn_count'],
            'current_stage': conv['stage'],
            'greeting_needed': self._should_greet(conv, user_message),
            'response_length': self._determine_response_length(user_message, conv),
            'qualification_signals': self._extract_qualifications(user_message),
            'escalation_needed': self._check_escalation_triggers(user_message),
            'accuracy_level': self._determine_accuracy_level(user_message),
            'needs_clarification': self._needs_clarification(user_message),
            'requires_uncertainty': self._requires_uncertainty_admission(user_message),
            'business_instructions': self._generate_business_instructions(conv, user_message)
        }
        
        # Update conversation state
        self._update_conversation_stage(conv, analysis)
        
        # Update qualifications
        conv['qualifications'].update(analysis['qualification_signals'])
        
        logger.info(f"Conversation {conversation_id}: Turn {conv['turn_count']}, "
                   f"Stage: {conv['stage'].value}, Accuracy: {analysis['accuracy_level'].value}")
        
        return analysis
    
    def _should_greet(self, conv: Dict, user_message: str) -> Tuple[bool, str]:
        """Determine if greeting is needed and which type"""
        if conv['greeting_used']:
            return False, None
        
        message_lower = user_message.lower()
        
        # If user uses Thai greeting, respond in Thai
        if any(thai in message_lower for thai in ['สวัสดี', 'sawasdee', 'sawadee']):
            return True, "thai"
        
        # If formal business inquiry, use English
        if any(formal in message_lower for formal in ['inquiry', 'interested in', 'looking for property']):
            return True, "english_formal"
        
        # Default warm English greeting for first interaction
        return True, "english_warm"
    
    def _determine_response_length(self, user_message: str, conv: Dict) -> ResponseLength:
        """Determine appropriate response length based on question complexity"""
        message_lower = user_message.lower()
        
        # Short responses for simple questions
        short_triggers = [
            'yes', 'no', 'ok', 'thanks', 'thank you', 'good', 'great',
            'how much', 'when', 'where', 'what time'
        ]
        
        # Long responses for complex topics
        long_triggers = [
            'tell me about', 'explain', 'what should i know', 'help me understand',
            'difference between', 'compare', 'pros and cons', 'process', 'steps'
        ]
        
        if any(trigger in message_lower for trigger in short_triggers):
            return ResponseLength.SHORT
        elif any(trigger in message_lower for trigger in long_triggers):
            return ResponseLength.LONG
        else:
            return ResponseLength.MEDIUM
    
    def _extract_qualifications(self, user_message: str) -> Dict[str, Any]:
        """Extract qualification signals from user message"""
        signals = {}
        message_lower = user_message.lower()
        
        for category, keywords in self.key_qualifiers.items():
            found_keywords = [kw for kw in keywords if kw in message_lower]
            if found_keywords:
                signals[category] = found_keywords
        
        # Extract specific values
        budget_match = re.search(r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:million|baht|k)', message_lower)
        if budget_match:
            signals['budget_amount'] = budget_match.group(1)
        
        # Urgency detection
        urgency_words = ['urgent', 'asap', 'quickly', 'soon', 'this week', 'immediately']
        if any(word in message_lower for word in urgency_words):
            signals['urgency'] = 'high'
        
        return signals
    
    def _check_escalation_triggers(self, user_message: str) -> Dict[str, Any]:
        """Check if message contains topics requiring specialist escalation"""
        message_lower = user_message.lower()
        
        triggered_topics = []
        for topic in self.escalation_topics:
            if topic in message_lower:
                triggered_topics.append(topic)
        
        return {
            'needs_escalation': len(triggered_topics) > 0,
            'topics': triggered_topics,
            'specialist_type': self._suggest_specialist(triggered_topics)
        }
    
    def _suggest_specialist(self, topics: List[str]) -> Optional[str]:
        """Suggest appropriate specialist based on topics"""
        if any(topic in ['visa', 'legal', 'ownership', 'contract'] for topic in topics):
            return "legal_specialist"
        elif any(topic in ['financing', 'loan', 'mortgage', 'bank'] for topic in topics):
            return "finance_specialist"
        elif any(topic in ['tax'] for topic in topics):
            return "tax_specialist"
        return "property_specialist"
    
    def _generate_business_instructions(self, conv: Dict, user_message: str) -> List[str]:
        """Generate specific business instructions including accuracy guidance"""
        instructions = []
        
        # NEW: Accuracy-based instructions
        accuracy_level = self._determine_accuracy_level(user_message)
        if accuracy_level == AccuracyLevel.FACTUAL_CRITICAL:
            instructions.append("ACCURACY_CRITICAL: Ask for clarification if unsure, admit limitations, be precise")
        
        if self._needs_clarification(user_message):
            instructions.append("CLARIFICATION_NEEDED: Ask for specific information rather than assuming")
        
        if self._requires_uncertainty_admission(user_message):
            instructions.append("ADMIT_UNCERTAINTY: Acknowledge limitations and offer to connect with specialist")
        
        # Stage-specific instructions
        if conv['stage'] == ConversationStage.GREETING:
            instructions.append("GREETING_STAGE: Warm welcome, introduce yourself, start gentle qualification")
        elif conv['stage'] == ConversationStage.QUALIFICATION:
            instructions.append("QUALIFICATION_STAGE: Build rapport while gathering specific needs")
        elif conv['stage'] == ConversationStage.ESCALATION:
            instructions.append("ESCALATION_STAGE: Guide toward concrete next steps - office visit or specialist meeting")
        
        # Turn-based guidance
        if conv['turn_count'] == 1:
            instructions.append("FIRST_INTERACTION: Set friendly, professional tone")
        elif conv['turn_count'] >= 3:
            instructions.append("CONVERSATION_MATURE: Start moving toward action items")
        elif conv['turn_count'] >= 4:
            instructions.append("ESCALATION_TIME: Strong push for next concrete step")
        
        # Qualification-specific instructions
        qualifications = conv.get('qualifications', {})
        if 'budget' in qualifications:
            instructions.append("BUDGET_KNOWN: Work within mentioned budget range")
        if 'location' in qualifications:
            instructions.append("LOCATION_INTEREST: Focus on preferred areas")
        if len(qualifications) >= 3:
            instructions.append("WELL_QUALIFIED: Ready for specific recommendations")
        
        return instructions
    
    def _update_conversation_stage(self, conv: Dict, analysis: Dict):
        """Update conversation stage based on analysis"""
        current_stage = conv['stage']
        turn_count = conv['turn_count']
        
        if current_stage == ConversationStage.GREETING and turn_count >= 1:
            conv['stage'] = ConversationStage.QUALIFICATION
        elif current_stage == ConversationStage.QUALIFICATION and turn_count >= 3:
            conv['stage'] = ConversationStage.CONSULTATION
        elif current_stage == ConversationStage.CONSULTATION and turn_count >= 4:
            conv['stage'] = ConversationStage.ESCALATION
        elif analysis['escalation_needed']['needs_escalation']:
            conv['stage'] = ConversationStage.ESCALATION
    
    def build_context_prompt(self, user_message: str, conversation_id: str) -> str:
        """Build enhanced context prompt with accuracy safeguards"""
        analysis = self.analyze_conversation_context(conversation_id, user_message)
        
        context_parts = []
        
        # NEW: Accuracy guidance
        if analysis['accuracy_level'] == AccuracyLevel.FACTUAL_CRITICAL:
            context_parts.append("ACCURACY_REQUIRED: If you don't know something precisely, say so and ask for clarification")
        
        if analysis['needs_clarification']:
            context_parts.append("ASK_FOR_CLARIFICATION: Don't assume information - ask the client directly")
        
        if analysis['requires_uncertainty']:
            context_parts.append("PROFESSIONAL_LIMITS: Acknowledge what you don't know and offer specialist help")
        
        # Greeting instruction
        if analysis['greeting_needed']:
            greeting_type = analysis['greeting_needed'][1]
            if greeting_type == "thai":
                context_parts.append("GREETING: Use 'Sawasdee ka!' then introduce yourself warmly")
            elif greeting_type == "english_formal":
                context_parts.append("GREETING: Professional introduction as Dao from Ires Thailand")
            else:
                context_parts.append("GREETING: Warm 'Hi there!' introduction")
            # Mark greeting as used
            self.conversations[conversation_id]['greeting_used'] = True
        
        # Response length guidance
        length_instruction = {
            ResponseLength.SHORT: "RESPONSE_LENGTH: 1-2 sentences, direct and helpful",
            ResponseLength.MEDIUM: "RESPONSE_LENGTH: 2-3 sentences, warm and informative", 
            ResponseLength.LONG: "RESPONSE_LENGTH: 3-4 sentences, thorough but concise"
        }
        context_parts.append(length_instruction[analysis['response_length']])
        
        # Business instructions
        context_parts.extend(analysis['business_instructions'])
        
        # Escalation instructions
        if analysis['escalation_needed']['needs_escalation']:
            specialist = analysis['escalation_needed']['specialist_type']
            context_parts.append(f"ESCALATION_NEEDED: Topics require {specialist} - offer office meeting")
        
        # Qualification context
        if analysis['qualification_signals']:
            signals_str = ", ".join(analysis['qualification_signals'].keys())
            context_parts.append(f"QUALIFICATION_SIGNALS: Client mentioned {signals_str}")
        
        # Build final prompt with accuracy emphasis
        if context_parts:
            business_context = " | ".join(context_parts)
            enhanced_prompt = f"""BUSINESS_CONTEXT: {business_context}

ACCURACY_REMINDER: You are Dao, a professional real estate agent. Be precise about facts, admit when you're unsure, and ask for clarification rather than guessing. Your reputation depends on accuracy.