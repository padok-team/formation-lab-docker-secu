from flask import Flask, request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if a file's extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files:
            return 'No file part in the request'
        file = request.files['file']
        # If user does not select a file, the browser submits an empty part without a filename.
        if file.filename == '':
            return 'No file selected'
        if file and allowed_file(file.filename):
            # Sanitize the file name
            filename = secure_filename(file.filename)
            # Ensure the upload folder exists
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return f'File "{filename}" successfully uploaded!'
        else:
            return 'File type is not allowed'
    
    # For GET requests, show a simple HTML form
    return '''
    <!doctype html>
    <html>
      <head>
        <title>Upload a File</title>
      </head>
      <body>
        <h1>Upload a File</h1>
        <form method="post" enctype="multipart/form-data">
          <input type="file" name="file">
          <input type="submit" value="Upload">
        </form>
      </body>
    </html>
    '''

if __name__ == '__main__':
    # Run the app on all interfaces so it can be accessed from outside the container
    app.run(debug=True, host='0.0.0.0', port=8080)
