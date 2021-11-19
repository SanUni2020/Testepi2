from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comentarios.sqlite3'
db = SQLAlchemy(app)


class Comentario(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    comentario = db.Column(db.String(300), nullable=False)

    def __init__(self, nome, comentario):
        self.nome = nome
        self.comentario = comentario


@app.route('/')
def index():
    comentarios = Comentario.query.all()
    return render_template('index.html', comentarios=comentarios)


@app.route("/mensagem")
def mensagem():
    return render_template("mensagem.html")


@app.route("/obrigado")
def obrigado():
    return render_template("obrigado.html")


@app.route('/<id>')
def comenta_pelo_id(id):
   comenta = Comentario.query.get(id)
   return render_template('index.html', comenta=comenta)


@app.route('/novo', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        comenta = Comentario(request.form['nome'], request.form['comentario'])
        db.session.add(comenta)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('novo.html')


@app.route('/edita/<int:id>', methods=['GET', 'POST'])
def edit(id):
    comenta = Comentario.query.get(id)
    if request.method == 'POST':
        comenta.nome = request.form['nome']
        comenta.comentario = request.form['comentario']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edita.html', comenta=comenta)


@app.route('/delete/<int:id>')
def delete(id):
    comenta = Comentario.query.get(id)
    db.session.delete(comenta)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
