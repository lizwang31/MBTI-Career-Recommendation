# MBTI-Career Recommendation System

A web-based career recommendation system based on MBTI personality types. Users complete a 20-question Likert-scale questionnaire, receive their MBTI type, and get personalized career suggestions powered by Prolog rules.

## Features
- Interactive MBTI questionnaire (Likert scale, 1–5)
- Automatic MBTI type calculation with explanation
- Career recommendations with reasons, powered by Prolog (`mbti_rules.pl`)
- Modern, responsive UI (Bootstrap 5)
- Session-based result saving and restart functionality

## Tech Stack
- **Backend:** Python 3, Flask
- **Frontend:** HTML, Bootstrap 5, Jinja2
- **Logic Engine:** SWI-Prolog

## File Structure
```
MBTI-Career Recommendation/
├── app.py                  # Flask backend & MBTI logic
├── mbti_rules.pl           # Prolog rules for career recommendation
├── questions.json          # MBTI questionnaire data
├── templates/
│   ├── questionnaire.html  # Questionnaire page
│   └── result.html         # Result page
└── README.md               # Project documentation
```

## Setup & Installation
1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd MBTI-Career\ Recommendation
   ```
2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install flask
   ```
4. **Install SWI-Prolog**
   - [Download and install SWI-Prolog](https://www.swi-prolog.org/Download.html) for your OS.
   - Ensure `swipl` is available in your PATH.

## Usage
1. **Start the Flask app**
   ```bash
   python app.py
   ```
2. **Open your browser and visit**
   [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
3. **Fill out the questionnaire and submit**
   - Your MBTI type and recommended careers will be displayed.
   - You can return to the questionnaire, and your previous answers/results will be saved until you click "Restart".

## Prolog Integration
- Career recommendations are defined in `mbti_rules.pl` using the format:
  ```prolog
  career('ENFP', 'Marketing Manager', 'Creative, energetic, and skilled at communication.').
  career('ENFP', 'Public Relations Specialist', 'Excellent with people and quick thinkers.').
  ```
- You can add or modify rules for all 16 MBTI types.
- The Flask backend calls Prolog using `subprocess` and parses the results for display.

## Customization
- **Add/modify questions:** Edit `questions.json`.
- **Add/modify career rules:** Edit `mbti_rules.pl`.
- **Change MBTI descriptions:** Edit the `descriptions` dictionary in `app.py`.

## Credits
- MBTI® is a registered trademark of the Myers-Briggs Company.
- This project is for educational and demonstration purposes only.

---

Feel free to contribute or adapt for your own use! 