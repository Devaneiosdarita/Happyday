                                                   Happyday

Este é um aplicativo web desenvolvido em Flask para gerenciamento de aniversários. Ele permite que os usuários registrem aniversariantes, organizem-nos em grupos e visualizem os aniversários em um calendário. Além disso, o aplicativo oferece recursos como autenticação de usuários, envio de solicitações de suporte ao cliente e notificação por e-mail de aniversários do mês.

Configuração do Ambiente
Para executar este aplicativo localmente, siga estas etapas:

Pré-requisitos:

- Python (versão 3.6 ou superior) instalado em seu sistema.
- Um servidor MySQL em execução localmente ou em um host remoto.

Instalação de Dependências:

Instale as dependências listadas no arquivo requirements.txt utilizando o pip:

pip install -r requirements.txt

Configuração do Banco de Dados:

- Certifique-se de ter um banco de dados MySQL configurado.
- Edite as credenciais do banco de dados no arquivo app.py conforme necessário.
- Execute o script schema.sql no seu banco de dados MySQL para criar as tabelas necessárias.
- Execução do Aplicativo:

Após configurar o ambiente e o banco de dados, execute o aplicativo Flask:

python app.py

O aplicativo estará disponível em http://localhost:5000/.

Funcionalidades Principais
- Autenticação de Usuários
- Os usuários podem se registrar e fazer login em suas contas.
- Senhas são armazenadas de forma segura no banco de dados.
- Gerenciamento de Aniversários
- Os usuários podem adicionar aniversariantes, especificando seu nome, data de nascimento, grupo e observações.
- Os aniversariantes podem ser organizados em grupos personalizados.
- Visualização de Aniversários
- Os aniversários podem ser visualizados em formato de calendário ou lista.
- Os usuários podem filtrar os aniversários por grupo.
- Notificação por E-mail
- O sistema envia notificações por e-mail para os usuários com os aniversariantes do mês.
- O envio de e-mails é agendado para o primeiro dia de cada mês.
- Suporte ao Cliente
- Os usuários podem enviar solicitações de suporte através de um formulário.
- As solicitações de suporte são enviadas por e-mail para o administrador do sistema.

Desenvolvimento e Contribuição
Este projeto está aberto a contribuições. Se você deseja contribuir com novos recursos, correções de bugs ou melhorias de qualquer tipo, sinta-se à vontade para criar uma issue ou enviar um pull request.

Para mais informações, entre em contato com o desenvolvedor:

Desenvolvedor: Ana Rita, Franciellen Cruz, José Alves e Lorena Saracho
E-mail: 
    
    fs.cruz@hotmail.com
    lologoldner@gmail.com

Nota: Este aplicativo é fornecido "no estado em que se encontra", sem garantias de qualquer tipo. Use por sua própria conta e risco.