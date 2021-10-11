import os
import pandas as pd
import secrets

from flask.helpers import flash, send_from_directory
from flask import Flask, request, redirect 
from flask.templating import render_template
from jitrgen.reports import Reports

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'downloads')
app.secret_key = secrets.token_bytes(16)

def allowed_file(filename):
    return filename[-5:] == '.xlsx'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        xlsx_file = request.files['xlsx_file']

        # first layer of validation
        if xlsx_file and allowed_file(xlsx_file.filename):
            # make sure the correct sheets actually exist
            try:
                setup_sheet = pd.read_excel(xlsx_file, sheet_name='Setup')
                students_sheet = pd.read_excel(xlsx_file, sheet_name='Students')

                reports = Reports(setup_sheet, students_sheet)

                student_names = [student.fullname for student in reports.students]

                data = {'fullname': student_names, 'report': reports.reports}
                df = pd.DataFrame(data=data)
                
                reports_file = os.path.join(app.config['UPLOAD_FOLDER'], 'reports.xlsx')

                df.to_excel(reports_file)

                return render_template('index.html', download_report=True)
            except:
                flash('File must conform to the template')
                return redirect('/')
        else:
            flash('File must be a .xlsx file')
            return redirect('/')
    else:
        return render_template('index.html', report=False)

@app.route('/downloads/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
        
if __name__ == '__main__':
    app.run()