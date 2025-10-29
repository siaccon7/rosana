# 📊 Analisador de Dividendos e Investimentos

Sistema completo para análise, projeção e visualização de dividendos recebidos de investimentos.

## 🎯 Características

- **Análise Estatística Completa**: Estatísticas detalhadas sobre rendimentos e custódia
- **Projeções Futuras**: Múltiplos métodos de projeção (média simples, média móvel, crescimento linear e composto)
- **Visualizações Gráficas**: Gráficos interativos e profissionais
- **Relatórios HTML**: Relatórios web interativos com Chart.js
- **Análise por Categoria**: Breakdown detalhado por tipo de ativo
- **Interface Interativa**: Menu CLI amigável

## 📁 Estrutura de Arquivos

```
.
├── analisador_dividendos.py          # Programa principal
├── gerador_relatorio_html.py         # Gerador de relatórios HTML
├── dividendos_exemplo.csv            # Arquivo de exemplo
├── requirements.txt                  # Dependências Python
└── README_DIVIDENDOS.md             # Esta documentação
```

## 🚀 Instalação

### 1. Instalar Python

Certifique-se de ter Python 3.8 ou superior instalado:

```bash
python --version
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

Ou instale manualmente:

```bash
pip install pandas numpy matplotlib seaborn
```

## 📝 Formato dos Dados

O programa aceita arquivos CSV com as seguintes colunas:

| Coluna | Descrição | Tipo |
|--------|-----------|------|
| `Mes_Ano` | Mês e ano (ex: DEZ/2019) | String |
| `Vlr_Custodia` | Valor total em custódia | Float |
| `Acoes` | Dividendos de ações | Float |
| `BDRs` | Dividendos de BDRs | Float |
| `FIIs` | Dividendos de FIIs | Float |
| `ETFs` | Dividendos de ETFs | Float |
| `FIAGRO_FIDC` | Dividendos de FIAGRO-FIDC | Float |
| `FI_INFRA` | Dividendos de FI-INFRA | Float |
| `FIP` | Dividendos de FIP | Float |
| `DIR_Subscr` | Direitos de subscrição | Float |
| `BDR_ETF` | Dividendos de BDR de ETF | Float |
| `ETF_Renda_Fixa` | Dividendos de ETF Renda Fixa | Float |
| `FIAGRO_FII` | Dividendos de FIAGRO-FII | Float |
| `Retorno_Yield` | Yield percentual | Float |
| `Total_Rendimentos` | Total de rendimentos | Float |

### Exemplo de CSV:

```csv
Mes_Ano,Vlr_Custodia,Acoes,BDRs,FIIs,ETFs,FIAGRO_FIDC,FI_INFRA,FIP,DIR_Subscr,BDR_ETF,ETF_Renda_Fixa,FIAGRO_FII,Retorno_Yield,Total_Rendimentos
DEZ/2019,70249.8248169026,273.9,0,208,0,0,0,0,0,0,0,0,0.685980358322618,481.9
JAN/2020,137532.620295368,608.31,0,244,0,0,0,0,0,0,0,0,0.619714797965429,852.31
```

## 💻 Como Usar

### Uso Básico

Execute o programa principal:

```bash
python analisador_dividendos.py
```

O programa solicitará o caminho do arquivo CSV (pressione Enter para usar o arquivo de exemplo).

### Menu Interativo

O programa oferece as seguintes opções:

```
1. Exibir relatório completo no console
2. Gerar visualizações (gráficos)
3. Visualizar projeções futuras
4. Exportar relatório para JSON
5. Salvar gráficos em arquivos
0. Sair
```

### Gerar Relatório HTML

Para gerar um relatório HTML interativo:

```bash
python gerador_relatorio_html.py dividendos_exemplo.csv
```

Isso criará um arquivo `relatorio_dividendos.html` que pode ser aberto em qualquer navegador.

## 📊 Funcionalidades Detalhadas

### 1. Estatísticas Gerais

Calcula automaticamente:
- Período de análise
- Valor inicial e final em custódia
- Crescimento absoluto e percentual
- Total de dividendos recebidos
- Média e mediana de dividendos mensais
- Yield médio e mediano
- Maior e menor rendimento

### 2. Análise por Categoria

Agrupa dividendos por tipo de ativo:
- Total recebido por categoria
- Média mensal por categoria
- Percentual do total por categoria

### 3. Métodos de Projeção

#### Média Simples
Usa a média histórica de todos os rendimentos.

```python
analisador.projetar_dividendos(12, 'media_simples')
```

#### Média Móvel
Usa a média dos últimos 3 meses para projeção.

```python
analisador.projetar_dividendos(12, 'media_movel')
```

#### Crescimento Linear
Aplica regressão linear aos dados históricos.

```python
analisador.projetar_dividendos(12, 'crescimento_linear')
```

#### Crescimento Composto (Recomendado)
Calcula taxa de crescimento composto e projeta exponencialmente.

```python
analisador.projetar_dividendos(12, 'crescimento_composto')
```

### 4. Visualizações

O programa gera 4 gráficos principais:

1. **Evolução da Custódia**: Linha mostrando crescimento do valor em custódia
2. **Rendimentos Mensais**: Barras com dividendos recebidos por mês
3. **Yield Mensal**: Linha mostrando retorno percentual mensal
4. **Distribuição por Categoria**: Pizza com top 5 categorias

## 🔧 Uso Programático

Você pode usar as classes diretamente em seus scripts:

```python
from analisador_dividendos import AnalisadorDividendos

# Criar analisador
analisador = AnalisadorDividendos('meus_dividendos.csv')

# Obter estatísticas
stats = analisador.estatisticas_gerais()
print(f"Total de dividendos: R$ {stats['total_dividendos']:.2f}")

# Análise por categoria
categorias = analisador.analise_por_categoria()
print(categorias)

# Projeção para 24 meses
projecao = analisador.projetar_dividendos(24, 'crescimento_composto')
print(f"Projeção 24 meses: R$ {projecao['Total_Rendimentos_Projetado'].sum():.2f}")

# Gerar visualizações
analisador.visualizar_evolucao(salvar_fig=True)
analisador.visualizar_projecoes(24, salvar_fig=True)

# Exportar relatório JSON
relatorio = analisador.gerar_relatorio_completo(salvar_json=True)
```

## 📈 Exemplos de Análises

### Calcular ROI Anual

```python
analisador = AnalisadorDividendos('dividendos.csv')
stats = analisador.estatisticas_gerais()

roi_anual = (stats['total_dividendos'] / stats['custodia_inicial']) * 100
print(f"ROI Anual: {roi_anual:.2f}%")
```

### Comparar Categorias

```python
analise = analisador.analise_por_categoria()
top_categoria = analise.iloc[0]
print(f"Melhor categoria: {top_categoria['Categoria']}")
print(f"Total recebido: R$ {top_categoria['Total_Recebido']:.2f}")
```

### Projetar Renda Passiva Futura

```python
projecao_5_anos = analisador.projetar_dividendos(60, 'crescimento_composto')
renda_anual_projetada = projecao_5_anos['Total_Rendimentos_Projetado'].tail(12).sum()
print(f"Renda anual projetada (ano 5): R$ {renda_anual_projetada:.2f}")
```

## 📤 Exportação de Dados

### JSON

```bash
# Via menu interativo (opção 4)
# Ou programaticamente:
```

```python
analisador.gerar_relatorio_completo(salvar_json=True)
# Gera: relatorio_dividendos.json
```

### Gráficos PNG

```bash
# Via menu interativo (opção 5)
# Ou programaticamente:
```

```python
analisador.visualizar_evolucao(salvar_fig=True)
analisador.visualizar_projecoes(12, salvar_fig=True)
# Gera: analise_dividendos.png, projecoes_dividendos.png
```

### HTML Interativo

```bash
python gerador_relatorio_html.py meus_dados.csv
# Gera: relatorio_dividendos.html
```

## 🎨 Personalização

### Alterar Cores dos Gráficos

Edite no arquivo `analisador_dividendos.py`:

```python
# Linha 18
plt.style.use('seaborn-v0_8-darkgrid')  # Altere para seu estilo preferido
sns.set_palette("husl")  # Altere a paleta de cores
```

### Adicionar Novas Métricas

Estenda a classe `AnalisadorDividendos`:

```python
class MeuAnalisador(AnalisadorDividendos):
    def calcular_sharpe_ratio(self):
        # Sua implementação
        pass
```

## 🐛 Solução de Problemas

### Erro: "No module named 'pandas'"

```bash
pip install pandas numpy matplotlib seaborn
```

### Erro ao importar dados

Verifique se:
- O arquivo CSV existe
- As colunas estão nomeadas corretamente
- Os valores numéricos não contêm texto
- O formato de data está em MÊS/ANO (ex: DEZ/2019)

### Gráficos não aparecem

Em ambientes sem interface gráfica (servidores):

```python
import matplotlib
matplotlib.use('Agg')  # Backend não-interativo
```

## 📊 Métricas Calculadas

| Métrica | Descrição | Fórmula |
|---------|-----------|---------|
| Yield Médio | Retorno percentual médio | `média(rendimentos / custódia) * 100` |
| Crescimento Custódia | Variação total da custódia | `(final - inicial) / inicial * 100` |
| ROI | Retorno sobre investimento | `total_dividendos / custodia_inicial * 100` |
| Média Mensal | Rendimento médio por mês | `total_dividendos / num_meses` |

## 🔮 Projeções

As projeções são baseadas em modelos estatísticos:

- **Curto Prazo (3-6 meses)**: Use média móvel
- **Médio Prazo (6-12 meses)**: Use crescimento composto
- **Longo Prazo (12+ meses)**: Use crescimento linear

**Importante**: Projeções são estimativas baseadas em dados históricos e não garantem resultados futuros.

## 🤝 Contribuindo

Para melhorias:
1. Adicione novos métodos de projeção
2. Implemente análises técnicas avançadas
3. Crie novos tipos de visualização
4. Adicione suporte a mais formatos de dados

## 📄 Licença

Este projeto é de código aberto.

## 👤 Autor

Criado para análise de investimentos pessoais.

## 📞 Suporte

Para dúvidas ou problemas:
- Verifique a documentação acima
- Revise os exemplos incluídos
- Teste com o arquivo `dividendos_exemplo.csv`

## 🎓 Aprendizado

Este projeto usa:
- **Pandas**: Manipulação de dados
- **NumPy**: Cálculos numéricos
- **Matplotlib**: Visualização de dados
- **Seaborn**: Gráficos estatísticos
- **Chart.js**: Gráficos web interativos

---

**Dica**: Mantenha seus dados atualizados mensalmente para melhores projeções!
