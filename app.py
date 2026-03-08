from flask import Flask, render_template, request, send_file
import os
from generator import VideoGenerator
from werkzeug.utils import secure_filename
import PyPDF2
from docx import Document

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(file, filename):
    """Extract text from different file formats"""
    file_extension = filename.rsplit('.', 1)[1].lower()
    
    try:
        if file_extension == 'txt':
            return file.read().decode('utf-8')
        
        elif file_extension == 'pdf':
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        
        elif file_extension == 'docx':
            # Save file temporarily for docx processing
            temp_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_' + secure_filename(filename))
            file.save(temp_path)
            
            try:
                doc = Document(temp_path)
                text = ""
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
                return text
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
            
    except Exception as e:
        raise Exception(f"Error reading {file_extension.upper()} file: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_video():
    try:
        if 'file' not in request.files:
            return {'error': 'No file provided'}, 400
        
        file = request.files['file']
        
        if file.filename == '':
            return {'error': 'No file selected'}, 400
        
        if not allowed_file(file.filename):
            return {'error': 'Only .txt, .pdf, and .docx files are allowed'}, 400
        
        # Extract text from uploaded file
        try:
            text = extract_text_from_file(file, file.filename)
            if not text.strip():
                return {'error': 'File is empty or no text could be extracted'}, 400
        except Exception as e:
            return {'error': str(e)}, 400
        
        generator = VideoGenerator()
        video_path = generator.create_video(text)
        
        return {'success': True, 'video_path': video_path}
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    except Exception as e:
        return {'error': str(e)}, 404

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
