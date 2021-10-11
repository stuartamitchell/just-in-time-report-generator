import click
import os
import pandas as pd
from reports import Reports

@click.command()
@click.argument('xlsx_file')
@click.option('--dir', '-d', help='The directory you wish to save the output')
def main(xlsx_file, dir):
    reports = Reports(xlsx_file)
    
    if dir:
        output_file = os.path.join(os.path.abspath(dir), 'reports.xlsx')
    else:
        output_file = os.path.join(os.path.dirname(xlsx_file), 'reports.xlsx')  
    
    student_names = [student.fullname for student in reports.students]

    data = {'fullname': student_names, 'report': reports.reports}
    df = pd.DataFrame(data=data)
    df.to_excel(output_file)

if __name__ == '__main__':
    main()
