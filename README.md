# Resume Analyzer - Optimized Version

A streamlined resume analyzer that extracts and displays skills, work experiences, and languages from Word documents.

## Features

- **Skills Extraction**: Displays all skills exclusively mentioned in the resume
- **Work Experience**: Shows detailed work experience with job titles, companies, durations, and descriptions
- **Language Detection**: Identifies and displays languages mentioned in the resume
- **Case-Insensitive Filtering**: Search for specific skills with case-insensitive keyword matching
- **Minimal Code**: Optimized for efficiency with reduced line count

## Usage

1. Run the application: `python app.py`
2. Upload a Word document (.doc or .docx)
3. Optionally enter keywords in the filter field (comma-separated)
4. View extracted information:
   - Languages found in the resume
   - Work experience details
   - Matching skills (if filter applied)
   - All skills mentioned in the resume

## Requirements

- Flask
- docx2txt
- Python 3.6+

## Installation

```bash
pip install flask docx2txt
python app.py
```

Access the application at: http://127.0.0.1:5000 