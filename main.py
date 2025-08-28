from flask import render_template, redirect, url_for, session
from config import app

from models import *
from formulario import *

"""
pip install flask, flask-wtf, flask_sqlalchemy, flask_login

"""


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    formulario = FormularioCriarconta()

    # if formulario.validate_on_submit():
    if formulario.username.data and formulario.password.data:
        usu = formulario.username.data
        sen = formulario.password.data
        print(f'-- {usu} -- {sen}')

        usu_ex = User.query.filter_by(username=usu).first()

        if usu_ex:
            print('Usuario ja existe')
            return redirect(url_for('login'))
        else:
            novo_usuario = User(username=usu, password=sen)
            db.session.add(novo_usuario)
            db.session.commit()
            print('Usuario Criado')
            return redirect(url_for('home'))

    return render_template('register.html', form=formulario)


@app.route('/login', methods=['GET', 'POST'])
def login():
    formulario = FormularioLogin()

    if formulario.validate_on_submit():
        usu = formulario.username.data
        sen = formulario.password.data
        print(f'-- {usu} -- {sen}')

        usu_ex = User.query.filter_by(username=usu).first()

        if usu_ex:
            if usu_ex.password == sen:
                print('Login com sucesso')
                session['user_id'] = usu_ex.id
                return redirect(url_for('dashboard'))
            else:
                print('Senha incorreta')
        else:
            print('Usuario nao existe')
            return redirect(url_for('register'))

    return render_template('login.html', form=formulario)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    events = Evento.query.all()

    current_user_id = session.get('user_id')

    myEvents = Evento.query.filter_by(id_usuario=current_user_id).all()
    return render_template('dashboard.html', todos_eventos=events, meus_eventos=myEvents)


@app.route('/create_event', methods=['GET', 'POST'])
def create_event():

    formulario = FormularioEvento()

    if formulario.validate_on_submit():
        nome = formulario.nome.data
        desc = formulario.descricao.data
        dat = formulario.data.data

        curent_user_id = session.get('user_id')

        novoEvento = Evento(nome=nome, descricao=desc, dataEvento=dat, id_usuario=curent_user_id)
        db.session.add(novoEvento)
        db.session.commit()

        print('-'*10)
        print(f'> {nome}')
        print(f'> {desc}')
        print(f'> {dat}')
        print('-'*10)

        return redirect(url_for('dashboard'))

    return render_template('create_event.html', form=formulario)


@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):

    formulario = FormularioEvento()

    if formulario.validate_on_submit():
        nome = formulario.nome.data
        desc = formulario.descricao.data
        dat = formulario.data.data

        evento = Evento.query.get(event_id)
        evento.nome = nome
        evento.descricao = desc
        evento.dataEvento = dat
        db.session.commit()

        print('-'*10)
        print(f'> {nome}')
        print(f'> {desc}')
        print(f'> {dat}')
        print('-'*10)

        return redirect(url_for('dashboard'))

    return render_template('edit_event.html', form=formulario)


@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    Evento.query.filter_by(id=event_id).delete()
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/perfil')
def perfil():

    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    current_user_id = session.get('user_id')
    user = User.query.filter_by(id=current_user_id).first()

    return render_template('perfil.html', usuario=user.username)

if __name__ == '__main__':
    app.run(debug=True)
