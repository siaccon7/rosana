@echo off
REM Menu principal para Windows
cls

:menu
echo ========================================
echo   ANALISADOR DE DIVIDENDOS
echo ========================================
echo.
echo 1. Executar Analisador (Menu Completo)
echo 2. Adicionar Novos Dados
echo 3. Gerar Relatorio HTML
echo 4. Executar Demo Rapida
echo 5. Sair
echo.
echo ========================================
set /p opcao="Escolha uma opcao (1-5): "

if "%opcao%"=="1" goto analisador
if "%opcao%"=="2" goto adicionar
if "%opcao%"=="3" goto relatorio
if "%opcao%"=="4" goto demo
if "%opcao%"=="5" goto sair
goto menu

:analisador
cls
echo Executando Analisador...
echo.
python analisador_dividendos.py
pause
goto menu

:adicionar
cls
echo Adicionar Dados de Dividendos...
echo.
python adicionar_dividendos.py
pause
goto menu

:relatorio
cls
set /p arquivo="Digite o nome do arquivo CSV (ou Enter para exemplo): "
if "%arquivo%"=="" set arquivo=dividendos_exemplo.csv
echo Gerando relatorio HTML...
python gerador_relatorio_html.py %arquivo%
echo.
echo Relatorio gerado: relatorio_dividendos.html
echo Abra o arquivo no seu navegador!
pause
goto menu

:demo
cls
echo Executando Demonstracao...
echo.
python -c "from analisador_dividendos import AnalisadorDividendos; a = AnalisadorDividendos('dividendos_exemplo.csv'); a.imprimir_relatorio_console()"
echo.
pause
goto menu

:sair
echo.
echo Encerrando...
exit
