# Trees Everywhere - Projeto Django para Youshop

Este projeto é um teste de conhecimento que faz parte do processo seletivo da FPF e visa demonstrar minhas habilidades em Django.

## Funcionalidades Principais

1. **CRUD de Estudantes:** Usuários podem criar, visualizar, editar e deletar matrículas de estudantes.

2. **API:** Os usuários podem também realizar esse CRUD via API REST.

3. **Administração via Django Admin:** A criação de usuários e estudantes podem ser realizadas pelo Django Admin.

## Requisitos 

1. **Python:** >= 3.11.4

2. **Postgres:**

3. **Docker (Opcional):**

## Instalação (Docker)
- Instalar o <b><a style="color: #337BEA;" href="https://www.docker.com/">Docker</a></b>
- Instalar o <b><a href="https://docs.docker.com/compose/install/" style="color: #337BEA;">Docker Compose</a></b>
- Fazer o Clone do repositorio
- No terminal:

  ```bash
    docker-compose up --build
    ```
  
- Recomendável criar um usuário superuser no terminal do docker

  ```bash
        python manage.py createsuperuser
        ```

## Instalação Manual

Para instalar e executar este projeto localmente, siga os passos abaixo:

1. **Configuração do Ambiente Virtual:**

    ```bash
    python3.11 -m venv myenv
    source myenv/bin/activate  # No Windows use `myenv\Scripts\activate`
    ```

2. **Instalação das Dependências:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Configuração do Banco de Dados:**

    - Configure as suas credenciais de banco de dados no arquivo `server_root/settings.py` na seção `DATABASES`.
    - Execute as migrações necessárias:

        ```bash
        python manage.py makemigrations
        python manage.py migrate
        ```

4. **Criar Superusuário:**

    - Crie um superusuário para acessar todas as funcionalidades do admin:

        ```bash
        python manage.py createsuperuser
        ```

7. **Executar o Servidor de Desenvolvimento:**

    ```bash
    python manage.py runserver
    ```
    
## Estudantes API

Esta API permite a criação, listagem, atualização e exclusão de informações sobre estudantes. A API é baseada no Django REST Framework e oferece suporte a operações CRUD (Create, Read, Update, Delete) para o modelo `Estudante`.

### Endpoints

#### 1. **Listar Estudantes**
   - **Método**: `GET`
   - **URL**: `/api/estudantes/`
   - **Descrição**: Retorna uma lista de todos os estudantes cadastrados.
   - **Exemplo de resposta**:
     ```json
     [
       {
         "id": 1,
         "nome": "João Silva",
         "matricula": "ES1234567",
         "endereco": "Rua das Flores, 123",
         "telefone": "(11) 99999-9999",
         "cursos": ["Matemática", "Física"]
       },
       ...
     ]
     ```

#### 2. **Detalhes de um Estudante**
   - **Método**: `GET`
   - **URL**: `/api/estudantes/{id}/`
   - **Descrição**: Retorna os detalhes de um estudante específico.
   - **Exemplo de resposta**:
     ```json
     {
       "id": 1,
       "nome": "João Silva",
       "matricula": "ES1234567",
       "endereco": "Rua das Flores, 123",
       "telefone": "(11) 99999-9999",
       "cursos": ["Matemática", "Física"]
     }
     ```

#### 3. **Criar Estudante**
   - **Método**: `POST`
   - **URL**: `/api/estudantes/`
   - **Descrição**: Cria um novo estudante com os dados fornecidos.
   - **Corpo da requisição**:
     ```json
     {
       "nome": "Maria Souza",
       "endereco": "Rua dos Bobos, 0",
       "telefone": "(21) 88888-8888",
       "cursos": [1, 2]
     }
     ```
   - **Exemplo de resposta**:
     ```json
     {
       "id": 2,
       "nome": "Maria Souza",
       "matricula": "ES7654321",
       "endereco": "Rua dos Bobos, 0",
       "telefone": "(21) 88888-8888",
       "cursos": ["Química", "Biologia"]
     }
     ```

#### 4. **Atualizar Estudante**
   - **Método**: `PUT` ou `PATCH`
   - **URL**: `/api/estudantes/{id}/`
   - **Descrição**: Atualiza os dados de um estudante existente.
   - **Corpo da requisição**:
     ```json
     {
       "nome": "Maria Souza",
       "endereco": "Rua Nova, 456",
       "telefone": "(21) 88888-8888",
       "cursos": [3]
     }
     ```
   - **Exemplo de resposta**:
     ```json
     {
       "id": 2,
       "nome": "Maria Souza",
       "matricula": "ES7654321",
       "endereco": "Rua Nova, 456",
       "telefone": "(21) 88888-8888",
       "cursos": ["Física"]
     }
     ```

#### 5. **Excluir Estudante**
   - **Método**: `DELETE`
   - **URL**: `/api/estudantes/{id}/`
   - **Descrição**: Remove um estudante pelo ID.

