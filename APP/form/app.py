from flask import Flask, render_template, request, send_file
import csv
import subprocess
import os

app = Flask(__name__)

# Load Wilaya data
def load_wilaya_data():
    with open(r'C:\Users\k_ben\OneDrive\Desktop\form\static\data\wilayas.csv', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        wilayas = {row['ID']: row['Name_Wilaya'] for row in reader}
    return wilayas

# Load Daira data
def load_daira_data():
    with open(r'C:\Users\k_ben\OneDrive\Desktop\form\static\data\dairas.csv', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        dairas = {row['ID']: row['Name_Daira'] for row in reader}
    return dairas

# Load Baladia data
def load_baladia_data():
    with open(r'C:\Users\k_ben\OneDrive\Desktop\form\static\data\baladias.csv', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        baladias = {row['ID']: row['Name_Baladia'] for row in reader}
    return baladias

@app.route('/')
def form():
    wilayas = load_wilaya_data()
    dairas = load_daira_data()
    baladias = load_baladia_data()
    return render_template('form.html', wilayas=wilayas, dairas=dairas, baladias=baladias)

@app.route('/', methods=['POST'])
def form_post():
    # Extract form data
    form_data = {
        'wilaya': request.form['wilaya'],
        'daira': request.form['daira'],
        'baladia': request.form['baladia'],
        'issuedate': request.form['date1'],
        'numbers': request.form['number1'],
        'name': request.form['text4'],
        'birthdate': request.form['date2'],
        'address': request.form['text7'],
        'cardnumber': request.form['number2'],
        'cardissuedate': request.form['date3'],
        'cause': request.form['select1']
    }

    # Read and replace variables in LaTeX template
    with open(r'C:\Users\k_ben\OneDrive\Desktop\form\شهادة إثبات معلومات.tex', 'r', encoding='utf-8') as file:
        filedata = file.read()

    # Function to escape LaTeX special characters
    def escape_latex(text):
        return text.replace('%', '\\%').replace('&', '\\&').replace('_', '\\_').replace('#', '\\#').replace('{', '\\{').replace('}', '\\}')

    # Replacements for the LaTeX template
    replacements = {
        r'\newcommand{\wilaya}{تيارت}': rf'\newcommand{{\wilaya}}{{{escape_latex(form_data["wilaya"])}}}',
        r'\newcommand{\daira}{تيارت}': rf'\newcommand{{\daira}}{{{escape_latex(form_data["daira"])}}}',
        r'\newcommand{\baladia}{تيارت}': rf'\newcommand{{\baladia}}{{{escape_latex(form_data["baladia"])}}}',
        r'\newcommand{\issuedate}{\englishnumbers{2024/06/23}}': rf'\newcommand{{\issuedate}}{{{escape_latex(form_data["issuedate"])}}}',
        r'\newcommand{\numbers}{\englishnumbers{5}}': rf'\newcommand{{\numbers}}{{{escape_latex(form_data["numbers"])}}}',
        r'\newcommand{\name}{بن زهرة كريمة}': rf'\newcommand{{\name}}{{{escape_latex(form_data["name"])}}}',
        r'\newcommand{\birthdate}{\englishnumbers{2002/01/18}}': rf'\newcommand{{\birthdate}}{{{escape_latex(form_data["birthdate"])}}}',
        r'\newcommand{\address}{حي التفاح 2}': rf'\newcommand{{\address}}{{{escape_latex(form_data["address"])}}}',
        r'\newcommand{\cardnumber}{\englishnumbers{2018131514}}': rf'\newcommand{{\cardnumber}}{{{escape_latex(form_data["cardnumber"])}}}',
        r'\newcommand{\cardissuedate}{\englishnumbers{2018/01/18}}': rf'\newcommand{{\cardissuedate}}{{{escape_latex(form_data["cardissuedate"])}}}',
        r'\newcommand{\cause}{انتهاء الصلاحية}': rf'\newcommand{{\cause}}{{{escape_latex(form_data["cause"])}}}',
    }

    for key, value in replacements.items():
        filedata = filedata.replace(key, value)

    filled_tex_path = r'C:\Users\k_ben\OneDrive\Desktop\form\document_filled_2.tex'
    with open(filled_tex_path, 'w', encoding='utf-8') as file:
        file.write(filedata)

    # Compile the LaTeX document
    output_dir = r'C:\Users\k_ben\OneDrive\Desktop\form'
    result = subprocess.run(
        ['xelatex', '-output-directory', output_dir, filled_tex_path],
        capture_output=True,
        text=True
    )

    # Debugging information
    print(result.stdout)  # Print standard output
    print(result.stderr)  # Print standard error

    # Check if the PDF was created
    pdf_file = os.path.join(output_dir, 'document_filled_2.pdf')
    if not os.path.exists(pdf_file):
        log_file_path = os.path.join(output_dir, 'latex_error.log')
        with open(log_file_path, 'w') as log_file:
            log_file.write(result.stdout)
            log_file.write(result.stderr)
        return 'An error occurred while generating the PDF. Check latex_error.log for details.'

    return 'Form submitted and LaTeX document generated successfully. <a href="/download">Download PDF</a>'

@app.route('/download')
def download():
    return send_file(r'C:\Users\k_ben\OneDrive\Desktop\form\document_filled_2.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
