@echo off
REM Script de instalacao e execucao para Windows
REM Analisador de Dividendos

echo ========================================
echo   Analisador de Dividendos - Windows
echo ========================================
echo.

REM Verificar se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo.
    echo Por favor, instale Python de: https://www.python.org/downloads/
    echo IMPORTANTE: Marque "Add Python to PATH" durante instalacao
    echo.
    pause
    exit /b 1
)

echo [OK] Python encontrado!
echo.

REM Instalar dependencias
echo Instalando dependencias...
pip install pandas numpy matplotlib seaborn --quiet --disable-pip-version-check
if errorlevel 1 (
    echo ERRO ao instalar dependencias!
    pause
    exit /b 1
)

echo [OK] Dependencias instaladas!
echo.

echo ========================================
echo   Instalacao concluida com sucesso!
echo ========================================
echo.
echo Programas disponiveis:
echo.
echo 1. python analisador_dividendos.py
echo    (Menu interativo completo)
echo.
echo 2. python adicionar_dividendos.py
echo    (Adicionar seus dados)
echo.
echo 3. python gerador_relatorio_html.py dividendos_exemplo.csv
echo    (Gerar relatorio HTML)
echo.
echo ========================================
pause
