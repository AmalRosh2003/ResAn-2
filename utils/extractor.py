import docx2txt
from typing import Dict, List
import re
import os

def extract_text_from_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf':
        try:
            import PyPDF2
            with open(path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                return "\n".join(page.extract_text() for page in reader.pages)
        except ImportError:
            try:
                exec("import pdfplumber")
                pdfplumber = eval("pdfplumber")
                with pdfplumber.open(path) as pdf:
                    return "\n".join(page.extract_text() for page in pdf.pages)
            except (ImportError, NameError):
                raise Exception("PDF processing not available. Install PyPDF2 or pdfplumber.")
    else: return docx2txt.process(path)

LANGUAGES = ['english', 'spanish', 'french', 'german', 'italian', 'portuguese', 'russian', 'chinese', 'japanese', 'korean', 'arabic', 'hindi', 'dutch', 'swedish', 'norwegian', 'danish', 'finnish', 'polish', 'turkish', 'greek', 'hebrew', 'thai', 'vietnamese', 'indonesian', 'malay', 'filipino', 'urdu', 'bengali', 'tamil', 'telugu', 'marathi', 'gujarati', 'kannada', 'malayalam', 'punjabi', 'persian', 'farsi', 'swahili', 'yoruba', 'zulu', 'amharic', 'somali', 'hausa', 'igbo', 'xhosa', 'afrikaans', 'catalan', 'basque', 'galician', 'welsh', 'irish', 'scottish', 'icelandic', 'estonian', 'latvian', 'lithuanian', 'hungarian', 'romanian', 'bulgarian', 'croatian', 'serbian', 'slovenian', 'slovak', 'czech', 'ukrainian', 'belarusian', 'kazakh', 'uzbek', 'kyrgyz', 'tajik', 'turkmen', 'mongolian', 'tibetan', 'nepali', 'sinhala', 'burmese', 'lao', 'khmer', 'malagasy', 'maori', 'hawaiian', 'samoan', 'tongan', 'fijian']
TECHNICAL_SKILLS = ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'perl', 'bash', 'powershell', 'sql', 'html', 'css', 'sass', 'scss', 'less', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'laravel', 'asp.net', 'jquery', 'bootstrap', 'tailwind', 'material-ui', 'ant design', 'redux', 'vuex', 'mobx', 'graphql', 'rest api', 'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle', 'sql server', 'mariadb', 'cassandra', 'elasticsearch', 'dynamodb', 'firebase', 'supabase', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab', 'github', 'bitbucket', 'terraform', 'ansible', 'chef', 'puppet', 'nginx', 'apache', 'linux', 'ubuntu', 'centos', 'debian', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly', 'jupyter', 'spark', 'hadoop', 'kafka', 'airflow', 'tableau', 'power bi', 'excel', 'r studio', 'react native', 'flutter', 'xamarin', 'ionic', 'cordova', 'android studio', 'xcode', 'swiftui', 'kotlin android', 'git', 'svn', 'mercurial', 'webpack', 'babel', 'eslint', 'prettier', 'jest', 'mocha', 'cypress', 'selenium', 'postman', 'swagger', 'oauth', 'jwt', 'oauth2', 'ldap', 'saml', 'oauth2.0', 'agile', 'scrum', 'kanban', 'waterfall', 'devops', 'ci/cd', 'tdd', 'bdd', 'lean', 'six sigma', 'vscode', 'intellij', 'eclipse', 'vim', 'emacs', 'sublime', 'atom', 'notepad++', 'word', 'excel', 'powerpoint', 'outlook', 'teams', 'slack', 'zoom', 'jira', 'confluence', 'trello', 'asana', 'monday.com']

def extract_section(text: str, start_keywords: List[str], end_keywords: List[str]) -> str:
    lines, in_section, content = text.split('\n'), False, []
    for line in lines:
        line_lower = line.lower().strip()
        if any(k in line_lower for k in start_keywords): in_section = True; continue
        if in_section and any(k in line_lower for k in end_keywords): break
        if in_section and line.strip(): content.append(line.strip())
    return ' '.join(content)

def extract_experience_precise(text: str) -> List[Dict]:
    experience_text = extract_section(text, ['experience', 'work experience', 'employment', 'professional experience'], ['education', 'skills', 'languages'])
    if not experience_text.strip(): return []
    experiences, lines, current_job = [], experience_text.split('\n'), {}
    for line in lines:
        line = line.strip()
        if not line: continue
        if re.search(r'(senior|junior|lead|principal|staff|associate|director|manager|engineer|developer|analyst|specialist|consultant)', line.lower()):
            if current_job: experiences.append(current_job)
            current_job = {'title': line, 'company': '', 'duration': '', 'description': []}
        elif re.search(r'(inc|corp|llc|ltd|company|co\.|technologies|solutions|systems)', line.lower()) or line.isupper():
            if current_job: current_job['company'] = line
        elif re.search(r'\d{4}[-–]\d{4}|\d{4}\s*[-–]\s*present|\d{4}\s*[-–]\s*now|\d{4}\s*[-–]\s*current', line, re.IGNORECASE):
            if current_job: current_job['duration'] = line
        elif current_job and not any(k in line.lower() for k in ['experience', 'work', 'employment']):
            current_job['description'].append(line)
    if current_job: experiences.append(current_job)
    return experiences

def extract_email(text: str) -> str:
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    for line in text.split('\n'):
        line_lower = line.lower().strip()
        if any(skip in line_lower for skip in ['fax', 'ext', 'extension', 'gpa', 'gpa:', 'score']): continue
        match = re.search(email_pattern, line)
        if match: return match.group().strip()
    return "Email not found"

def extract_education(text: str) -> List[Dict]:
    education_text = extract_section(text, ['education', 'academic', 'qualifications'], ['experience', 'skills', 'languages', 'projects'])
    if not education_text.strip(): return []
    education_list, lines, current_edu = [], education_text.split('\n'), {}
    for line in lines:
        line = line.strip()
        if not line: continue
        if re.search(r'(bachelor|master|phd|doctorate|diploma|certificate|associate|b\.|m\.|ph\.d)', line.lower()):
            if current_edu: education_list.append(current_edu)
            current_edu = {'degree': line, 'institution': '', 'year': '', 'gpa': ''}
        elif re.search(r'(university|college|institute|school|academy)', line.lower()) or line.isupper():
            if current_edu: current_edu['institution'] = line
        elif re.search(r'\b(19|20)\d{2}\b', line):
            if current_edu: current_edu['year'] = line
        elif re.search(r'gpa|grade|score', line.lower()) and re.search(r'\d+\.?\d*', line):
            if current_edu: current_edu['gpa'] = line
    if current_edu: education_list.append(current_edu)
    return education_list

def extract_qualifications(text: str) -> List[str]:
    edu_keywords = ['education', 'educational background', 'qualifications', 'educational qualifications', 'educational qualification']
    lines, qualifications, in_edu_section = text.split('\n'), [], False
    for line in lines:
        line_lower = line.lower().strip()
        if any(k in line_lower for k in edu_keywords): in_edu_section = True; continue
        if in_edu_section and any(k in line_lower for k in ['experience', 'skills', 'languages', 'projects']): break
        if in_edu_section and line.strip(): qualifications.append(line.strip())
    return qualifications

def extract_phone(text: str) -> str:
    phone_patterns = [r'\+?1?\s*\(?[0-9]{3}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{4}', r'\+?[0-9]{1,4}[\s\-]?[0-9]{1,4}[\s\-]?[0-9]{1,4}[\s\-]?[0-9]{1,4}', r'\(?[0-9]{3}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{4}', r'[0-9]{3}[\s\-]?[0-9]{3}[\s\-]?[0-9]{4}']
    for line in text.split('\n'):
        line_lower = line.lower().strip()
        if any(skip in line_lower for skip in ['fax', 'ext', 'extension', 'gpa', 'gpa:', 'score']): continue
        for pattern in phone_patterns:
            match = re.search(pattern, line)
            if match: return match.group().strip()
    return "Phone number not found"

def extract_skills_from_headings(text: str) -> Dict[str, List[str]]:
    skills_headings = ['skills', 'additional skills', 'other skills', 'technical skills', 'core skills', 'key skills', 'professional skills', 'soft skills', 'hard skills', 'computer skills', 'programming skills', 'language skills', 'qualities', 'personal qualities', 'characteristics', 'attributes', 'competencies', 'expertise', 'proficiencies', 'capabilities']
    lines, skills_by_section, current_section, current_skills = text.split('\n'), {}, None, []
    for line in lines:
        line = line.strip()
        if not line: continue
        line_lower = line.lower()
        is_skills_heading = any(heading in line_lower for heading in skills_headings)
        if is_skills_heading:
            if current_section and current_skills: skills_by_section[current_section] = current_skills
            current_section, current_skills = line, []
            continue
        if current_section:
            if not any(skip in line_lower for skip in ['experience', 'education', 'contact', 'projects', 'certifications', 'awards', 'references']):
                skill_items = re.split(r'[,;•\-\n]', line)
                for item in skill_items:
                    skill = item.strip()
                    if (len(skill) > 2 and not any(skip in skill.lower() for skip in ['years', 'experience', 'proficient', 'expert', 'intermediate', 'beginner', 'level', 'advanced']) and not skill.lower() in ['and', 'or', 'with', 'using', 'via', 'through', 'the', 'a', 'an', 'of', 'in', 'on', 'at', 'to', 'for']):
                        current_skills.append(skill)
    if current_section and current_skills: skills_by_section[current_section] = current_skills
    return skills_by_section

def extract_skills_from_text(text: str) -> List[str]:
    skills_by_section = extract_skills_from_headings(text)
    all_skills = []
    for section, skills in skills_by_section.items(): all_skills.extend(skills)
    return list(set(all_skills))

def extract_skills_with_context(text: str) -> Dict[str, List[str]]:
    skills_by_section, skills_context = extract_skills_from_headings(text), {}
    for section, skills in skills_by_section.items():
        for skill in skills:
            if skill not in skills_context: skills_context[skill] = []
            skills_context[skill].append(section)
    return skills_context

def extract_info(path: str, filter_keywords: str = '') -> Dict:
    try:
        text = extract_text_from_file(path)
        if not text.strip(): raise ValueError("Empty document")
        phone, email = extract_phone(text), extract_email(text)
        education, qualifications = extract_education(text), extract_qualifications(text)
        skills_by_section = extract_skills_from_headings(text)
        skills, skills_with_context = extract_skills_from_text(text), extract_skills_with_context(text)
        experiences = extract_experience_precise(text)
        languages = []
        in_lang = False
        for line in text.split('\n'):
            line_lower = line.lower().strip()
            if any(k in line_lower for k in ['languages', 'language skills']): in_lang = True; continue
            if in_lang and any(k in line_lower for k in ['education', 'skills', 'experience']): break
            if in_lang and line.strip(): languages.extend([l.strip() for l in re.split(r'[,;•\-\n]', line) if len(l.strip()) > 2])
        filtered_skills, missing_keywords, found_keywords = [], [], []
        if filter_keywords:
            keywords = [k.strip().lower() for k in filter_keywords.split(',') if k.strip()]
            text_lower = text.lower()
            for keyword in keywords:
                if keyword in text_lower:
                    found_keywords.append(keyword)
                    for skill in skills:
                        if keyword in skill.lower() and skill not in filtered_skills: filtered_skills.append(skill)
                else: missing_keywords.append(keyword)
        return {"phone": phone, "email": email, "education": education, "qualifications": qualifications, "skills": list(set(skills)), "skills_by_section": skills_by_section, "filtered_skills": filtered_skills, "missing_keywords": missing_keywords, "found_keywords": found_keywords, "experiences": experiences, "languages": list(set(languages)), "total_skills": len(set(skills)), "filter_keywords": filter_keywords, "skills_with_context": skills_with_context}
    except Exception as e: raise Exception(f"Error processing resume: {str(e)}") 