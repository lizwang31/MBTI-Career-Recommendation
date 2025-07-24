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
    # 维度映射：Python维度 -> Prolog维度
    dim_map = {
        'EI': 'e_i',
        'SN': 's_n',
        'TF': 't_f',
        'JP': 'j_p',
    }
    # 维度分数初始化
    scores = {
        'E': 0, 'I': 0,
        'S': 0, 'N': 0,
        'T': 0, 'F': 0,
        'J': 0, 'P': 0
    }
    # 维度两侧映射
    dim_sides = {
        'e_i': ('E', 'I'),
        's_n': ('S', 'N'),
        't_f': ('T', 'F'),
        'j_p': ('J', 'P'),
    }
    for idx, answer in enumerate(answers):
        q = questions[idx]
        qid = q.get('id', idx+1)
        py_dim = q['dimension']
        prolog_dim = dim_map[py_dim]
        pos_side = q['positive'].lower()  # 'E'/'I' -> 'e'/'i'
        user_score = int(answer)
        # 调用 Prolog 计算得分
        prolog_query = f"rule({qid}, {prolog_dim}, {pos_side}, {user_score}, Score), write(Score), halt."
        try:
            result = subprocess.run(
                ['swipl', '-q', '-s', 'mbti_scores.pl', '-g', prolog_query],
                capture_output=True, text=True, timeout=3
            )
            score_str = result.stdout.strip()
            score = int(score_str) if score_str.isdigit() else 0
        except Exception as e:
            print(f"Prolog error on Q{qid}: {e}")
            score = 0
        # 累加到对应维度
        # 判断正向是哪一侧
        left, right = dim_sides[prolog_dim]
        if pos_side == left.lower():
            scores[left] += score
        else:
            scores[right] += score
    # 生成 MBTI 字符串
    mbti = ''
    mbti += 'E' if scores['E'] >= scores['I'] else 'I'
    mbti += 'S' if scores['S'] >= scores['N'] else 'N'
    mbti += 'T' if scores['T'] >= scores['F'] else 'F'
    mbti += 'J' if scores['J'] >= scores['P'] else 'P'
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