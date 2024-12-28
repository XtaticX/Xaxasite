from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'app/static/img/'  # Определите папку для загрузки изображений

@app.route("/")
def home():
    cards_folder = os.path.join(app.template_folder, 'cards', 'news')
    cards = []

    for filename in os.listdir(cards_folder):
        if filename.endswith('.txt'):
            card_data = {}
            with open(os.path.join(cards_folder, filename), 'r', encoding='utf-8') as file:
                lines = file.readlines()
                # Извлекаем данные из строк
                card_data['title'] = lines[0].strip().split(": ")[1]  # Заголовок
                card_data['description'] = lines[1].strip().split(": ")[1]  # Описание
                if len(lines) > 2:
                    card_data['image'] = lines[2].strip().split(": ")[1]  # Имя файла изображения
                else:
                    card_data['image'] = None  # Если изображения нет
            cards.append(card_data)  # Добавляем словарь карточки в список

    return render_template("index.html", cards=cards)


@app.route('/card')
def card():
    return redirect(url_for('home'))  # Перенаправление на главную страницу

@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')  # Здесь должен быть ваш файл admin.html

@app.route('/add_card', methods=['POST'])
def add_card():
    title = request.form['title']
    description = request.form['description']
    image = request.files['image']

    image_filename = None  # Инициализируем переменную для имени изображения

    if image:
        # Сохраните изображение в указанной папке для загрузки
        image_filename = image.filename
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        image.save(image_path)

    # Создаем имя файла для новой карточки
    base_filename = 'templates/cards/news/card'
    file_extension = '.txt'
    counter = 1

    # Проверяем существование файла и создаем новый, если необходимо
    filename = f"{base_filename}{counter}{file_extension}"
    while os.path.exists(filename):
        counter += 1
        filename = f"{base_filename}{counter}{file_extension}"

    # Создаем новый текстовый файл для карточки
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"Title: {title}\n")
        file.write(f"Description: {description}\n")
        file.write(f"Image: {image_filename}\n")

    print(f'Файл {filename} успешно создан!')

    return redirect(url_for('admin'))  # Перенаправление обратно на админ-панель


if __name__ == '__main__':
    app.run(debug=True)
