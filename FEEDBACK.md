# Feedback das Aulas 01 e 02

Na Aula 01 você montou a API de miniaturas com listagem, busca, filtro por marca, cadastro, atualização e remoção. O GET traz `marca_nome`, mas POST e PUT não; devolve esse campo também para manter o mesmo JSON. A Aula 02 ainda não foi feita: o app continua com `sqlite3` e SQL escrito na mão. Cria os modelos `Marca` e `Miniatura`, liga a miniatura à marca pela chave estrangeira e passa as consultas para `db.session`, mantendo as rotas e respostas. Inclui `Flask-SQLAlchemy` no requirements.
