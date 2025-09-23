from flask import Flask, render_template, request, redirect, url_for, flash;
from werkzeug.security import check_password_hash;
from modelo import engine, Usuario, Produto
from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import declarative_base, sessionmaker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
app.secret_key = "SENHASUPERHIPERMEGASECRETAUAAAAAU"
Sessao_base = sessionmaker(engine)

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
        with Sessao_base() as sessao: # instancia a Sessao_base como a variável 'sessao'
            sessao.add(novo_usuario)
            sessao.commit()
        return redirect(url_for('index'))
        # renderiza a página cadastro.html e passa os valores de nome e email para ela
    return render_template('cadastro_usuario.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['emailForm']
        senha = request.form['senhaForm']

        # Consulta no banco
        with Sessao_base() as sessao:
            usuario = sessao.query(Usuario).filter_by(email=email).first()
            print(usuario)

        if usuario and usuario.senha == senha:
            return f"Login bem-sucedido! Bem-vindo {usuario.nome}"
        else:
            return "Usuário ou senha inválidos"
    return render_template('login.html')

@app.route('/cadastrar_produtos', methods=["GET", "POST"])
def cadastrar_produtos():
    if request.method == 'POST': # verifica se o método usado foi o POST
        nome = request.form['nome']
        preco = request.form['preco']
        descricao = request.form['descricao']

        if float(preco) <= -1:
            flash('O valor não pode ser menor do que 0. Coloque outrto valor.', category='error')
            return redirect(url_for('cadastrar_produtos'))
        else:
            pass

        novo_produto = Produto(nome=nome, preco=preco, descricao=descricao)
        with Sessao_base() as sessao: # instancia a Sessao_base como a variável 'sessao'
            sessao.add(novo_produto)
            sessao.commit()

        return redirect(url_for('exibir_produtos'))
    return render_template('cadastrar_produtos.html')

@app.route('/exibir_produtos', methods=["GET", "POST"])
def exibir_produtos():
    with Sessao_base() as sessao:
            produtos = sessao.query(Produto).all()
            print(produtos)
    return render_template("produtos.html", produtos=produtos)

@app.route('/remover_produto', methods=["GET", "POST"])
def remover_produto():
    pro_id = request.form['id']

    with Sessao_base() as sessao:
        produto = sessao.query(Produto).filter_by(id=pro_id).first()
        if produto:
            sessao.delete(produto)
            sessao.commit()
        else:
            flash("Produto não encontrado.", category="error")
    
    return redirect(url_for('exibir_produtos'))

@app.route('/editar_produto/<id>', methods=["GET", "POST"])
def editar_produto(id):
    if request.method == 'POST':
        
        pro_id = request.form['id']
        nome = request.form['nome']
        preco = request.form['preco']
        descricao = request.form['descricao']

        if float(preco) <= -1:
            flash('O valor não pode ser menor do que 0. Coloque outrto valor.', category='error')
            return redirect(url_for('editar_produto'))
        else:
            pass

        with Sessao_base() as sessao: # instancia a Sessao_base como a variável 'sessao'
            produto = sessao.query(Produto).filter_by(id=pro_id).first()

            if not produto:
                flash("Produto não encontrado.", category="error")
                return redirect(url_for("exibir_produtos"))

            produto.nome = nome
            produto.preco = preco
            produto.descricao = descricao
            sessao.commit()

            return redirect(url_for('exibir_produtos'))
    
    if request.method == 'GET':
        with Sessao_base() as sessao:
            produto = sessao.query(Produto).filter_by(id=id).first()

            if not produto:
                flash("Produto não encontrado.", category="error")
                return redirect(url_for("exibir_produtos"))

            return render_template("editar_produto.html", produto=produto)

if __name__ == '__main__':
    app.run(debug=True)