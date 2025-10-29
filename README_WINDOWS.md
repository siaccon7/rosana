# 🪟 Guia para Windows - Analisador de Dividendos

## 📋 Pré-requisitos

### 1. Instalar Python

1. Acesse: https://www.python.org/downloads/
2. Baixe Python 3.11 ou superior
3. **IMPORTANTE:** Marque "Add Python to PATH" durante instalação
4. Clique em "Install Now"

### 2. Verificar Instalação

Abra o Prompt de Comando (Win + R → digite `cmd` → Enter) e execute:

```cmd
python --version
```

Deve mostrar algo como: `Python 3.11.x`

---

## 🚀 Instalação do Programa

### Método 1: Download Direto (Mais Fácil)

1. Baixe os arquivos do GitHub:
   - Acesse: https://github.com/siaccon7/rosana
   - Branch: `claude/create-dividend-input-program-011CUaa8qiHscPAwTsNTjg9L`
   - Clique em "Code" → "Download ZIP"

2. Extraia o ZIP em uma pasta, exemplo:
   ```
   C:\dividendos\
   ```

3. Abra o Prompt de Comando nessa pasta:
   - Win + R → digite `cmd` → Enter
   - Digite: `cd C:\dividendos`

4. Execute a instalação:
   ```cmd
   INSTALAR_WINDOWS.bat
   ```

### Método 2: Usando Git

```cmd
git clone https://github.com/siaccon7/rosana.git
cd rosana
git checkout claude/create-dividend-input-program-011CUaa8qiHscPAwTsNTjg9L
INSTALAR_WINDOWS.bat
```

---

## 💻 Como Usar

### Forma Mais Fácil: Menu Interativo

Duplo clique no arquivo:
```
EXECUTAR.bat
```

Ou no Prompt de Comando:
```cmd
EXECUTAR.bat
```

### Comandos Individuais

#### 1. Analisador Completo
```cmd
python analisador_dividendos.py
```

#### 2. Adicionar Dados
```cmd
python adicionar_dividendos.py
```

#### 3. Gerar Relatório HTML
```cmd
python gerador_relatorio_html.py dividendos_exemplo.csv
```

---

## 📂 Estrutura de Pastas no Windows

```
C:\dividendos\
│
├── analisador_dividendos.py       ← Programa principal
├── adicionar_dividendos.py        ← Adicionar dados
├── gerador_relatorio_html.py      ← Gerar HTML
├── dividendos_exemplo.csv         ← Dados de exemplo
│
├── EXECUTAR.bat                   ← Menu Windows (clique duplo)
├── INSTALAR_WINDOWS.bat           ← Instalador Windows
│
├── requirements.txt               ← Dependências
├── README_DIVIDENDOS.md           ← Documentação completa
└── README_WINDOWS.md              ← Este arquivo
```

---

## 🎯 Primeiro Uso - Passo a Passo

### 1. Instalar Dependências (apenas primeira vez)

```cmd
cd C:\dividendos
pip install pandas numpy matplotlib seaborn
```

### 2. Testar com Dados de Exemplo

```cmd
python analisador_dividendos.py
```

- Pressione **Enter** quando pedir o arquivo (usa exemplo)
- Escolha opção **1** para ver relatório

### 3. Adicionar Seus Dados

```cmd
python adicionar_dividendos.py
```

- Digite nome do arquivo: `meus_dividendos.csv`
- Escolha opção **1** e preencha os dados

### 4. Gerar Relatório HTML

```cmd
python gerador_relatorio_html.py meus_dividendos.csv
```

- Abra `relatorio_dividendos.html` no navegador

---

## 🖱️ Usando com Duplo Clique

### Criar Atalho na Área de Trabalho

1. Clique com botão direito em `EXECUTAR.bat`
2. "Enviar para" → "Área de trabalho (criar atalho)"
3. Agora você pode executar com duplo clique!

### Associar Arquivos CSV ao Programa

Crie um arquivo `ANALISAR_CSV.bat`:

```batch
@echo off
python gerador_relatorio_html.py %1
start relatorio_dividendos.html
```

Depois arraste um arquivo CSV para este .bat!

---

## ❓ Problemas Comuns no Windows

### "python não é reconhecido..."

**Solução:**
- Reinstale Python marcando "Add Python to PATH"
- OU adicione manualmente ao PATH:
  1. Painel de Controle → Sistema → Configurações avançadas
  2. Variáveis de Ambiente
  3. PATH → Adicionar: `C:\Users\SeuUsuario\AppData\Local\Programs\Python\Python311`

### "No module named pandas"

**Solução:**
```cmd
pip install pandas numpy matplotlib seaborn
```

### Gráficos não aparecem

**Solução:**
- Instale backend adicional:
```cmd
pip install pillow
```

### Erro de encoding/caracteres

**Solução:**
- Abra arquivos CSV no Excel e salve com encoding UTF-8
- Ou use o programa `adicionar_dividendos.py` que já cria no formato correto

---

## 📊 Visualizar Relatórios

### Relatório HTML

Após gerar com:
```cmd
python gerador_relatorio_html.py dividendos_exemplo.csv
```

Abra o arquivo:
- Duplo clique em `relatorio_dividendos.html`
- OU arraste para o navegador

### Gráficos PNG

Para salvar gráficos:
1. Execute: `python analisador_dividendos.py`
2. Escolha opção **5**
3. Arquivos salvos:
   - `analise_dividendos.png`
   - `projecoes_dividendos.png`

---

## 🔧 Comandos Úteis no Windows

### Ver dados no Excel
```cmd
start dividendos_exemplo.csv
```

### Abrir pasta no Explorer
```cmd
explorer .
```

### Limpar tela
```cmd
cls
```

### Ver conteúdo do CSV
```cmd
type dividendos_exemplo.csv
```

---

## 🎨 Dicas para Windows

### 1. Use PowerShell (alternativa ao CMD)

PowerShell é mais moderno:
- Win + X → "Windows PowerShell"
- Mesmos comandos funcionam

### 2. Windows Terminal (Windows 11)

Melhor experiência:
- Instale da Microsoft Store
- Suporta abas e cores

### 3. Visual Studio Code

Para editar arquivos Python:
- Instale: https://code.visualstudio.com/
- Abra a pasta do projeto
- Extensão Python recomendada

---

## 📱 Atalhos Úteis

Crie um arquivo `ATALHOS.txt` na sua pasta:

```
Menu Principal:
  EXECUTAR.bat

Análise Rápida:
  python analisador_dividendos.py

Adicionar Dados:
  python adicionar_dividendos.py

Gerar HTML:
  python gerador_relatorio_html.py dividendos_exemplo.csv
```

---

## 🆘 Suporte

Se tiver problemas:

1. Verifique se Python está instalado: `python --version`
2. Verifique se está na pasta correta: `dir`
3. Reinstale dependências: `pip install -r requirements.txt`
4. Veja documentação completa: `README_DIVIDENDOS.md`

---

## ✅ Checklist de Instalação

- [ ] Python instalado (com PATH)
- [ ] Arquivos baixados do GitHub
- [ ] Dependências instaladas (`pip install ...`)
- [ ] Testado com dados de exemplo
- [ ] Relatório HTML gerado com sucesso

**Pronto para usar!** 🚀
