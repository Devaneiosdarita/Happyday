from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

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
    return render_template('new_user.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    cursor = db.cursor()

    try:
        # Inserir novo usuário no banco de dados
        cursor.execute("INSERT INTO USUARIO (NOME, EMAIL, SENHA) VALUES (%s, %s, %s)", (nome, email, senha))
        db.commit()
        cursor.close()
        return redirect(url_for('index'))
    
    except mysql.connector.Error as err:
        return f"Erro de programação: {err}"


    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
