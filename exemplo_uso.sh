#!/bin/bash
# Script de exemplo para usar o Analisador de Dividendos

echo "=================================="
echo "  Analisador de Dividendos - Demo"
echo "=================================="
echo ""

# 1. Verificar se as dependências estão instaladas
echo "1. Verificando dependências..."
python3 -c "import pandas, numpy, matplotlib, seaborn" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ Todas as dependências estão instaladas!"
else
    echo "❌ Instalando dependências..."
    pip install -q pandas numpy matplotlib seaborn
    echo "✓ Dependências instaladas!"
fi

echo ""
echo "2. Executando análise com dados de exemplo..."
echo ""

# 2. Executar análise programática
python3 << 'EOF'
from analisador_dividendos import AnalisadorDividendos

print("="*80)
print("ANÁLISE RÁPIDA - DADOS DE EXEMPLO")
print("="*80)

# Carregar dados
analisador = AnalisadorDividendos('dividendos_exemplo.csv')

# Estatísticas
stats = analisador.estatisticas_gerais()
print(f"\n📊 Resumo:")
print(f"   Período: {stats['periodo_inicial']} a {stats['periodo_final']}")
print(f"   Custódia atual: R$ {stats['custodia_final']:,.2f}")
print(f"   Total dividendos: R$ {stats['total_dividendos']:,.2f}")
print(f"   Yield médio: {stats['yield_medio']:.3f}%")

# Projeção
print(f"\n🔮 Projeção (12 meses):")
proj = analisador.projetar_dividendos(12, 'crescimento_composto')
print(f"   Rendimento projetado: R$ {proj['Total_Rendimentos_Projetado'].sum():,.2f}")
print(f"   Custódia projetada: R$ {proj['Vlr_Custodia_Projetado'].iloc[-1]:,.2f}")

print("\n" + "="*80)
print("✓ Análise concluída!")
print("="*80)
EOF

echo ""
echo "3. Gerando relatório HTML..."
python3 gerador_relatorio_html.py dividendos_exemplo.csv 2>/dev/null
echo "   ✓ Relatório salvo em: relatorio_dividendos.html"

echo ""
echo "=================================="
echo "  Próximos passos:"
echo "=================================="
echo "1. Execute: python3 analisador_dividendos.py"
echo "   (menu interativo completo)"
echo ""
echo "2. Execute: python3 adicionar_dividendos.py"
echo "   (para adicionar seus dados)"
echo ""
echo "3. Abra: relatorio_dividendos.html"
echo "   (no seu navegador)"
echo "=================================="
