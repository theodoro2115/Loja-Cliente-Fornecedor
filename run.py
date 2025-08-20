from flask import Flask, redirect, render_template, request, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_super_secreta'

UPLOAD_FOLDER = 'static/assets'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['dados_login'] = None

# Certifique-se de que a pasta de upload existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')

    conexao = sqlite3.connect('models/loja.db')
    cursor = conexao.cursor()

    sql = "SELECT * FROM tb_login WHERE usuario = ? AND senha = ?"
    cursor.execute(sql, (usuario, senha))

    login_usuario = cursor.fetchone()
    conexao.close()

    if login_usuario:
        app.config['dados_login'] = login_usuario
        return redirect('/cliente')
    return redirect('/')

@app.route('/cliente', methods=['GET', 'POST'])
def cliente():
    usuario = app.config.get('dados_login')  # Dados do login do usuário
    
    if not usuario:
        return redirect('/')
    
    # Verifica se o usuário possui uma imagem
    avatar = f"assets/{usuario[3]}" if len(usuario) > 3 and usuario[3] else "assets/default.png"
    print("Caminho do avatar:", avatar)  # Depuração: verifica o caminho gerado
    
    # Caso seja um POST, manipular os dados enviados
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        cpf = request.form.get('cpf')
        cep = request.form.get('cep')
        endereco = request.form.get('endereco')
        cidade = request.form.get('cidade')
        estado = request.form.get('estado')
        data_cadastro = request.form.get('data_cadastro')

        conexao = sqlite3.connect('models/loja.db')
        cursor = conexao.cursor()

        sql = """
            INSERT INTO tb_cliente (nome, telefone, email, cpf, cep, endereco, cidade, estado, data_cadastro)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (nome, telefone, email, cpf, cep, endereco, cidade, estado, data_cadastro))

        conexao.commit()
        conexao.close()

        return redirect('/cliente')

    # Renderiza o template
    return render_template('cliente.html', usuario=usuario)



@app.route('/consultaclie')
def consulta_clientes():
    usuario = app.config.get('dados_login')  
    
    if not usuario:
        return redirect('/')
    
    avatar = f"assets/{usuario[3]}" if len(usuario) > 3 and usuario[3] else "assets/default.png"
    print("Caminho do avatar:", avatar) 

    
    conexao = sqlite3.connect('models/loja.db')
    cursor = conexao.cursor()

    # Seleciona todas as informações da tabela tb_cliente
    cursor.execute("SELECT * FROM tb_cliente")
    clientes = cursor.fetchall()  # Lista com todos os clientes
    conexao.close()

    return render_template("consultaclie.html", clientes=clientes, usuario=usuario)


@app.route('/ver_fornecedor/<int:id>', methods=['GET', 'POST'])
def ver_fornecedor(id):
    usuario = app.config.get('dados_login')  
    
    if not usuario:
        return redirect('/')
    
    avatar = f"assets/{usuario[3]}" if len(usuario) > 3 and usuario[3] else "assets/default.png"
    print("Caminho do avatar:", avatar) 

    conexao = sqlite3.connect('models/loja.db')
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM tb_fornecedor WHERE fornecedor_id = ?", (id,))
    fornecedor = cursor.fetchone()
    conexao.close()

    if fornecedor:
        return render_template('ver_fornecedor.html', fornecedor=fornecedor, usuario=usuario)
    

@app.route('/consultafor')
def consulta_fornecedores():
    usuario = app.config.get('dados_login')  
    
    if not usuario:
        return redirect('/')
    
    avatar = f"assets/{usuario[3]}" if len(usuario) > 3 and usuario[3] else "assets/default.png"
    print("Caminho do avatar:", avatar) 

    
    conexao = sqlite3.connect('models/loja.db')
    cursor = conexao.cursor()

    # Seleciona todas as informações da tabela tb_fornecedor
    cursor.execute("SELECT * FROM tb_fornecedor")
    fornecedores = cursor.fetchall()  # Lista com todos os fornecedores
    conexao.close()

    return render_template("consultafor.html", fornecedores=fornecedores, usuario=usuario)


@app.route('/fornecedor', methods=['GET', 'POST'])
def fornecedor():
    usuario = app.config.get('dados_login')  # Dados do login do usuário
    
    if not usuario:
        return redirect('/')
    
    # Verifica se o usuário possui uma imagem
    avatar = f"assets/{usuario[3]}" if len(usuario) > 3 and usuario[3] else "assets/default.png"
    print("Caminho do avatar:", avatar)  # Depuração: verifica o caminho gerado
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        cnpj = request.form.get('cnpj')
        cep = request.form.get('cep')
        endereco = request.form.get('endereco')
        cidade = request.form.get('cidade')
        estado = request.form.get('estado')
        data_cadastro = request.form.get('data_cadastro')

        conexao = sqlite3.connect('models/loja.db')
        cursor = conexao.cursor()

        sql = """
            INSERT INTO tb_fornecedor (nome, telefone, email, cnpj, cep, endereco, cidade, estado, data_cadastro)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (nome, telefone, email, cnpj, cep, endereco, cidade, estado, data_cadastro))

        conexao.commit()
        conexao.close()

        return redirect('/consultafor')

    return render_template("fornecedor.html", usuario=usuario)   

@app.route('/logout')
def logout():
    app.config['dados_login'] = None
    return redirect('/') 

@app.route('/efetuar_cadastro', methods=['GET', 'POST'])
def efetuar_cadastro():
        usuario = None  # Define um valor padrão para a variável
        if request.method == 'POST':
            nome_usuario = request.form.get('nome')
            usuario = request.form.get('usuario')
            senha = request.form.get('senha')
            avatar = request.files.get('imagem')
 
            conexao = sqlite3.connect('models/loja.db')
            cursor = conexao.cursor()
 
 
 
            cursor.execute("SELECT * FROM tb_login WHERE usuario_id = ?", (usuario,))
            if cursor.fetchone():
                return "Usuário já existe. Tente outro."
           
                    # Verificar se o usuário já existe
 
            
 
            nome_avatar = None
            if avatar:
                extensao = avatar.filename.split('.')[-1]
                nome_avatar = f"{avatar.filename.strip().lower().replace(' ', '_')}"
                caminho_avatar = os.path.join(app.config['UPLOAD_FOLDER'], avatar.filename)
                avatar.save(caminho_avatar)
 
            cursor.execute("INSERT INTO tb_login (nome_usuario, usuario, senha, avatar) VALUES (?, ?, ?, ?)", 
               (nome_usuario, usuario, senha, nome_avatar))

            conexao.commit()
            conexao.close()
 
            return redirect ('/login')  # Redireciona para a página de login
     
        return render_template('cadastro.html', usuario=usuario)  # Retorna o formulário de cadastro

@app.route('/excluir_cliente/<int:id>', methods=['GET'])
def excluir_cliente(id):
    conexao = sqlite3.connect('models/loja.db')
    cursor = conexao.cursor()
 
    sql = 'DELETE FROM tb_cliente WHERE cliente_id = ?'
    cursor.execute(sql, (id,))
 
    conexao.commit()
    conexao.close()
 
    return redirect('/consultaclie')


@app.route('/excluir_fornecedor/<int:id>', methods=['GET'])
def excluir_fornecedor(id):
    conexao = sqlite3.connect('models/loja.db')
    cursor = conexao.cursor()
 
    sql = 'DELETE FROM tb_fornecedor WHERE fornecedor_id = ?'
    cursor.execute(sql, (id,))
 
    conexao.commit()
    conexao.close()
 
    return redirect('/consultafor')

@app.route('/editarclie/<int:cliente_id>', methods=['GET', 'POST'])
def editarclie(cliente_id):  # O nome do parâmetro na rota e na função agora são iguais
    nome = session.get('nome')
    imagem = session.get('imagem')
 
    if nome is None:
        return redirect('/')
 
    conexao = sqlite3.connect('models/loja.db')
    cursor = conexao.cursor()
 
    if request.method == 'POST':
        # Captura os dados do formulário para atualização
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        cpf = request.form['cpf']
        cep = request.form['cep']
        endereco = request.form['endereco']
        cidade = request.form['cidade']
        estado = request.form['estado']
        data_cadastro = request.form['data_cadastro']
 
        # Atualiza os dados no banco de dados
        sql = '''UPDATE tb_clientes
                 SET nome=?, email=?, telefone=?, cpf=?, cep=?, endereco=?, cidade=?, estado=?, data_cadastro=?, imagem=?
                 WHERE cliente_id=?'''
        cursor.execute(sql, (nome, email, telefone, cpf, cep, endereco, cidade, estado, data_cadastro, cliente_id))
        conexao.commit()
 
        return redirect('/consultaclie')
    else:
        # Busca os dados atuais do cliente para exibir no formulário de edição
        cursor.execute('SELECT * FROM tb_cliente WHERE cliente_id=?', (cliente_id,))
        cliente = cursor.fetchone()
        conexao.close()
        return render_template('editarclie.html', cliente=cliente, nome=nome)

@app.route('/ver_cliente/<int:id>', methods=['GET', 'POST'])
def ver_cliente(id):
    usuario = app.config.get('dados_login')  # Dados do login do usuário
    
    if not usuario:
        return redirect('/')
    
    # Verifica se o usuário possui uma imagem
    avatar = f"assets/{usuario[3]}" if len(usuario) > 3 and usuario[3] else "assets/default.png"
    print("Caminho do avatar:", avatar)  # Depuração: verifica o caminho gerado
    

    # Usando o gerenciador de contexto 'with' para garantir o fechamento da conexão
    with sqlite3.connect('models/loja.db') as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM tb_cliente WHERE cliente_id = ?", (id,))
        cliente = cursor.fetchone()

    if cliente:
        return render_template('ver_cliente.html', cliente=cliente, usuario=usuario)



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80, debug=True)
