# Laundry Out

Projeto de Lavanderia desenvolvido em Django.

## Preparar o ambiente

Crie o ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente no Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

No Linux ou macOS, use:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

## Usar SQLite

Sem criar um arquivo `.env`, o projeto usa SQLite automaticamente:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

O arquivo `db.sqlite3` é local e não é enviado ao GitHub.
O comando `createsuperuser` é necessário apenas na primeira execução desse banco.

## Usar PostgreSQL

Copie `.env.example` para `.env`, informe a senha do usuário do banco e mantenha
`DB_ENGINE=postgresql`. Depois execute:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Para voltar ao SQLite, use `DB_ENGINE=sqlite` no `.env` ou remova o arquivo.
O comando `createsuperuser` é necessário apenas na primeira execução desse banco.

Com o servidor iniciado, acesse:

```text
http://127.0.0.1:8000/entrar/
```
