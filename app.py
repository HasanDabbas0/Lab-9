from flask import Flask, render_template, request, redirect
from extensions import db
from models import Project

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        link = request.form['link']
        new_project = Project(title=title, link=link)
        db.session.add(new_project)
        db.session.commit()
        return redirect('/')

    projects = Project.query.all()
    return render_template('index.html', projects=projects)

# Новый маршрут для очистки базы данных
@app.route('/clear', methods=['POST'])
def clear():
    Project.query.delete()  # Удаляем все проекты
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
