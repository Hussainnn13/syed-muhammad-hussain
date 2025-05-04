from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import nltk
from nltk.tokenize import sent_tokenize

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

nltk.download('punkt')

def generate_questions(text):
    sentences = sent_tokenize(text)
    questions = []
    for sentence in sentences:
        if "water" in sentence:
            questions.append({
                'question': f"What does the sentence '{sentence}' explain?",
                'options': ["Water evaporates", "Water moves through the cycle", "Water freezes", "Water condenses"],
                'answer': "Water moves through the cycle"
            })
    return questions

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_text():
    text = request.form['text']
    session['quiz_data'] = generate_questions(text)
    session['current_question'] = 0
    session['answers'] = []
    return jsonify({'status': 'success', 'message': 'Quiz generated successfully!'})

@app.route('/next_question', methods=['POST'])
def next_question():
    index = session.get('current_question', 0)
    if index < len(session['quiz_data']):
        question = session['quiz_data'][index]
        session['current_question'] = index + 1
        return jsonify({
            'question': question['question'],
            'options': question['options']
        })
    return jsonify({'status': 'finished'})

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    index = session.get('current_question', 1) - 1
    answer = request.form['answer']
    correct_answer = session['quiz_data'][index]['answer']
    session['answers'].append({
        'question': session['quiz_data'][index]['question'],
        'user_answer': answer,
        'correct_answer': correct_answer,
        'is_correct': answer == correct_answer
    })
    return jsonify({'is_correct': answer == correct_answer, 'correct_answer': correct_answer})

@app.route('/review')
def review():
    return render_template('review.html', answers=session.get('answers', []))

@app.route('/ask_followup', methods=['POST'])
def ask_followup():
    user_question = request.form['question'].lower()
    if 'why' in user_question:
        return jsonify({'response': "This is because water moves through different states and locations in nature."})
    return jsonify({'response': "I don't have a clear answer to that, but I can help with more questions!"})

if __name__ == '__main__':
    app.run(debug=True)
