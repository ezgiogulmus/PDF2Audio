from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from flask import send_from_directory
from pdfconverter import ListenPDFs, empty_folder

app = Flask(__name__)

MYDIR = os.path.dirname(__file__)
app.config['UPLOAD_FOLDER'] = os.path.join(MYDIR, 'static/uploads/')

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/', methods=['GET', 'POST'])
def pdf():
    if request.method == "POST":
        empty_folder(app.config['UPLOAD_FOLDER'])
        if 'pdf-file' not in request.files:
            flash('No file part.')
            return redirect(request.url)
        pdf_file = request.files['pdf-file']        
        if pdf_file.filename == '':
            flash('Select a file.')
            return redirect(request.url)
        if pdf_file.filename.rsplit('.', 1)[1].lower() != "pdf":
            flash('Only PDF files are accepted.')
            return redirect(request.url)
        else:
            if request.form['first-page'] == "":
                first_page = 1
            else:
                first_page = int(request.form['first-page'])
            if request.form['last-page'] == "":
                last_page = -1
            else:
                last_page = int(request.form['last-page'])
            if last_page > 0 and last_page < first_page:
                flash('Select at least 1 page.')
                return redirect(request.url)
            filename = secure_filename(pdf_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            pdf_file.save(file_path)
            converter = ListenPDFs(file_path, first_page, last_page)
            text_path = converter.get_text()
            if request.form['type'] == 'txt':
                return redirect(url_for('download', filename=os.path.basename(text_path)))
            else:
                mp3 = converter.save_mp3(text_path)
                return redirect(url_for('download', filename=os.path.basename(mp3)))        
    return render_template("index.html")
    
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == "__main__":
    app.run()
