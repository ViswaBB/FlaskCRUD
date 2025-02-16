#importing 
from datetime import datetime, timezone 
from flask import Flask, redirect ,render_template, request
from flask_scss import Scss
from flask_restful import Api,Resource
from flask_sqlalchemy import SQLAlchemy

#setting up the app
app = Flask(__name__) 

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

#database
class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(100),nullable = False)
    complete = db.Column(db.Integer,default = 0)
    created = db.Column(db.DateTime,default = lambda:datetime.now(timezone.utc)) 

    def __repr__(self):
        return f"Task:{self.id}"

@app.route("/",methods=["POST","GET"])
def index():
    if request.method == "POST":
        current_task = request.form["content"]
        new_task = Task(content= current_task) 
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
            
        except Exception as e:
            print(f"{e}")
            return e 
    else:
        tasks = Task.query.order_by(Task.created).all()
        return render_template("index.html",tasks=tasks) 
    
@app.route('/delete/<int:id>')
def delete(id:int):
    deletetask = Task.query.get_or_404(id)
    try:
        db.session.delete(deletetask)
        db.session.commit()
        return redirect("/")
    except Exception as E:
        print(f"Error {E}")
        return E
    
@app.route('/update/<int:id>',methods= ["GET","POST"])
def update(id:int):
    task = Task.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return e
    else:
        return render_template("update.html",task = task)
if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)  

