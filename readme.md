# Segurança Computacional - Trabalho Seminário

## Passos para rodar projeto

- Inicialize um embiente de desenvolvimento em python

```bash
python3 -m venv venv
source venv/bin/activate
```

- Instale as dependências necessárias

```bash
pip install -r requirements.txt
```

- Crie as variaveis de ambiente
  Para este projeto, é necessário um banco de dados POSTGRES,
  então será necessário criar um arquivo .env e colocar nele um DATABASE_URL valida

Primeiro, crie o arquivo .env

```bash
touch .env
```

Agora, preencha o arquivo .env com uma DATABASE_URL

```shell
DATABASE_URL="postgresql://neondb_owner:npg_C2uDtqlYp0kx@ep-misty-rice-a57r1o5e-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"
```

Esta é uma database que estou liberando temporariamente para demonstracao do projeto

- Rodando projeto

```bash
fastapi dev app/main.py
```

Agora, rode o front com o back e interaja com o sistema :)
