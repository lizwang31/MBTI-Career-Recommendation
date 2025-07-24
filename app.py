# app.py
from flask import Flask, render_template, request, redirect, url_for, session
import json
import subprocess
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure random key in production

# Static descriptions for each MBTI type
descriptions = {
    "ISTJ": "Responsible, reliable, and organized. ISTJs value traditions and prefer clear structures and plans.",
    "ISFJ": "Caring, loyal, and meticulous. ISFJs are devoted helpers who enjoy preserving harmony and supporting others.",
    "INFJ": "Insightful, principled, and reserved. INFJs seek meaning in relationships and ideas, often acting as idealistic advocates.",
    "INTJ": "Strategic, independent, and analytical. INTJs are long-term planners who excel in conceptual thinking and innovation.",
    "ISTP": "Practical, curious, and adaptable. ISTPs are hands-on problem-solvers who enjoy figuring out how things work.",
    "ISFP": "Gentle, spontaneous, and artistic. ISFPs appreciate beauty and personal freedom, often expressing themselves creatively.",
    "INFP": "Idealistic, empathetic, and imaginative. INFPs are driven by values and enjoy exploring human potential and emotions.",
    "INTP": "Curious, logical, and inventive. INTPs are independent thinkers who love solving abstract and theoretical problems.",
    "ESTP": "Energetic, action-oriented, and bold. ESTPs thrive on excitement and tend to live in the present moment.",
    "ESFP": "Fun-loving, outgoing, and spontaneous. ESFPs enjoy being around others and embracing life's pleasures.",
    "ENFP": "Enthusiastic, expressive, and imaginative. ENFPs are passionate about ideas and forming deep connections.",
    "ENTP": "Inventive, witty, and energetic. ENTPs love challenges, exploring possibilities, and debating ideas.",
    "ESTJ": "Efficient, organized, and practical. ESTJs are natural leaders who like order and getting things done.",
    "ESFJ": "Sociable, warm, and caring. ESFJs enjoy helping others and value community and harmony.",
    "ENFJ": "Charismatic, supportive, and visionary. ENFJs are empathetic leaders who inspire and connect with others.",
    "ENTJ": "Confident, strategic, and assertive. ENTJs are natural organizers who thrive in leadership and decision-making."
}

def load_questions():
    with open('questions.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def calculate_mbti(answers, questions):
    # Build a Prolog list of resp(Dimension,Side,Score) terms
    dim_map = {
        'EI': 'e_i',
        'SN': 's_n',
        'TF': 't_f',
        'JP': 'j_p'
    }
    terms = []
    for idx, ans in enumerate(answers):
        q = questions[idx]
        prolog_dim = dim_map[q['dimension']]
        side = q['positive'].lower()             # 'E' or 'I' etc.
        terms.append(f"resp({prolog_dim},{side},{ans})")
    prolog_list = '[' + ','.join(terms) + ']'

    # Call Prolog to compute the MBTI code
    query = f"calculate_mbti({prolog_list},MBTI), write(MBTI), halt."
    result = subprocess.run(
        ['swipl', '-q', '-s', 'mbti_scores.pl', '-g', query],
        capture_output=True, text=True, timeout=5
    )
    return result.stdout.strip()

def get_career_recommendation(mbti_type):
    # Call Prolog to fetch all career/3 facts for this MBTI
    query = (
        f"findall(career('{mbti_type}',Job,Reason), career('{mbti_type}',Job,Reason), L), "
        f"forall(member(career(_,J,R),L), (write(J), write(':!:'), write(R), nl)), halt."
    )
    result = subprocess.run(
        ['swipl', '-q', '-s', 'mbti_rules.pl', '-g', query],
        capture_output=True, text=True, timeout=5
    )
    careers = []
    for line in result.stdout.strip().splitlines():
        if ':!:' in line:
            title, desc = line.split(':!:', 1)
            careers.append({'title': title, 'desc': desc})
    if not careers:
        careers = [{'title': 'No recommendation', 'desc': ''}]
    return careers

@app.route('/', methods=['GET', 'POST'])
def questionnaire():
    questions = load_questions()
    last_result = None
    saved_answers = session.get('answers')
    if 'mbti' in session and 'careers' in session:
        last_result = {'mbti': session['mbti'], 'careers': session['careers']}
    if request.method == 'POST':
        answers = [int(request.form.get(f"q{i}")) for i in range(len(questions))]
        if None in answers:
            return render_template('questionnaire.html',
                                   questions=questions,
                                   error='Please complete all questions',
                                   last_result=last_result,
                                   saved_answers=saved_answers)
        mbti = calculate_mbti(answers, questions)
        careers = get_career_recommendation(mbti)
        session['mbti'] = mbti
        session['careers'] = careers
        session['answers'] = answers
        return render_template('result.html',
                               mbti=mbti,
                               careers=careers,
                               description=descriptions.get(mbti, "No description available."))
    return render_template('questionnaire.html',
                           questions=questions,
                           last_result=last_result,
                           saved_answers=saved_answers)

@app.route('/restart')
def restart():
    session.clear()
    return redirect(url_for('questionnaire'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
