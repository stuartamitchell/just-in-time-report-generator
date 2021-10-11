import os
from flask.helpers import send_from_directory
import pandas as pd
from flask import Flask, request, redirect, url_for 
from flask.templating import render_template
from jitrgen.reports import Reports

def create_app():
    #UPLOAD_FOLDER = './tmp'

    app = Flask(__name__)
    #app.config[UPLOAD_FOLDER] = UPLOAD_FOLDER

    def allowed_file(filename):
        return filename[-5:] == '.xlsx'

    @app.route('/')
    def index():
        return render_template('home.html')

    @app.route('/generate', methods=['POST'])
    def generate():
        xlsx_file = request.files['xlsx_file']

        if xlsx_file and allowed_file(xlsx_file.filename):
            reports = Reports(xlsx_file)

            student_names = [student.fullname for student in reports.students]

            data = {'fullname': student_names, 'report': reports.reports}
            df = pd.DataFrame(data=data)

            uploads = os.path.join(app.root_path, 'tmp')
            reports_file = os.path.join(uploads, 'reports.xlsx')

            df.to_excel(reports_file)

            return 'Reports generated'
        else:
            return redirect('/')
    return app
