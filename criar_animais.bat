
@echo off
echo Criando tabela 'animais' no banco adotantes.db...
sqlite3 adotantes.db < criar_tabela_animais.sql
echo Tabela criada com sucesso!
pause
