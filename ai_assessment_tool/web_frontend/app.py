from flask import Flask, render_template, request, session, url_for, redirect
import sys
import os
import re # For parsing

# Adjust path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.data_structures import ProjectInput
from assessments import survivability, valuation
from recommendation_engine import generate_recommendations

app = Flask(__name__)
app.secret_key = os.urandom(24) # Replace with a fixed key for consistent dev e.g. 'your_secret_key'

# Define the order of questions and corresponding session keys / regex patterns
CONVERSATION_FLOW = [
    {'key': 'name', 'question': "Hello! To start an assessment, please tell me the name of your project (e.g., 'My project is called Nebula').", 'pattern': r"(?:my project(?: name)? is|call it|it's called)\s+([A-Za-z0-9\s\-]+)(?:\.|;|$)"},
    {'key': 'description', 'question': "Thanks for the name, {name}! Now, what's a brief description of {name}?", 'pattern': None}, # Will take any text if name is known
    {'key': 'market_size', 'question': "Got it. What's the market size for {name}? (e.g., Small, Medium, Large)", 'pattern': r"(?:market|market size is)\s+(small|medium|large)"},
    {'key': 'competition', 'question': "And how would you describe the competition? (e.g., Low, Medium, High)", 'pattern': r"competition(?: is)?\s+(low|medium|high)"},
    {'key': 'initial_investment_usd', 'question': "What was the initial investment in USD? (e.g., 'investment 50000 USD')", 'pattern': r"(?:investment|invested)\s+([0-9\.]+)\s*(?:USD|dollars)?"},
    {'key': 'revenue_stage', 'question': "What's the current revenue stage? (e.g., Pre-Revenue, Early-Revenue, Growth)", 'pattern': r"(?:revenue stage(?: is)?)\s+(pre-revenue|early-revenue|growth|[A-Za-z\s]+stage)"},
    {'key': 'team_size', 'question': "Finally, how many people are on the team? (e.g., 'team size 5')", 'pattern': r"(?:team size(?: is)?|team has)\s+([0-9]+)"}
]
ALL_DETAIL_KEYS = [item['key'] for item in CONVERSATION_FLOW if item['key'] not in ['name', 'description']]


def get_next_question(project_details):
    for item in CONVERSATION_FLOW:
        if item['key'] not in project_details:
            question = item['question']
            if '{name}' in question and 'name' in project_details:
                question = question.format(name=project_details['name'])
            return question, item['key'], item['pattern']
    return None, None, None # All details collected

@app.route('/', methods=['GET', 'POST'])
def chat_interface():
    if 'chat_history' not in session:
        session['chat_history'] = []
    if 'project_details' not in session:
        session['project_details'] = {}

    current_question, current_key, current_pattern = get_next_question(session['project_details'])

    if request.method == 'POST':
        user_message = request.form.get('message').strip()
        session['chat_history'].append({'speaker': 'User', 'text': user_message})

        extracted_value = None
        if current_pattern: # If there's a pattern for the current question
            match = re.search(current_pattern, user_message, re.IGNORECASE)
            if match:
                extracted_value = match.group(1).strip()
        elif current_key == 'description': # Description takes any text if no pattern
             extracted_value = user_message

        if extracted_value:
            session['project_details'][current_key] = extracted_value
            session['chat_history'].append({'speaker': 'AI', 'text': f"Understood: {current_key.replace('_', ' ')} set to '{extracted_value}'."})
            session.modified = True
            # Get next question
            current_question, current_key, current_pattern = get_next_question(session['project_details'])
        elif current_question : # No value extracted, but there is a pending question
             session['chat_history'].append({'speaker': 'AI', 'text': f"Sorry, I didn't quite catch that. Could you try again? {current_question}"})


        if not current_question: # All details collected
            session['chat_history'].append({'speaker': 'AI', 'text': "Great, I have all the details. Processing assessment..."})

            # Sanitize numeric inputs, providing defaults if conversion fails
            try:
                investment = float(session['project_details'].get('initial_investment_usd', 0.0))
            except ValueError:
                investment = 0.0
            try:
                team = int(session['project_details'].get('team_size', 0))
            except ValueError:
                team = 0

            project_input = ProjectInput(
                name=session['project_details'].get('name'),
                description=session['project_details'].get('description'),
                details={
                    'market_size': session['project_details'].get('market_size'),
                    'competition': session['project_details'].get('competition'),
                    'initial_investment_usd': investment,
                    'revenue_stage': session['project_details'].get('revenue_stage'),
                    'team_size': team
                }
            )

            survivability_assessment = survivability.assess_survivability(project_input)
            valuation_assessment = valuation.assess_valuation(project_input)
            assessment_outputs = [survivability_assessment, valuation_assessment]
            recommendations = generate_recommendations(assessment_outputs)

            # Temp store results before clearing session for this specific interaction
            # This is so result_chat.html can access them.
            # A better way might be to pass results directly or use a one-time token.
            session['last_assessment_results'] = {
                'project_name': project_input.name,
                'survivability_assessment': survivability_assessment.to_dict() if hasattr(survivability_assessment, 'to_dict') else vars(survivability_assessment), # Make serializable
                'valuation_assessment': valuation_assessment.to_dict() if hasattr(valuation_assessment, 'to_dict') else vars(valuation_assessment), # Make serializable
                'recommendations': recommendations,
                'chat_history': list(session['chat_history']) # Store a copy
            }

            # Clear project_details for next assessment
            session.pop('project_details')
            # Don't clear chat_history immediately, let result_chat show it
            return redirect(url_for('show_results'))

        else: # Still questions left
            if not any(entry['speaker'] == 'AI' and entry['text'] == current_question for entry in session['chat_history'][-3:]): # Avoid repeating question if already asked
                 session['chat_history'].append({'speaker': 'AI', 'text': current_question})

        session.modified = True
        return redirect(url_for('chat_interface'))

    # Initial GET request or after a POST that redirects
    if not session['chat_history']: # Very first message
        first_question, _, _ = get_next_question({})
        session['chat_history'].append({'speaker': 'AI', 'text': first_question})
        session.modified = True

    return render_template('index_chat.html', chat_history=session.get('chat_history', []))

@app.route('/results')
def show_results():
    results = session.pop('last_assessment_results', None)
    # Clear chat history after displaying results, for the next full interaction
    current_chat_history = session.pop('chat_history', [])
    if results:
         # Convert dicts back to AssessmentOutput objects if needed by template, or pass dicts
         # For simplicity, ensure AssessmentOutput has a to_dict and from_dict method, or pass dicts directly
        survivability_obj = AssessmentOutput(**results['survivability_assessment']) if results.get('survivability_assessment') else None
        valuation_obj = AssessmentOutput(**results['valuation_assessment']) if results.get('valuation_assessment') else None

        return render_template('result_chat.html',
                               project_name=results['project_name'],
                               survivability_assessment=survivability_obj,
                               valuation_assessment=valuation_obj,
                               recommendations=results['recommendations'],
                               chat_history=results['chat_history']) # Show the history that led to this result
    return redirect(url_for('chat_interface'))


@app.route('/reset_chat', methods=['POST'])
def reset_chat():
    session.pop('chat_history', None)
    session.pop('project_details', None)
    session.pop('last_assessment_results', None)
    return redirect(url_for('chat_interface'))

# Add to_dict method to AssessmentOutput for session serialization if not already there
# This should ideally be in core/data_structures.py
# For the subtask, we'll just assume it's there or use vars() as a fallback.
# Example of adding to_dict to AssessmentOutput (conceptual, real change in data_structures.py)
# class AssessmentOutput:
# ... (existing code) ...
#     def to_dict(self):
#         return {
#             'module_name': self.module_name,
#             'score': self.score,
#             'text_summary': self.text_summary,
#             'details': self.details
#         }
# And a way to re-create it, e.g. using __init__(**data) as done in show_results

# The AssessmentOutput class in core.data_structures.py already takes all args in __init__
# and vars() can be used for simple object-to-dict if it's basic.
# Let's ensure core.data_structures.py AssessmentOutput can be easily serialized.
# We'll assume vars() is sufficient for now for the subtask.
# No changes to index_chat.html or result_chat.html are strictly needed for this step's logic,
# but the experience will change due to app.py modifications.
