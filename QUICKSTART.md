# 🚀 Guia Rápido - Analisador de Dividendos

## Instalação Rápida

```bash
# 1. Instalar dependências
pip install pandas numpy matplotlib seaborn

# 2. Pronto para usar!
```

## Uso em 3 Passos

### 1️⃣ Preparar seus dados

Crie um arquivo CSV com seus dados de dividendos ou use o exemplo fornecido:

```bash
# Usar arquivo de exemplo
python analisador_dividendos.py
# Pressione Enter quando solicitar o arquivo

# OU adicionar seus próprios dados
python adicionar_dividendos.py
```

### 2️⃣ Gerar análises

```bash
python analisador_dividendos.py
```

Escolha no menu:
- **Opção 1**: Ver relatório completo
- **Opção 2**: Ver gráficos
- **Opção 3**: Ver projeções futuras
- **Opção 4**: Exportar para JSON
- **Opção 5**: Salvar gráficos

### 3️⃣ Gerar relatório HTML

```bash
python gerador_relatorio_html.py dividendos_exemplo.csv
```

Abra `relatorio_dividendos.html` no navegador!

## Exemplo de Uso Programático

```python
from analisador_dividendos import AnalisadorDividendos

# Carregar dados
analisador = AnalisadorDividendos('dividendos_exemplo.csv')

# Ver estatísticas
stats = analisador.estatisticas_gerais()
print(f"Total de dividendos: R$ {stats['total_dividendos']:.2f}")
print(f"Yield médio: {stats['yield_medio']:.3f}%")

# Projetar 12 meses
projecao = analisador.projetar_dividendos(12, 'crescimento_composto')
print(f"\nProjeção 12 meses: R$ {projecao['Total_Rendimentos_Projetado'].sum():.2f}")

# Gerar gráficos
analisador.visualizar_evolucao(salvar_fig=True)
analisador.visualizar_projecoes(12, salvar_fig=True)
```

## Estrutura do CSV

Seu arquivo CSV deve ter estas colunas:

```csv
Mes_Ano,Vlr_Custodia,Acoes,BDRs,FIIs,ETFs,FIAGRO_FIDC,FI_INFRA,FIP,DIR_Subscr,BDR_ETF,ETF_Renda_Fixa,FIAGRO_FII,Retorno_Yield,Total_Rendimentos
DEZ/2019,70249.82,273.9,0,208,0,0,0,0,0,0,0,0,0.686,481.9
JAN/2020,137532.62,608.31,0,244,0,0,0,0,0,0,0,0,0.620,852.31
```

## Comandos Úteis

### Adicionar novos dados interativamente
```bash
python adicionar_dividendos.py
```

### Ver relatório no terminal
```bash
python -c "
from analisador_dividendos import AnalisadorDividendos
a = AnalisadorDividendos('dividendos_exemplo.csv')
a.imprimir_relatorio_console()
"
```

### Exportar apenas projeções
```bash
python -c "
from analisador_dividendos import AnalisadorDividendos
a = AnalisadorDividendos('dividendos_exemplo.csv')
p = a.projetar_dividendos(24, 'crescimento_composto')
p.to_csv('projecoes.csv', index=False)
print('Projeções salvas em projecoes.csv')
"
```

### Gerar todos os gráficos de uma vez
```bash
python -c "
from analisador_dividendos import AnalisadorDividendos
a = AnalisadorDividendos('dividendos_exemplo.csv')
a.visualizar_evolucao(salvar_fig=True)
a.visualizar_projecoes(12, salvar_fig=True)
print('Gráficos salvos!')
"
```

## Dicas

- **Dados mínimos**: Recomendado ter pelo menos 6 meses de dados para projeções mais precisas
- **Atualização**: Adicione dados mensalmente para manter as análises atualizadas
- **Backup**: Mantenha backup do seu arquivo CSV
- **Formato de data**: Use sempre MÊS/ANO em maiúsculas (ex: JAN/2024)
- **Valores numéricos**: Use ponto (.) para decimais no CSV

## Problemas Comuns

### "No module named pandas"
```bash
pip install pandas numpy matplotlib seaborn
```

### Gráficos não aparecem
Se estiver em servidor sem interface gráfica, use `salvar_fig=True`:
```python
analisador.visualizar_evolucao(salvar_fig=True)
```

### Erro ao ler CSV
Verifique se:
- O arquivo existe
- As colunas estão nomeadas corretamente
- Não há linhas vazias
- Valores numéricos não contêm vírgulas (use ponto)

## Próximos Passos

1. Adicione seus dados reais usando `adicionar_dividendos.py`
2. Execute análises mensalmente
3. Compare projeções com resultados reais
4. Ajuste sua estratégia de investimentos

---

**Pronto!** Agora você tem um sistema completo de análise de dividendos funcionando.

Para documentação completa, veja: `README_DIVIDENDOS.md`
