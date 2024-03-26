from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import mysql.connector
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
from datetime import datetime

app = Flask(__name__, static_folder='static')
app.secret_key = 'aviso'


# Conectar ao banco de dados MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="", #1234
    database="happyday"
)

# Verificar se a conexão foi estabelecida com sucesso
if db.is_connected():
    print("Conexão bem-sucedida ao banco de dados.")
else:
    print("Não foi possível conectar ao banco de dados.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auth_login', methods=['POST'])
def auth_login():
    email = request.form['email']
    senha = request.form['senha']

    cursor = db.cursor()

    try:
        cursor.execute("SELECT ID_USER, NOME FROM USUARIO WHERE EMAIL = %s AND SENHA = %s", (email, senha))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Definir informações do usuário na sessão
            session['usuario_id'] = user[0]
            session['usuario_nome'] = user[1]
            # Redirecionar para a página principal após o login
            return redirect(url_for('main_page'))
        else:
            flash("Credenciais inválidas. Tente novamente.", "error")
            return redirect(url_for('index'))

    except mysql.connector.Error as err:
        return f"Erro de programação: {err}"

@app.route('/logout')
def logout():
    session.clear()  # Limpa todas as informações da sessão
    return redirect(url_for('index'))

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        cursor = db.cursor()

        try:
            # Verificar se o email já está cadastrado
            cursor.execute("SELECT * FROM USUARIO WHERE EMAIL = %s", (email,))
            if cursor.fetchone() is not None:
                cursor.close()
                flash("Usuário já tem uma conta com este email!", "warning")
                return redirect(url_for('index'))

            # Inserir novo usuário no banco de dados
            cursor.execute("INSERT INTO USUARIO (NOME, EMAIL, SENHA) VALUES (%s, %s, %s)", (nome, email, senha))
            db.commit()
            cursor.close()
            flash("Cadastro realizado com sucesso. Faça o login.", "success")
            return redirect(url_for('index'))

        except mysql.connector.Error as err:
            return f"Erro de programação: {err}"

    return render_template('new_user.html')

@app.route('/main_page')
def main_page():
    if 'usuario_nome' in session:
        return render_template('main_page.html', usuario_nome=session['usuario_nome'])
    else:
        return redirect(url_for('index'))
    
@app.route('/aniversariante', methods=['GET', 'POST'])
def aniversariante():
    usuario_id = session.get('usuario_id')  # Obtém o ID do usuário logado
    if request.method == 'POST':
        nome = request.form['nome']
        grupo = request.form['grupo']
        data_nascimento = request.form['data_nascimento']
        observacoes = request.form['observacoes']

        cursor = db.cursor()

        try:
            # Verifica se o aniversariante já existe no banco de dados
            cursor.execute("SELECT * FROM ANIVERSARIO WHERE NOME = %s AND NASCIMENTO = %s", (nome, data_nascimento))
            aniversariante_existente = cursor.fetchone()

            if aniversariante_existente:
                flash("Este aniversariante já foi adicionado anteriormente.", "warning")
                return redirect(url_for('aniversariante'))
            else:
            # Insere o novo aniversariante no banco de dados
                cursor.execute("INSERT INTO ANIVERSARIO (NOME, NASCIMENTO, OBSERVACOES, ID_ANI_GRUPO, ID_ANI_USER) VALUES (%s, %s, %s, %s, %s)", (nome, data_nascimento, observacoes, grupo, usuario_id))
                db.commit()

                flash("Aniversariante adicionado com sucesso.", "success")
                return redirect(url_for('aniversariante'))

        except mysql.connector.Error as err:
            return f"Erro de programação: {err}"
            
    # Carrega os grupos do banco de dados

    grupos=return_grupos()

    return render_template('aniversariante.html', grupos=grupos)

    
'''
@app.route('/calendariopadrao', methods=['GET'])
def calendariopadrao():
    # Verifica se o usuário está logado
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        # Se não estiver logado, redireciona para a página de login
        flash("Você precisa estar logado para acessar esta página.", "warning")
        return redirect(url_for('index'))
    
    # Prepara a consulta ao banco de dados
    cursor = db.cursor(dictionary=True)
    
    try:
        # Seleciona os aniversários relacionados ao usuário logado
        cursor.execute("SELECT * FROM ANIVERSARIO WHERE ID_ANI_USER = %s", (usuario_id,))
        aniversarios = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Erro ao buscar aniversários: {err}", "error")
        aniversarios = []
    finally:
        cursor.close()
    
    # Passa a lista de aniversários para o template
    return render_template('calendariopadrao.html', aniversarios=aniversarios)
'''
@app.route('/calendariopadrao', methods=['GET'])
def calendariopadrao():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('index'))

    grupo_selecionado = request.args.get('grupo')  # Obtém o parâmetro de query 'grupo'

    cursor = db.cursor(dictionary=True)
    
    try:
        # Buscar os grupos da base de dados
        cursor.execute("SELECT ID_GRUPO, NOME_GRUPO FROM GRUPO WHERE ID_GRU_USER = %s", (usuario_id,))
        grupos = cursor.fetchall()

        # Filtrar aniversários por grupo, se um grupo foi selecionado
        if grupo_selecionado and grupo_selecionado != 'todos':
            query = """
            SELECT ANIVERSARIO.NOME, ANIVERSARIO.NASCIMENTO 
            FROM ANIVERSARIO 
            JOIN GRUPO ON ANIVERSARIO.ID_ANI_GRUPO = GRUPO.ID_GRUPO
            WHERE ANIVERSARIO.ID_ANI_USER = %s AND GRUPO.ID_GRUPO = %s
            """
            cursor.execute(query, (usuario_id, grupo_selecionado))
        else:
            cursor.execute("SELECT NOME, NASCIMENTO FROM ANIVERSARIO WHERE ID_ANI_USER = %s", (usuario_id,))
        
        aniversarios = cursor.fetchall()

        eventos = [{
            'title': aniversario['NOME'],
            'start': aniversario['NASCIMENTO'].replace(year=datetime.now().year).strftime("%Y-%m-%d"),
            'allDay': True
        } for aniversario in aniversarios]

    finally:
        cursor.close()

    # Enviar a lista de eventos para o template
    return render_template('calendariopadrao.html', eventos=json.dumps(eventos), grupos=grupos)


@app.route('/adicionar_grupo', methods=['POST'])
def adicionar_grupo():
    # Get usuario id da sessão
    usuario_id = session.get('usuario_id')
    
    if request.method == 'POST':
        nome_grupo = request.form['nome_grupo']

        cursor = db.cursor()

        try:
            # Verifica se o grupo já existe
            cursor.execute("SELECT * FROM GRUPO WHERE NOME_GRUPO = %s AND ID_GRU_USER =	%s", (nome_grupo, usuario_id))
            grupo_existente = cursor.fetchone()

            if grupo_existente:
                flash("O grupo já existe.", "error")
                return redirect(url_for('grupos'))

            else:
                # Insere o novo grupo no banco de dados
                cursor.execute("INSERT INTO GRUPO (NOME_GRUPO, ID_GRU_USER) VALUES (%s,%s)", (nome_grupo,usuario_id))
                db.commit()
                cursor.close()
                flash("Novo grupo adicionado com sucesso.", "success")
                return redirect(url_for('grupos'))

        except mysql.connector.Error as err:
            flash(f"Erro de programação: {err}", "error")

@app.route('/grupos', methods=['GET', 'POST'])
def grupos():
    grupos=return_grupos()
    return render_template('grupos.html', grupos=grupos)


def return_grupos():
    cursor = db.cursor()
    usuario_id = session.get('usuario_id')  # Obtém o ID do usuário logado
    print("ID do usuário logado:", usuario_id) 
    cursor.execute("SELECT ID_GRUPO, NOME_GRUPO FROM GRUPO WHERE ID_GRU_USER = %s", (usuario_id,))
    grupos = cursor.fetchall()
    cursor.close() 
    
    return grupos


@app.route('/definicoes')
def definicoes():
    return render_template('definicoes.html', usuario_nome=session['usuario_nome'])

@app.route('/alterar_definicoes', methods=['POST'])
def alterar_definicoes():
    nova_senha = request.form['nova-password']
    confirmar_senha = request.form['confirmar-nova-password']

    if nova_senha != confirmar_senha:
        flash("As senhas não coincidem. Por favor, tente novamente.", "error")
        return redirect(url_for('definicoes'))

    try:
        usuario_id = session.get('usuario_id')
        cursor = db.cursor()
        cursor.execute("UPDATE USUARIO SET SENHA = %s WHERE ID_USER = %s", (nova_senha, usuario_id))
        db.commit()
        cursor.close()
        flash("Senha alterada com sucesso.", "success")
        return redirect(url_for('index'))
    except mysql.connector.Error as err:
        flash(f"Erro ao atualizar senha: {err}", "error")
        return redirect(url_for('definicoes'))

@app.route('/apoioaocliente')
def apoioaocliente():
    return render_template('apoioaocliente.html')

@app.route('/enviar_problema', methods=['POST'])
def enviar_problema():
    assunto_formulario = request.form['assunto']
    mensagem_formulario = request.form['mensagem']
    usuario_id = session.get('usuario_id')
    # Compor o assunto do e-mail com o ID do usuário
    assunto_email = f'ID do Usuário: {usuario_id}'

    # Configurar o corpo do e-mail com o assunto e a mensagem do formulário
    corpo_email = f'<p><strong>Assunto:</strong><br>{assunto_formulario}</p><p><strong>Mensagem:</strong><br>{mensagem_formulario}</p>'

    # Localização do arquivo que contém a senha
    caminho_arquivo_senha = "C:/Users/User/Desktop/happyday.txt"

    # Tente abrir o arquivo e ler a senha
    try:
        with open(caminho_arquivo_senha, 'r') as arquivo:
            senha = arquivo.read().strip()  # Ler o conteúdo do arquivo e remover espaços em branco extras
    except FileNotFoundError:
        flash("Falha no envio.", "error")
        return redirect(url_for('apoioaocliente'))

    # Configurar os detalhes do servidor SMTP e as credenciais do remetente
    remetente_email = 'joaofonseca19990@gmail.com'
    destinatario_email = 'josemalves1992@gmail.com'

    # Configurar o servidor SMTP do Gmail
    servidor_smtp = smtplib.SMTP('smtp.gmail.com', 587)
    servidor_smtp.starttls()

    # Faça login no servidor SMTP
    servidor_smtp.login(remetente_email, senha)

    # Compor o e-mail
    msg = MIMEMultipart()
    msg['From'] = remetente_email
    msg['To'] = destinatario_email
    msg['Subject'] = assunto_email

    # Adicionar corpo do e-mail
    msg.attach(MIMEText(corpo_email, 'html'))  # Definindo o tipo de conteúdo como HTML

    # Enviar o e-mail
    servidor_smtp.send_message(msg)

    # Fechar a conexão com o servidor SMTP
    servidor_smtp.quit()

    flash("Solicitação de suporte enviada com sucesso!", "success")
    return redirect(url_for('apoioaocliente'))

@app.route('/calendariolista', methods=['GET'])
def calendariolista():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('index'))

    grupo_selecionado = request.args.get('grupo')  # Obtém o parâmetro de query 'grupo'

    cursor = db.cursor(dictionary=True)
    
    try:
        # Buscar os grupos da base de dados
        cursor.execute("SELECT ID_GRUPO, NOME_GRUPO FROM GRUPO WHERE ID_GRU_USER = %s", (usuario_id,))
        grupos = cursor.fetchall()

        # Filtrar aniversários por grupo, se um grupo foi selecionado
        if grupo_selecionado and grupo_selecionado != 'todos':
            query = """
            SELECT ANIVERSARIO.NOME, ANIVERSARIO.NASCIMENTO 
            FROM ANIVERSARIO 
            JOIN GRUPO ON ANIVERSARIO.ID_ANI_GRUPO = GRUPO.ID_GRUPO
            WHERE ANIVERSARIO.ID_ANI_USER = %s AND GRUPO.ID_GRUPO = %s
            """
            cursor.execute(query, (usuario_id, grupo_selecionado))
        else:
            cursor.execute("SELECT NOME, NASCIMENTO FROM ANIVERSARIO WHERE ID_ANI_USER = %s", (usuario_id,))
        
        aniversarios = cursor.fetchall()

        eventos = [{
            'title': aniversario['NOME'],
            'start': aniversario['NASCIMENTO'].replace(year=datetime.now().year).strftime("%Y-%m-%d"),
            'allDay': True
        } for aniversario in aniversarios]

    finally:
        cursor.close()

    # Enviar a lista de eventos para o template
    return render_template('calendariolista.html', eventos=json.dumps(eventos), grupos=grupos)

if __name__ == '__main__':
    app.run(debug=True)
