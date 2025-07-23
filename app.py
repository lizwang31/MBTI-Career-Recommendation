from flask import Flask, render_template, request, redirect, url_for, session
import json
import subprocess
import os
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure random key in production

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

# Load questionnaire
def load_questions():
    with open('questions.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Calculate MBTI type
def calculate_mbti(answers, questions):
    # Count scores for each dimension (both sides)
    dimensions = {
        'E': 0, 'I': 0,
        'S': 0, 'N': 0,
        'T': 0, 'F': 0,
        'J': 0, 'P': 0
    }
    for idx, answer in enumerate(answers):
        q = questions[idx]
        dim = q['dimension']
        pos = q['positive']
        score = int(answer)
        if pos:
            dimensions[dim[0]] += score
            dimensions[dim[1]] += 6 - score
        else:
            dimensions[dim[0]] += 6 - score
            dimensions[dim[1]] += score
    # Determine MBTI type by higher score in each dimension
    mbti = ''
    mbti += 'E' if dimensions['E'] >= dimensions['I'] else 'I'
    mbti += 'S' if dimensions['S'] >= dimensions['N'] else 'N'
    mbti += 'T' if dimensions['T'] >= dimensions['F'] else 'F'
    mbti += 'J' if dimensions['J'] >= dimensions['P'] else 'P'
    return mbti

# Call Prolog to get career recommendations
def get_career_recommendation(mbti_type):
    query = f"findall(career('{mbti_type}',Job,Reason), career('{mbti_type}',Job,Reason), Careers), write(Careers), halt."
    try:
        result = subprocess.run(
            ['swipl', '-q', '-s', 'mbti_rules.pl', '-g', query],
            capture_output=True, text=True, timeout=5
        )
        output = result.stdout.strip()
        # Parse Prolog output: [career('ENFP','Marketing Manager','Creative'), ...] or [career(ENFP,Marketing Manager,Creative), ...]
        pattern = r"career\([^,]+,\s*'?([^,'\)]*)'?\s*,\s*'?([^,'\)]*)'?\s*\)"
        matches = re.findall(pattern, output)
        careers = [{'title': m[0], 'desc': m[1]} for m in matches]
        if not careers:
            return [{'title': 'No recommendation', 'desc': ''}]
        return careers
    except Exception as e:
        print('Prolog error:', e)
        return [{'title': 'Prolog error', 'desc': ''}]

@app.route('/', methods=['GET', 'POST'])
def questionnaire():
    questions = load_questions()
    last_result = None
    saved_answers = session.get('answers')
    if 'mbti' in session and 'careers' in session:
        last_result = {'mbti': session['mbti'], 'careers': session['careers']}
    if request.method == 'POST':
        answers = [request.form.get(f"q{i}") for i in range(len(questions))]
        if None in answers:
            return render_template('questionnaire.html', questions=questions, error='Please complete all questions', last_result=last_result, saved_answers=answers)
        mbti = calculate_mbti(answers, questions)
        careers = get_career_recommendation(mbti)
        session['mbti'] = mbti
        session['careers'] = careers
        session['answers'] = answers
        return render_template('result.html', mbti=mbti, careers=careers, description=descriptions.get(mbti, "No description available."))
    return render_template('questionnaire.html', questions=questions, last_result=last_result, saved_answers=saved_answers)

@app.route('/restart')
def restart():
    session.clear()
    return redirect(url_for('questionnaire'))

if __name__ == '__main__':
    app.run(debug=True) 