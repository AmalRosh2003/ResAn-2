from flask import Flask, render_template, request, flash
from utils.extractor import extract_info
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
UPLOAD_FOLDER, ALLOWED_EXTENSIONS = 'resumes', {'pdf', 'docx', 'doc'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    if request.method == 'POST':
        if 'resume' not in request.files:
            flash('No file uploaded')
            return render_template('index.html')
        file = request.files['resume']
        if not file.filename or '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
            flash('Please upload a valid document (.pdf, .doc, or .docx)')
            return render_template('index.html')
        try:
            if not os.path.exists(app.config['UPLOAD_FOLDER']): os.makedirs(app.config['UPLOAD_FOLDER'])
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            data = extract_info(file_path, request.form.get('filter', '').strip())
            os.remove(file_path)
        except Exception as e: flash(f'Error processing file: {str(e)}')
    return render_template('index.html', data=data)

if __name__ == '__main__':
    try: app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
    except KeyboardInterrupt: pass
    except Exception as e: print(f"Error starting server: {e}")
