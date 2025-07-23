% mbti_rules.pl
% MBTI-based career recommendation expert system

% Format: career(MBTI, JobTitle, Reason).

career('INTJ', 'Software Architect', 'Strategic and analytical thinkers who excel in complex planning.').
career('INTJ', 'Scientist', 'Enjoy exploring theoretical systems and solving deep problems.').
career('INTJ', 'Data Scientist', 'Logical and independent; thrive in solving complex data problems.').

career('INTP', 'Researcher', 'Curious and logical thinkers; enjoy analyzing ideas.').
career('INTP', 'Software Developer', 'Independent and analytical problem-solvers.').
career('INTP', 'Philosopher', 'Love abstract ideas and deep thinking.').

career('ENTJ', 'Executive', 'Natural leaders who are goal-oriented and decisive.').
career('ENTJ', 'Business Consultant', 'Strategic thinkers who enjoy solving organizational problems.').
career('ENTJ', 'Corporate Lawyer', 'Commanding and logical; thrive in high-stakes environments.').

career('ENTP', 'Entrepreneur', 'Innovative and persuasive; love new ideas and challenge.').
career('ENTP', 'Product Manager', 'Quick-witted with broad vision and execution skills.').
career('ENTP', 'Creative Director', 'Energetic and imaginative, thrive in dynamic work.').

career('INFJ', 'Psychologist', 'Insightful and empathetic; driven to help others grow.').
career('INFJ', 'Writer', 'Value depth and meaning; enjoy expressive work.').
career('INFJ', 'Social Worker', 'Compassionate advocates for people and causes.').

career('INFP', 'Writer', 'Idealistic and expressive; enjoy creative self-expression.').
career('INFP', 'Counselor', 'Empathetic and good at understanding others.').
career('INFP', 'Graphic Designer', 'Creative and independent; express values through design.').

career('ENFJ', 'Teacher', 'Inspiring leaders who help others reach their potential.').
career('ENFJ', 'Human Resources Manager', 'Supportive and organized; strong people skills.').
career('ENFJ', 'Public Speaker', 'Persuasive and expressive communicators.').

career('ENFP', 'Marketing Manager', 'Creative, energetic, and skilled at communication.').
career('ENFP', 'Public Relations Specialist', 'Excellent with people and quick thinkers.').
career('ENFP', 'Journalist', 'Curious and expressive; love storytelling.').

career('ISTJ', 'Accountant', 'Reliable and detail-oriented; thrive in structured roles.').
career('ISTJ', 'Civil Engineer', 'Responsible and pragmatic problem-solvers.').
career('ISTJ', 'Auditor', 'Value accuracy and process consistency.').

career('ISFJ', 'Librarian', 'Meticulous and service-oriented; enjoy quiet, structured environments.').
career('ISFJ', 'Administrative Assistant', 'Organized and detail-focused.').
career('ISFJ', 'Healthcare Worker', 'Reliable and empathetic caregivers.').

career('ESTJ', 'Project Manager', 'Strong organizers who like clear structure and efficiency.').
career('ESTJ', 'Operations Manager', 'Practical leaders who enforce processes.').
career('ESTJ', 'Police Officer', 'Firm and dependable; uphold rules and systems.').

career('ESFJ', 'Teacher', 'Supportive and outgoing; thrive in structured social environments.').
career('ESFJ', 'Nurse', 'Caring and responsible, drawn to helping others.').
career('ESFJ', 'Event Planner', 'Detail-oriented and sociable; enjoy managing logistics.').

career('ISTP', 'Engineer', 'Technical problem-solvers who work well independently.').
career('ISTP', 'Mechanic', 'Hands-on and enjoy troubleshooting systems.').
career('ISTP', 'Pilot', 'Cool-headed and confident in fast-changing environments.').

career('ISFP', 'Artist', 'Sensitive and creative; express through visual or tactile media.').
career('ISFP', 'Chef', 'Practical creatives who enjoy working with their hands.').
career('ISFP', 'Veterinary Technician', 'Gentle and observant; enjoy caring for animals.').

career('ESTP', 'Sales Representative', 'Energetic and persuasive; thrive in fast-paced roles.').
career('ESTP', 'Emergency Medical Technician (EMT)', 'Quick-acting and resilient under pressure.').
career('ESTP', 'Real Estate Agent', 'Bold and sociable; skilled in negotiation.').

career('ESFP', 'Performer', 'Lively and spontaneous; enjoy the spotlight.').
career('ESFP', 'Recreational Therapist', 'Enthusiastic and compassionate; love bringing joy.').
career('ESFP', 'Flight Attendant', 'Energetic and service-oriented; love dynamic environments.').


% Recommend careers for a given MBTI type
recommend(MBTI, Careers) :-
    findall((Job, Reason), career(MBTI, Job, Reason), Careers).
