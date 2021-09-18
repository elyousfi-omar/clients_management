from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clients.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)
    credit = db.Column(db.Float, default = 0)
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        client_name = request.form['name']
        client_credit = request.form['credit']
        new_client = Todo(name=client_name, credit = client_credit)
        
        try:
            db.session.add(new_client)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue addding the client'
    else:
        clients = Todo.query.order_by(Todo.date).all()
        return render_template('index.html', clients=clients)

@app.route('/delete/<int:id>')
def delete(id):
    client_del = Todo.query.get_or_404(id)
    try:
        db.session.delete(client_del)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error deleting the client'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    client = Todo.query.get_or_404(id)

    if request.method=='POST':
        client.name  = request.form['name']
        client.credit = request.form['credit']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating the client'
    else:
        return render_template('update.html', client=client)

if __name__ == "__main__":
    app.run(debug=True)