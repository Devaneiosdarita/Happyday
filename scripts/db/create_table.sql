CREATE TABLE USUARIO (
	ID_USER 		INT PRIMARY KEY AUTO_INCREMENT, 
	NOME	 		VARCHAR(255) NOT NULL,
	EMAIL 			VARCHAR(300) UNIQUE NOT NULL,
	SENHA 			VARCHAR(255) NOT NULL CHECK (senha REGEXP '[a-zA-Z]' AND senha REGEXP '[0-9]')
	);

CREATE TABLE ANIVERSARIO (
	ID_ANIVERSARIO 	INT PRIMARY KEY AUTO_INCREMENT, 
	NOME 			VARCHAR(255) NOT NULL,
	NASCIMENTO		DATE NOT NULL,
	ID_ANI_GRUPO	INT,
	FOREIGN KEY (ID_ANI_GRUPO) REFERENCES GRUPO (ID_GRUPO),
	ID_ANI_USER			INT,
	FOREIGN KEY (ID_ANI_USER) REFERENCES USUARIO (ID_USER)
	);
	
CREATE TABLE GRUPO (
	ID_GRUPO 		INT PRIMARY KEY AUTO_INCREMENT, 
	NOME_GRUPO 		VARCHAR(255) NOT NULL,
	ID_GRU_USER		INT,
	FOREIGN KEY (ID_GRU_USER) REFERENCES USUARIO (ID_USER)
	);
