# for creating a flask app it is recomended to create a seperate virtual envirnoment first
# so we execute this command first "pip iinstall virtualenv"
# now execute this command first "virtualenv env"
# run this command in powershell with admin rights "Set-ExecutionPolicy unrestricted"
# now this command "pip install flask-sqlalchemy" installin sql type db for storing data in todo.db file
# then activate the virtual envirnoment by executing this command ".\env\Scripts\activate.ps1"
# now you can run "pip install flask" to install flask
# now you can run "python app.py" to start flask app
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    tittle = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.tittle} - {self.description}"

def initialize_database():
    with app.app_context():
        db.create_all()

@app.route('/', methods=['GET','POST'])
def home():
    if request.method=='POST':
        tittle = request.form['tittle']
        description = request.form['description']
        if not tittle or not description:
            pass
        else:
            todo = Todo(tittle=tittle, description=description)
            db.session.add(todo)
            db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method == "POST":
        tittle = request.form['tittle']
        description = request.form['description']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.tittle = tittle
        todo.description = description
        if not todo.tittle or not todo.description:
            pass
        else:
            db.session.add(todo)
            db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/greet/<string:name>')
def greet(name):
    return render_template('greet.html', name=name)

if __name__=="__main__":
    initialize_database()
    app.run(debug=True, port=8000)