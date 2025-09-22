from flask import Flask, render_template, request, redirect, url_for;
from werkzeug.security import check_password_hash;
from db import db
from modelo import Usuario, Produto

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST': # verifica se o método usado foi o POST
        nome = request.form['nomeForm']# pega o valor do campo nomeForm do formulário
        email = request.form['emailForm'] # pega o valor do campo emailForm do formulário
        senha = request.form['senhaForm'] # pega o valor do campo senhaForm do formulário

        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()

        return redirect(url_for('index'))
        # renderiza a página cadastro.html e passa os valores de nome e email para ela
    return render_template('cadastro_usuario.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['emailForm']
        senha = request.form['senhaForm']

         # Consulta no banco
        usuario = Usuario.query.filter_by(email=email).first()
        print(usuario)

        if usuario and usuario.senha == senha:
            return f"Login bem-sucedido! Bem-vindo {usuario.nome}"
        else:
            return "Usuário ou senha inválidos"
    return render_template('login.html')

@app.route('/produtos', methods=["GET", "POST"])
def produtos():
    if request.method == 'POST': # verifica se o método usado foi o POST
        nome = request.form['nome']
        preco = request.form['preco']
        descricao = request.form['descricao']

        novo_produto = Produto(nome=nome, preco=preco, descricao=descricao)
        db.session.add(novo_produto)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('produtos.html')

if __name__ == '__main__':
    with app.app_context():
    # cria o contexto da aplicação web
        db.create_all()
        # cria todas as tabelas do banco de dados que ainda não existem
    app.run()