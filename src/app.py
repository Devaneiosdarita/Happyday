from flask import Flask, render_template, request, redirect, url_for, flash, session
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
    
@app.route('/aniversariante')
def aniversariante():
    return render_template('aniversariante.html')

@app.route('/calendariopadrao')
def calendariopadrao():
    return render_template('calendariopadrao.html')

@app.route('/grupos')
def grupos():
    return render_template('grupos.html')

@app.route('/definicoes')
def definicoes():
    return render_template('definicoes.html')

@app.route('/apoioaocliente')
def apoioaocliente():
    return render_template('apoioaocliente.html')

@app.route('/calendariolista')
def calendariolista():
    return render_template('calendariolista.html')

if __name__ == '__main__':
    app.run(debug=True)
