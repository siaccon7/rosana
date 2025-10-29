#!/usr/bin/env python3
"""
Gerador de Relatório HTML Interativo
Cria visualização web interativa dos dados de dividendos
"""

import pandas as pd
import json
from analisador_dividendos import AnalisadorDividendos
import base64
from io import BytesIO
import matplotlib.pyplot as plt


def gerar_html_interativo(arquivo_csv: str, arquivo_saida: str = 'relatorio_dividendos.html'):
    """
    Gera relatório HTML interativo com gráficos e análises

    Args:
        arquivo_csv: Caminho para arquivo CSV com dados
        arquivo_saida: Nome do arquivo HTML de saída
    """
    # Criar analisador
    analisador = AnalisadorDividendos(arquivo_csv)
    stats = analisador.estatisticas_gerais()
    analise_cat = analisador.analise_por_categoria()
    crescimento = analisador.calcular_crescimento_mensal()
    projecoes = analisador.projetar_dividendos(12, 'crescimento_composto')

    # Gerar gráficos em base64
    graficos = gerar_graficos_base64(analisador)

    # Template HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Dividendos</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        .card {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }}
        .stat-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 8px;
            padding: 1.5rem;
            text-align: center;
        }}
        .stat-value {{
            font-size: 2rem;
            font-weight: bold;
            margin: 0.5rem 0;
        }}
        .stat-label {{
            font-size: 0.875rem;
            opacity: 0.9;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
        }}
        th {{
            background-color: #f3f4f6;
            font-weight: 600;
        }}
        tr:hover {{
            background-color: #f9fafb;
        }}
    </style>
</head>
<body class="p-4">
    <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <div class="card">
            <h1 class="text-4xl font-bold text-gray-800 mb-2">📊 Relatório de Análise de Dividendos</h1>
            <p class="text-gray-600">Período: {stats['periodo_inicial']} até {stats['periodo_final']} ({stats['total_meses']} meses)</p>
        </div>

        <!-- Estatísticas Principais -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <div class="stat-box">
                <div class="stat-label">Custódia Atual</div>
                <div class="stat-value">R$ {stats['custodia_final']:,.2f}</div>
                <div class="text-sm mt-2">
                    {'+' if stats['crescimento_custodia_pct'] > 0 else ''}{stats['crescimento_custodia_pct']:.2f}% desde início
                </div>
            </div>

            <div class="stat-box">
                <div class="stat-label">Total Dividendos</div>
                <div class="stat-value">R$ {stats['total_dividendos']:,.2f}</div>
                <div class="text-sm mt-2">
                    R$ {stats['media_dividendos_mes']:,.2f}/mês
                </div>
            </div>

            <div class="stat-box">
                <div class="stat-label">Yield Médio</div>
                <div class="stat-value">{stats['yield_medio']:.3f}%</div>
                <div class="text-sm mt-2">
                    Mediana: {stats['yield_mediano']:.3f}%
                </div>
            </div>

            <div class="stat-box">
                <div class="stat-label">Crescimento</div>
                <div class="stat-value">R$ {stats['crescimento_custodia']:,.0f}</div>
                <div class="text-sm mt-2">
                    Variação total
                </div>
            </div>
        </div>

        <!-- Gráficos -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div class="card">
                <h2 class="text-2xl font-bold text-gray-800 mb-4">Evolução da Custódia</h2>
                <canvas id="chartCustodia"></canvas>
            </div>

            <div class="card">
                <h2 class="text-2xl font-bold text-gray-800 mb-4">Rendimentos Mensais</h2>
                <canvas id="chartRendimentos"></canvas>
            </div>

            <div class="card">
                <h2 class="text-2xl font-bold text-gray-800 mb-4">Yield Mensal</h2>
                <canvas id="chartYield"></canvas>
            </div>

            <div class="card">
                <h2 class="text-2xl font-bold text-gray-800 mb-4">Distribuição por Categoria</h2>
                <canvas id="chartCategorias"></canvas>
            </div>
        </div>

        <!-- Tabela de Análise por Categoria -->
        <div class="card mt-6">
            <h2 class="text-2xl font-bold text-gray-800 mb-4">📈 Análise por Categoria</h2>
            <div class="overflow-x-auto">
                <table>
                    <thead>
                        <tr>
                            <th>Categoria</th>
                            <th>Total Recebido</th>
                            <th>Média Mensal</th>
                            <th>% do Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {gerar_linhas_tabela_categorias(analise_cat)}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Projeções -->
        <div class="card mt-6">
            <h2 class="text-2xl font-bold text-gray-800 mb-4">🔮 Projeções (12 meses)</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div class="bg-blue-50 p-4 rounded-lg">
                    <div class="text-sm text-gray-600">Rendimento Projetado</div>
                    <div class="text-2xl font-bold text-blue-600">R$ {projecoes['Total_Rendimentos_Projetado'].sum():,.2f}</div>
                </div>
                <div class="bg-green-50 p-4 rounded-lg">
                    <div class="text-sm text-gray-600">Custódia Projetada</div>
                    <div class="text-2xl font-bold text-green-600">R$ {projecoes['Vlr_Custodia_Projetado'].iloc[-1]:,.2f}</div>
                </div>
                <div class="bg-purple-50 p-4 rounded-lg">
                    <div class="text-sm text-gray-600">Yield Médio Projetado</div>
                    <div class="text-2xl font-bold text-purple-600">{projecoes['Yield_Projetado'].mean():.3f}%</div>
                </div>
            </div>

            <canvas id="chartProjecoes"></canvas>
        </div>

        <!-- Tabela de Crescimento Mensal -->
        <div class="card mt-6">
            <h2 class="text-2xl font-bold text-gray-800 mb-4">📊 Crescimento Mensal</h2>
            <div class="overflow-x-auto">
                <table>
                    <thead>
                        <tr>
                            <th>Mês/Ano</th>
                            <th>Custódia</th>
                            <th>Rendimentos</th>
                            <th>Cresc. Custódia</th>
                            <th>Cresc. Rendimentos</th>
                        </tr>
                    </thead>
                    <tbody>
                        {gerar_linhas_tabela_crescimento(crescimento)}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        // Dados para gráficos
        const dados = {json.dumps({
            'datas': analisador.df['Mes_Ano'].tolist(),
            'custodia': analisador.df['Vlr_Custodia'].tolist(),
            'rendimentos': analisador.df['Total_Rendimentos'].tolist(),
            'yield': analisador.df['Retorno_Yield'].tolist(),
            'categorias': analise_cat['Categoria'].tolist(),
            'categorias_valores': analise_cat['Total_Recebido'].tolist(),
            'projecoes_datas': projecoes['Mes_Ano'].tolist(),
            'projecoes_rendimentos': projecoes['Total_Rendimentos_Projetado'].tolist(),
        })};

        // Configuração comum dos gráficos
        const chartOptions = {{
            responsive: true,
            maintainAspectRatio: true,
            plugins: {{
                legend: {{
                    display: true,
                    position: 'top',
                }}
            }}
        }};

        // Gráfico de Custódia
        new Chart(document.getElementById('chartCustodia'), {{
            type: 'line',
            data: {{
                labels: dados.datas,
                datasets: [{{
                    label: 'Valor em Custódia (R$)',
                    data: dados.custodia,
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.4
                }}]
            }},
            options: chartOptions
        }});

        // Gráfico de Rendimentos
        new Chart(document.getElementById('chartRendimentos'), {{
            type: 'bar',
            data: {{
                labels: dados.datas,
                datasets: [{{
                    label: 'Rendimentos Mensais (R$)',
                    data: dados.rendimentos,
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderColor: 'rgb(54, 162, 235)',
                    borderWidth: 1
                }}]
            }},
            options: chartOptions
        }});

        // Gráfico de Yield
        new Chart(document.getElementById('chartYield'), {{
            type: 'line',
            data: {{
                labels: dados.datas,
                datasets: [{{
                    label: 'Yield Mensal (%)',
                    data: dados.yield,
                    borderColor: 'rgb(255, 159, 64)',
                    backgroundColor: 'rgba(255, 159, 64, 0.2)',
                    tension: 0.4
                }}]
            }},
            options: chartOptions
        }});

        // Gráfico de Categorias
        new Chart(document.getElementById('chartCategorias'), {{
            type: 'doughnut',
            data: {{
                labels: dados.categorias,
                datasets: [{{
                    label: 'Rendimentos por Categoria',
                    data: dados.categorias_valores,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.6)',
                        'rgba(54, 162, 235, 0.6)',
                        'rgba(255, 206, 86, 0.6)',
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(153, 102, 255, 0.6)',
                        'rgba(255, 159, 64, 0.6)',
                    ]
                }}]
            }},
            options: chartOptions
        }});

        // Gráfico de Projeções
        new Chart(document.getElementById('chartProjecoes'), {{
            type: 'line',
            data: {{
                labels: [...dados.datas, ...dados.projecoes_datas],
                datasets: [
                    {{
                        label: 'Histórico',
                        data: [...dados.rendimentos, ...Array(dados.projecoes_datas.length).fill(null)],
                        borderColor: 'rgb(75, 192, 192)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    }},
                    {{
                        label: 'Projeção',
                        data: [...Array(dados.datas.length).fill(null), ...dados.projecoes_rendimentos],
                        borderColor: 'rgb(255, 99, 132)',
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderDash: [5, 5]
                    }}
                ]
            }},
            options: chartOptions
        }});
    </script>
</body>
</html>
"""

    # Salvar HTML
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\n✓ Relatório HTML gerado: {arquivo_saida}")
    return arquivo_saida


def gerar_linhas_tabela_categorias(df):
    """Gera linhas HTML para tabela de categorias"""
    linhas = ""
    for _, row in df.iterrows():
        if row['Total_Recebido'] > 0:
            linhas += f"""
                        <tr>
                            <td class="font-medium">{row['Categoria']}</td>
                            <td>R$ {row['Total_Recebido']:,.2f}</td>
                            <td>R$ {row['Media_Mensal']:,.2f}</td>
                            <td>{row['Percentual_Total']:.2f}%</td>
                        </tr>
            """
    return linhas


def gerar_linhas_tabela_crescimento(df):
    """Gera linhas HTML para tabela de crescimento"""
    linhas = ""
    for _, row in df.iterrows():
        cresc_custodia = row['Crescimento_Custodia']
        cresc_rend = row['Crescimento_Rendimentos']

        cor_custodia = 'text-green-600' if cresc_custodia > 0 else 'text-red-600' if cresc_custodia < 0 else ''
        cor_rend = 'text-green-600' if cresc_rend > 0 else 'text-red-600' if cresc_rend < 0 else ''

        linhas += f"""
                        <tr>
                            <td class="font-medium">{row['Mes_Ano']}</td>
                            <td>R$ {row['Vlr_Custodia']:,.2f}</td>
                            <td>R$ {row['Total_Rendimentos']:,.2f}</td>
                            <td class="{cor_custodia}">{cresc_custodia:.2f}%</td>
                            <td class="{cor_rend}">{cresc_rend:.2f}%</td>
                        </tr>
        """
    return linhas


def gerar_graficos_base64(analisador):
    """Gera gráficos em formato base64 para embedding"""
    graficos = {}

    # Gráfico 1: Evolução
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(analisador.df['Data'], analisador.df['Vlr_Custodia'])
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=150)
    buffer.seek(0)
    graficos['evolucao'] = base64.b64encode(buffer.read()).decode()
    plt.close()

    return graficos


if __name__ == "__main__":
    import sys

    arquivo = sys.argv[1] if len(sys.argv) > 1 else 'dividendos_exemplo.csv'
    gerar_html_interativo(arquivo)
