from flask import Flask, render_template, request
import PyPDF2
import os
import sqlite3
from skills_db import SKILLS

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

    # Extract text from PDF
    def extract_text(file_path):
        text = ""
            with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                            for page in reader.pages:
                                        page_text = page.extract_text()
                                                    if page_text:
                                                                    text += page_text
                                                                        return text

                                                                        # Extract skills
                                                                        def extract_skills(text):
                                                                            found_skills = []
                                                                                for skill in SKILLS:
                                                                                        if skill.lower() in text.lower():
                                                                                                    found_skills.append(skill)
                                                                                                        return found_skills

                                                                                                        # Career suggestion
                                                                                                        def suggest_career(skills):
                                                                                                            if "Python" in skills:
                                                                                                                    return "Software Developer / Data Scientist"
                                                                                                                        elif "HTML" in skills:
                                                                                                                                return "Frontend Developer"
                                                                                                                                    elif "Excel" in skills:
                                                                                                                                            return "Data Analyst"
                                                                                                                                                else:
                                                                                                                                                        return "General Career Path"

                                                                                                                                                        # Improvement tips
                                                                                                                                                        def improvement_tips(skills):
                                                                                                                                                            tips = []
                                                                                                                                                                if "Python" not in skills:
                                                                                                                                                                        tips.append("Learn Python for better opportunities.")
                                                                                                                                                                            if "SQL" not in skills:
                                                                                                                                                                                    tips.append("Add SQL to your skillset.")
                                                                                                                                                                                        if "Communication" not in skills:
                                                                                                                                                                                                tips.append("Improve communication skills.")
                                                                                                                                                                                                    return tips

                                                                                                                                                                                                    @app.route('/', methods=['GET', 'POST'])
                                                                                                                                                                                                    def index():
                                                                                                                                                                                                        if request.method == 'POST':
                                                                                                                                                                                                                file = request.files['resume']

                                                                                                                                                                                                                        # Save file
                                                                                                                                                                                                                                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                                                                                                                                                                                                                                        file.save(filepath)

                                                                                                                                                                                                                                                # Process resume
                                                                                                                                                                                                                                                        text = extract_text(filepath)
                                                                                                                                                                                                                                                                skills = extract_skills(text)
                                                                                                                                                                                                                                                                        career = suggest_career(skills)
                                                                                                                                                                                                                                                                                tips = improvement_tips(skills)

                                                                                                                                                                                                                                                                                        # Database (Render-safe)
                                                                                                                                                                                                                                                                                                conn = sqlite3.connect('/tmp/database.db')
                                                                                                                                                                                                                                                                                                        cursor = conn.cursor()

                                                                                                                                                                                                                                                                                                                cursor.execute('''
                                                                                                                                                                                                                                                                                                                        CREATE TABLE IF NOT EXISTS resumes (
                                                                                                                                                                                                                                                                                                                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                                                                                                                                                                                                                                                                                                filename TEXT,
                                                                                                                                                                                                                                                                                                                                                            skills TEXT
                                                                                                                                                                                                                                                                                                                                                                    )
                                                                                                                                                                                                                                                                                                                                                                            ''')

                                                                                                                                                                                                                                                                                                                                                                                    cursor.execute(
                                                                                                                                                                                                                                                                                                                                                                                                "INSERT INTO resumes (filename, skills) VALUES (?, ?)",
                                                                                                                                                                                                                                                                                                                                                                                                            (file.filename, ",".join(skills))
                                                                                                                                                                                                                                                                                                                                                                                                                    )

                                                                                                                                                                                                                                                                                                                                                                                                                            conn.commit()
                                                                                                                                                                                                                                                                                                                                                                                                                                    conn.close()

                                                                                                                                                                                                                                                                                                                                                                                                                                            return render_template(
                                                                                                                                                                                                                                                                                                                                                                                                                                                        'result.html',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    skills=skills,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                career=career,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            tips=tips
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    )

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        return render_template('index.html')

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        # Required for Render deployment
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        if __name__ == '__main__':
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))