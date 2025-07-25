# MBTI-Based Career Recommendation System

This web-based expert system provides career recommendations based on a user’s MBTI personality type. Users complete a structured questionnaire, and the system infers their MBTI type using Prolog logic rules before presenting tailored career suggestions.

---

## 🚀 Project Overview

- **Interactive MBTI Questionnaire**: Users complete a web-based form assessing personality traits.
- **Prolog-Based Inference**: Logical rules in SWI-Prolog compute MBTI types based on submitted responses.
- **Career Recommendation Engine**: Careers are retrieved from a Prolog knowledge base linked to each MBTI type.
- **Flask Web Framework**: Python Flask handles request routing, form submission, and response rendering.
- **Responsive Design**: Clean, responsive UI built using HTML, Bootstrap 5, and Jinja2 templating.

---

## ⚙️ Technology Stack

### Backend

- **Python 3** – Core application logic and API handling.
- **Flask** – Lightweight web framework for routing and server-side rendering.
- **SWI-Prolog** – Inference engine for personality typing and rule-based career matching.

### Frontend

- **HTML + Jinja2** – Dynamic questionnaire and results pages.
- **Bootstrap 5** – Modern responsive styling.
- **Custom CSS** – Minor layout adjustments and theming.

### Data & Logic

- `questions.json` – Question bank used in the MBTI questionnaire.
- `mbti_scores.pl` – Computes MBTI type from questionnaire scores using logical rules.
- `mbti_rules.pl` – Maps MBTI types to associated career options and rationales.

---

## 📂 Project Structure

```
mbti-career-app/
├── app.py                  # Flask application entry point
├── questions.json          # MBTI questionnaire data
├── mbti_scores.pl          # Prolog: MBTI type scoring logic
├── mbti_rules.pl           # Prolog: Career recommendation rules
├── templates/
│   ├── questionnaire.html  # Questionnaire form page
│   └── result.html         # Results display page
└── static/                 # CSS, images, and optional static assets
```

---

## 🚦 Quickstart Guide

### Prerequisites

- Python 3.x  
- [SWI-Prolog](https://www.swi-prolog.org/Download.html) installed  
- pip (Python package manager)

### Installation Steps

```bash
git clone https://github.com/yourusername/mbti-career-app.git
cd mbti-career-app
pip install flask
flask --app app.py run --host=0.0.0.0 --port=5000
```

Then open in browser:  
👉 [http://localhost:5000](http://localhost:5000)

---

## 🔁 System Workflow

1. **User Input**: Users complete a 20-question Likert-scale questionnaire.
2. **Flask Backend**: Parses and structures responses for Prolog.
3. **Prolog Inference**:
   - `mbti_scores.pl` computes four-letter MBTI type from scores.
   - `mbti_rules.pl` returns matching careers with rationales.
4. **Flask Rendering**: Displays results on a styled HTML page.

---

## 📊 MBTI Scoring Logic

- Answers are mapped from 1–5 scale to –2 through +2.
- Responses aligned with the second MBTI pole (I, N, F, P) are scored inversely.
- Each dimension (e.g., E vs. I) is scored independently.
- The final MBTI type reflects the dominant preference in each dimension.

---

## 🔮 Future Enhancements

- Add more career options and rationales per MBTI type.
- Introduce user feedback to refine recommendations.
- Support additional user attributes (e.g., interests, skills).
- Add multilingual support and accessibility features.
- Dockerize for containerized deployment and cloud hosting.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
