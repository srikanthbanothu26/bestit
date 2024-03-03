class Config:
    SECRET_KEY = 'secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    UPLOAD_FOLDERS = {
        'python': {
            'notes': 'upload_python_notes',
            'recordings': 'upload_python_recordings',
            'assignments': 'upload_python_assignments',
            'assessments': 'upload_python_assessments'
        },
        'java': {
            'notes': 'upload_java_notes',
            'recordings': 'upload_java_recordings',
            'assignments': 'upload_java_assignments',
            'assessments': 'upload_java_assessments'
        }
    }

