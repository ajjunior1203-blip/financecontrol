from flask import Flask, render_template, request, redirect, session
import psycopg2
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'segredo'
UPLOAD_FOLDER = 'static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def conectar():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE,
            senha TEXT,
            nome TEXT,
            email TEXT,
            montante REAL DEFAULT 0,
            reserva REAL DEFAULT 0,
            dark_mode INTEGER DEFAULT 0,
            banco_montante TEXT,
            banco_reserva TEXT,
            foto_url TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS investimentos (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER,
            tipo TEXT,
            codigo TEXT,
            quantidade INTEGER,
            valor_unitario REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orcamentos (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER,
            mes TEXT,
            categoria TEXT,
            valor REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lancamentos (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER,
            data TEXT,
            descricao TEXT,
            categoria TEXT,
            tipo TEXT,
            valor REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categorias (
            id SERIAL PRIMARY KEY,
            nome TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

@app.template_filter('format_currency')
def format_currency(value):
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        usuario = request.form['usuario'].strip()
        senha = request.form['senha'].strip()
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('SELECT id, senha FROM usuarios WHERE username=%s', (usuario,))
        user = cursor.fetchone()
        conn.close()
        if user and check_password_hash(user[1], senha):
            session['usuario_id'] = user[0]
            return redirect('/dashboard')
        else:
            erro = "Usuário ou senha inválidos."
    return render_template('login.html', erro=erro)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    erro = None
    if request.method == 'POST':
        usuario = request.form['usuario'].strip()
        senha = request.form['senha'].strip()
        confirmar = request.form['confirmar'].strip()

        if not usuario or not senha or not confirmar:
            erro = "Todos os campos são obrigatórios."
        elif senha != confirmar:
            erro = "As senhas não coincidem."
        else:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM usuarios WHERE username=%s', (usuario,))
            if cursor.fetchone():
                erro = "Usuário já existe."
            else:
                senha_hash = generate_password_hash(senha)
                cursor.execute('''
                    INSERT INTO usuarios (username, senha, nome, email, montante, reserva, dark_mode, banco_montante, banco_reserva, foto_url)
                    VALUES (%s, %s, '', '', 0, 0, 0, '', '', '')
                ''', (usuario, senha_hash))
                conn.commit()
                conn.close()
                return redirect('/login')
            conn.close()
    return render_template('cadastro.html', erro=erro)

from flask import Flask, render_template, request, redirect, session
import psycopg2
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'segredo'
UPLOAD_FOLDER = 'static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def conectar():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            nome TEXT,
            email TEXT,
            montante REAL DEFAULT 0,
            reserva REAL DEFAULT 0,
            dark_mode BOOLEAN DEFAULT FALSE,
            banco_montante TEXT,
            banco_reserva TEXT,
            foto_url TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS investimentos (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
            tipo TEXT,
            codigo TEXT,
            quantidade INTEGER,
            valor_unitario REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orcamentos (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
            mes TEXT,
            categoria TEXT,
            valor REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lancamentos (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
            data DATE,
            descricao TEXT,
            categoria TEXT,
            tipo TEXT CHECK (tipo IN ('entrada', 'saida')),
            valor REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categorias (
            id SERIAL PRIMARY KEY,
            nome TEXT UNIQUE NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


@app.template_filter('format_currency')
def format_currency(value):
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        usuario = request.form['usuario'].strip()
        senha = request.form['senha'].strip()
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('SELECT id, senha FROM usuarios WHERE username=%s', (usuario,))
        user = cursor.fetchone()
        conn.close()
        if user and check_password_hash(user[1], senha):
            session['usuario_id'] = user[0]
            return redirect('/dashboard')
        else:
            erro = "Usuário ou senha inválidos."
    return render_template('login.html', erro=erro)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    erro = None
    if request.method == 'POST':
        usuario = request.form['usuario'].strip()
        senha = request.form['senha'].strip()
        confirmar = request.form['confirmar'].strip()

        if not usuario or not senha or not confirmar:
            erro = "Todos os campos são obrigatórios."
        elif senha != confirmar:
            erro = "As senhas não coincidem."
        else:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM usuarios WHERE username=%s', (usuario,))
            if cursor.fetchone():
                erro = "Usuário já existe."
            else:
                senha_hash = generate_password_hash(senha)
                cursor.execute('''
                    INSERT INTO usuarios (username, senha, nome, email, montante, reserva, dark_mode, banco_montante, banco_reserva, foto_url)
                    VALUES (%s, %s, '', '', 0, 0, 0, '', '', '')
                ''', (usuario, senha_hash))
                conn.commit()
                conn.close()
                return redirect('/login')
            conn.close()
    return render_template('cadastro.html', erro=erro, usuario={'dark_mode': False})

@app.route('/orcamentos', methods=['GET', 'POST'])
def orcamentos():
    if 'usuario_id' not in session:
        return redirect('/login')
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('SELECT nome FROM categorias')
    categorias = [row[0] for row in cursor.fetchall()]

    if request.method == 'POST':
        mes = request.form['mes']
        categoria = request.form['categoria']
        valor_str = request.form['valor'].replace(',', '.')
        valor = float(valor_str)
        cursor.execute('INSERT INTO orcamentos (usuario_id, mes, categoria, valor) VALUES (%s, %s, %s, %s)',
                       (session['usuario_id'], mes, categoria, valor))
        conn.commit()

    cursor.execute('SELECT id, mes, categoria, valor FROM orcamentos WHERE usuario_id=%s', (session['usuario_id'],))
    dados_raw = cursor.fetchall()

    cursor.execute('SELECT dark_mode FROM usuarios WHERE id=%s', (session['usuario_id'],))
    resultado = cursor.fetchone()
    usuario = {'dark_mode': bool(resultado[0])} if resultado else {'dark_mode': False}

    conn.close()

    from collections import defaultdict
    dados_agrupados = defaultdict(lambda: defaultdict(list))
    for id, mes, categoria, valor in dados_raw:
        ano = "2025"
        dados_agrupados[ano][mes].append((id, categoria, valor))

    return render_template('orcamentos.html',
                           categorias=categorias,
                           dados_agrupados=dados_agrupados,
                           usuario=usuario,
                           active_page='orcamentos')

@app.route('/editar_orcamento/<int:id>', methods=['GET', 'POST'])
def editar_orcamento(id):
    if 'usuario_id' not in session:
        return redirect('/login')
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('SELECT nome FROM categorias')
    categorias = [row[0] for row in cursor.fetchall()]

    if request.method == 'POST':
        mes = request.form['mes']
        categoria = request.form['categoria']
        valor_str = request.form['valor'].replace(',', '.')
        valor = float(valor_str)
        cursor.execute('UPDATE orcamentos SET mes=%s, categoria=%s, valor=%s WHERE id=%s AND usuario_id=%s',
                       (mes, categoria, valor, id, session['usuario_id']))
        conn.commit()
        conn.close()
        return redirect('/orcamentos')

    cursor.execute('SELECT mes, categoria, valor FROM orcamentos WHERE id=%s AND usuario_id=%s', (id, session['usuario_id']))
    dados = cursor.fetchone()
    conn.close()
    return render_template('editar_orcamento.html', dados=dados, categorias=categorias)

@app.route('/excluir_orcamento/<int:id>')
def excluir_orcamento(id):
    if 'usuario_id' not in session:
        return redirect('/login')
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM orcamentos WHERE id=%s AND usuario_id=%s', (id, session['usuario_id']))
    conn.commit()
    conn.close()
    return redirect('/orcamentos')

@app.route('/lancamentos', methods=['GET', 'POST'])
def lancamentos():
    if 'usuario_id' not in session:
        return redirect('/login')
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('SELECT nome FROM categorias')
    categorias = [row[0] for row in cursor.fetchall()]

    if request.method == 'POST':
        mes = request.form['mes']
        descricao = request.form['descricao']
        categoria = request.form['categoria']
        tipo = request.form['tipo']
        valor_str = request.form['valor'].replace(',', '.')
        valor = float(valor_str)
        data_formatada = f"{datetime.now().year}-{mes}-01"
        cursor.execute('''
            INSERT INTO lancamentos (usuario_id, data, descricao, categoria, tipo, valor)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (session['usuario_id'], data_formatada, descricao, categoria, tipo, valor))
        conn.commit()

    cursor.execute('''
        SELECT id, data, descricao, categoria, tipo, valor
        FROM lancamentos
        WHERE usuario_id=%s
        ORDER BY data DESC
    ''', (session['usuario_id'],))
    dados_raw = cursor.fetchall()

    cursor.execute('SELECT dark_mode FROM usuarios WHERE id=%s', (session['usuario_id'],))
    resultado = cursor.fetchone()
    usuario = {'dark_mode': bool(resultado[0])} if resultado else {'dark_mode': False}

    conn.close()

    from collections import defaultdict
    dados_agrupados = defaultdict(lambda: defaultdict(list))
    for id, data, descricao, categoria, tipo, valor in dados_raw:
        ano, mes, _ = data.split('-')
        dados_agrupados[ano][mes].append((id, data, descricao, categoria, tipo, valor))

    return render_template('lancamentos.html',
                           categorias=categorias,
                           dados_agrupados=dados_agrupados,
                           usuario=usuario,
                           active_page='lancamentos')

@app.route('/editar_lancamento/<int:id>', methods=['GET', 'POST'])
def editar_lancamento(id):
    if 'usuario_id' not in session:
        return redirect('/login')
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('SELECT nome FROM categorias')
    categorias = [row[0] for row in cursor.fetchall()]

    if request.method == 'POST':
        mes = request.form['mes']
        descricao = request.form['descricao']
        categoria = request.form['categoria']
        tipo = request.form['tipo']
        valor_str = request.form['valor'].replace(',', '.')
        valor = float(valor_str)
        data_formatada = f"{datetime.now().year}-{mes}-01"

        cursor.execute('''
            UPDATE lancamentos
            SET data=%s, descricao=%s, categoria=%s, tipo=%s, valor=%s
            WHERE id=%s AND usuario_id=%s
        ''', (data_formatada, descricao, categoria, tipo, valor, id, session['usuario_id']))
        conn.commit()
        conn.close()
        return redirect('/lancamentos')

    cursor.execute('''
        SELECT data, descricao, categoria, tipo, valor
        FROM lancamentos
        WHERE id=%s AND usuario_id=%s
    ''', (id, session['usuario_id']))
    resultado = cursor.fetchone()
    conn.close()

    mes = resultado[0].split('-')[1] if resultado else ''
    dados = (mes, resultado[1], resultado[2], resultado[3], resultado[4]) if resultado else ('', '', '', '', '')
    return render_template('editar_lancamento.html', dados=dados, categorias=categorias)

@app.route('/excluir_lancamento/<int:id>')
def excluir_lancamento(id):
    if 'usuario_id' not in session:
        return redirect('/login')
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM lancamentos WHERE id=%s AND usuario_id=%s', (id, session['usuario_id']))
    conn.commit()
    conn.close()
    return redirect('/lancamentos')

@app.route('/graficos', methods=['GET'])
def graficos():
    if 'usuario_id' not in session:
        return redirect('/login')

    mes = request.args.get('mes')
    ano = request.args.get('ano')

    conn = conectar()
    cursor = conn.cursor()

    if mes and ano:
        filtro = f"{ano}-{mes.zfill(2)}%"
        cursor.execute('''
            SELECT categoria, SUM(valor)
            FROM lancamentos
            WHERE usuario_id=%s AND tipo='saida' AND data LIKE %s
            GROUP BY categoria
        ''', (session['usuario_id'], filtro))
    else:
        cursor.execute('''
            SELECT categoria, SUM(valor)
            FROM lancamentos
            WHERE usuario_id=%s AND tipo='saida'
            GROUP BY categoria
        ''', (session['usuario_id'],))

    dados = cursor.fetchall()

    cursor.execute('SELECT dark_mode FROM usuarios WHERE id=%s', (session['usuario_id'],))
    resultado = cursor.fetchone()
    usuario = {'dark_mode': bool(resultado[0])} if resultado else {'dark_mode': False}

    conn.close()

    return render_template('graficos.html',
                           dados=dados,
                           mes=mes,
                           ano=ano,
                           usuario=usuario,
                           active_page='graficos')

@app.route('/categorias', methods=['GET', 'POST'])
def categorias():
    if 'usuario_id' not in session:
        return redirect('/login')
    conn = conectar()
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        cursor.execute('INSERT INTO categorias (nome) VALUES (%s)', (nome,))
        conn.commit()

    cursor.execute('SELECT id, nome FROM categorias')
    lista = cursor.fetchall()

    cursor.execute('SELECT dark_mode FROM usuarios WHERE id=%s', (session['usuario_id'],))
    resultado = cursor.fetchone()
    usuario = {'dark_mode': bool(resultado[0])} if resultado else {'dark_mode': False}

    conn.close()
    return render_template('categorias.html',
                           categorias=lista,
                           usuario=usuario,
                           active_page='categorias')

@app.route('/editar_categoria/<int:id>', methods=['GET', 'POST'])
def editar_categoria(id):
    if 'usuario_id' not in session:
        return redirect('/login')
    conn = conectar()
    cursor = conn.cursor()

    if request.method == 'POST':
        novo_nome = request.form['nome']
        cursor.execute('UPDATE categorias SET nome=%s WHERE id=%s', (novo_nome, id))
        conn.commit()
        conn.close()
        return redirect('/categorias')

    cursor.execute('SELECT nome FROM categorias WHERE id=%s', (id,))
    nome = cursor.fetchone()[0]
    conn.close()
    return render_template('editar_categoria.html', nome=nome)

@app.route('/excluir_categoria/<int:id>')
def excluir_categoria(id):
    if 'usuario_id' not in session:
        return redirect('/login')
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM categorias WHERE id=%s', (id,))
    conn.commit()
    conn.close()
    return redirect('/categorias')

if __name__ == '__main__':
    criar_tabelas()
    app.run(debug=True)
