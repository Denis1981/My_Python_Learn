from flask import Flask, request, render_template, redirect, url_for, flash
import fitz  # PyMuPDF
from docx import Document
from db import create_connection, insert_document, create_table, get_all_documents
from transformers import BertTokenizer, BertForQuestionAnswering, pipeline
import os
import tempfile

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Секретный ключ для флеш-сообщений

# Проверка существования модели и токенизатора
model_path = "./trained_model"
if not os.path.exists(model_path):
    raise EnvironmentError(f"Model path {model_path} does not exist. Please train the model first.")

tokenizer_path = os.path.join(model_path, "tokenizer_config.json")
model_file_path = os.path.join(model_path, "pytorch_model.bin")

if not os.path.exists(tokenizer_path) or not os.path.exists(model_file_path):
    raise EnvironmentError(f"Model files not found in {model_path}. Please ensure the model is correctly saved.")

# Загрузка предобученной модели и токенизатора
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForQuestionAnswering.from_pretrained(model_path)
qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)


# Извлечение текста из .pdf
def extract_text_from_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None


# Извлечение текста из .docx
def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text
        return text
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return None


# Маршрут для главной страницы
@app.route('/')
def upload_form():
    return render_template('upload.html')


# Маршрут для отображения загруженных документов
@app.route('/documents')
def list_documents():
    connection = create_connection()
    if connection is None:
        flash("Failed to connect to database", "error")
        return redirect(url_for('upload_form'))

    documents = get_all_documents(connection)
    return render_template('documents.html', documents=documents)


# Маршрут для обработки загруженных файлов
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        file_type = file.filename.split('.')[-1].lower()  # Приведение расширения файла к нижнему регистру
        temp_file_path = None

        try:
            # Сохранение загруженного файла во временную директорию
            temp_dir = tempfile.gettempdir()
            temp_file_path = os.path.join(temp_dir, file.filename)
            file.save(temp_file_path)

            # Извлечение текста в зависимости от типа файла
            if file_type == 'pdf':
                content = extract_text_from_pdf(temp_file_path)
            elif file_type == 'docx':
                content = extract_text_from_docx(temp_file_path)
            else:
                flash("Unsupported file type", "error")
                return redirect(url_for('upload_form'))

            if content is None:
                flash("Failed to extract text from the document", "error")
                return redirect(url_for('upload_form'))

            # Сохранение документа в базу данных
            connection = create_connection()
            if connection is None:
                flash("Failed to connect to database", "error")
                return redirect(url_for('upload_form'))

            insert_document(connection, file.filename, file_type, content)
            flash("File uploaded successfully!", "success")
        except Exception as e:
            flash(f"An error occurred: {e}", "error")
        finally:
            # Удаление временного файла
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)

        return redirect(url_for('upload_form'))


# Маршрут для задания вопросов
@app.route('/ask', methods=['GET', 'POST'])
def ask_question():
    if request.method == 'POST':
        question = request.form['question']
        context = request.form['context']

        result = qa_pipeline(question=question, context=context)
        return render_template('ask.html', question=question, context=context, answer=result['answer'])

    return render_template('ask.html')


if __name__ == "__main__":
    connection = create_connection()
    if connection is not None:
        create_table(connection)
    else:
        print("Failed to connect to the database. Please check your connection settings.")
    app.run(debug=True)
