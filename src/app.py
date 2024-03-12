from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import mysql.connector

app = Flask(__name__, static_folder='static')
app.secret_key = 'aviso'


# Conectar ao banco de dados MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
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

            # Insere o novo aniversariante no banco de dados
            cursor.execute("INSERT INTO ANIVERSARIO (NOME, ID_ANI_GRUPO, NASCIMENTO, OBSERVACOES) VALUES (%s, %s, %s, %s)", (nome, grupo, data_nascimento, observacoes))
            db.commit()

            flash("Aniversariante adicionado com sucesso.", "success")
            return redirect(url_for('aniversariante'))

        except mysql.connector.Error as err:
            return f"Erro de programação: {err}"

    return render_template('aniversariante.html')

    

@app.route('/calendariopadrao', methods=['GET', 'POST'])
def calendariopadrao():
    

    return render_template('calendariopadrao.html')

@app.route('/adicionar_grupo', methods=['POST'])
def adicionar_grupo():
    # Get usuario id da sessão
    usuario_id = session.get('usuario_id')
    
    if request.method == 'POST':
        nome_grupo = request.form['nome_grupo']

        cursor = db.cursor()

        try:
            # Verifica se o grupo já existe
            cursor.execute("SELECT * FROM GRUPO WHERE NOME_GRUPO = %s", (nome_grupo,))
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
    cursor = db.cursor()
    usuario_id = session.get('usuario_id')  # Obtém o ID do usuário logado
    cursor.execute("SELECT * FROM GRUPO WHERE ID_GRU_USER = %s", (usuario_id,))
    grupos = cursor.fetchall()
    cursor.close()
    
    return render_template('grupos.html', grupos=grupos)


@app.route('/definicoes')
def definicoes():
    return render_template('definicoes.html')

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

@app.route('/calendariolista')
def calendariolista():
    return render_template('calendariolista.html')

if __name__ == '__main__':
    app.run(debug=True)
