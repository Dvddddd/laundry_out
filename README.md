# Laundry Out

Projeto de Lavanderia desenvolvido em Django.

## Preparar o ambiente

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Usar SQLite

Sem criar um arquivo `.env`, o projeto usa SQLite automaticamente:

```bash
python manage.py migrate
python manage.py runserver
```

O arquivo `db.sqlite3` é local e não é enviado ao GitHub.

## Usar PostgreSQL

Copie `.env.example` para `.env`, informe a senha do usuário do banco e mantenha
`DB_ENGINE=postgresql`. Depois execute:

```bash
python manage.py migrate
python manage.py runserver
```

Para voltar ao SQLite, use `DB_ENGINE=sqlite` no `.env` ou remova o arquivo.
