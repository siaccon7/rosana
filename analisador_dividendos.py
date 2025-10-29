#!/usr/bin/env python3
"""
Analisador de Dividendos e Investimentos
Sistema completo para análise, projeção e visualização de dividendos recebidos
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import json
import warnings
warnings.filterwarnings('ignore')

# Configurações de visualização
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


class AnalisadorDividendos:
    """Classe principal para análise de dividendos"""

    def __init__(self, arquivo_csv: str):
        """
        Inicializa o analisador com dados de um arquivo CSV

        Args:
            arquivo_csv: Caminho para o arquivo CSV com dados de dividendos
        """
        self.df = pd.read_csv(arquivo_csv)
        self._processar_dados()

    def _processar_dados(self):
        """Processa e limpa os dados importados"""
        # Converter Mes_Ano para datetime
        self.df['Data'] = pd.to_datetime(self.df['Mes_Ano'], format='%b/%Y', errors='coerce')

        # Se falhar, tentar formato brasileiro
        if self.df['Data'].isna().any():
            meses_pt = {
                'JAN': '01', 'FEV': '02', 'MAR': '03', 'ABR': '04',
                'MAI': '05', 'JUN': '06', 'JUL': '07', 'AGO': '08',
                'SET': '09', 'OUT': '10', 'NOV': '11', 'DEZ': '12'
            }

            def converter_data_pt(mes_ano):
                try:
                    mes, ano = mes_ano.split('/')
                    mes_num = meses_pt.get(mes.upper(), '01')
                    return pd.to_datetime(f'{ano}-{mes_num}-01')
                except:
                    return pd.NaT

            self.df['Data'] = self.df['Mes_Ano'].apply(converter_data_pt)

        # Ordenar por data
        self.df = self.df.sort_values('Data').reset_index(drop=True)

        # Calcular colunas adicionais
        self.df['Mes'] = self.df['Data'].dt.month
        self.df['Ano'] = self.df['Data'].dt.year
        self.df['Yield_Decimal'] = self.df['Retorno_Yield'] / 100

    def estatisticas_gerais(self) -> Dict:
        """
        Calcula estatísticas gerais dos investimentos

        Returns:
            Dicionário com estatísticas
        """
        stats = {
            'periodo_inicial': self.df['Mes_Ano'].iloc[0],
            'periodo_final': self.df['Mes_Ano'].iloc[-1],
            'total_meses': len(self.df),
            'custodia_inicial': self.df['Vlr_Custodia'].iloc[0],
            'custodia_final': self.df['Vlr_Custodia'].iloc[-1],
            'crescimento_custodia': self.df['Vlr_Custodia'].iloc[-1] - self.df['Vlr_Custodia'].iloc[0],
            'crescimento_custodia_pct': ((self.df['Vlr_Custodia'].iloc[-1] / self.df['Vlr_Custodia'].iloc[0]) - 1) * 100,
            'total_dividendos': self.df['Total_Rendimentos'].sum(),
            'media_dividendos_mes': self.df['Total_Rendimentos'].mean(),
            'mediana_dividendos': self.df['Total_Rendimentos'].median(),
            'yield_medio': self.df['Retorno_Yield'].mean(),
            'yield_mediano': self.df['Retorno_Yield'].median(),
            'maior_rendimento': self.df['Total_Rendimentos'].max(),
            'menor_rendimento': self.df['Total_Rendimentos'].min(),
        }

        return stats

    def analise_por_categoria(self) -> pd.DataFrame:
        """
        Analisa dividendos recebidos por categoria de ativo

        Returns:
            DataFrame com análise por categoria
        """
        categorias = ['Acoes', 'BDRs', 'FIIs', 'ETFs', 'FIAGRO_FIDC',
                     'FI_INFRA', 'FIP', 'DIR_Subscr', 'BDR_ETF',
                     'ETF_Renda_Fixa', 'FIAGRO_FII']

        analise = []
        for cat in categorias:
            if cat in self.df.columns:
                total = self.df[cat].sum()
                media = self.df[cat].mean()
                percentual = (total / self.df['Total_Rendimentos'].sum()) * 100 if total > 0 else 0

                analise.append({
                    'Categoria': cat,
                    'Total_Recebido': total,
                    'Media_Mensal': media,
                    'Percentual_Total': percentual
                })

        return pd.DataFrame(analise).sort_values('Total_Recebido', ascending=False)

    def calcular_crescimento_mensal(self) -> pd.DataFrame:
        """
        Calcula crescimento mês a mês

        Returns:
            DataFrame com crescimento mensal
        """
        df_crescimento = self.df.copy()
        df_crescimento['Crescimento_Custodia'] = df_crescimento['Vlr_Custodia'].pct_change() * 100
        df_crescimento['Crescimento_Rendimentos'] = df_crescimento['Total_Rendimentos'].pct_change() * 100

        return df_crescimento[['Mes_Ano', 'Vlr_Custodia', 'Total_Rendimentos',
                               'Crescimento_Custodia', 'Crescimento_Rendimentos']]

    def projetar_dividendos(self, meses_futuros: int = 12, metodo: str = 'media_movel') -> pd.DataFrame:
        """
        Projeta dividendos futuros baseado em dados históricos

        Args:
            meses_futuros: Número de meses a projetar
            metodo: 'media_simples', 'media_movel', 'crescimento_linear', 'crescimento_composto'

        Returns:
            DataFrame com projeções
        """
        projecoes = []

        ultima_data = self.df['Data'].iloc[-1]
        ultima_custodia = self.df['Vlr_Custodia'].iloc[-1]

        if metodo == 'media_simples':
            rendimento_medio = self.df['Total_Rendimentos'].mean()
            yield_medio = self.df['Yield_Decimal'].mean()
            crescimento_custodia = 0

        elif metodo == 'media_movel':
            # Média móvel dos últimos 3 meses (ou menos se não houver dados)
            janela = min(3, len(self.df))
            rendimento_medio = self.df['Total_Rendimentos'].tail(janela).mean()
            yield_medio = self.df['Yield_Decimal'].tail(janela).mean()
            crescimento_custodia = self.df['Vlr_Custodia'].pct_change().tail(janela).mean()

        elif metodo == 'crescimento_linear':
            # Regressão linear simples
            if len(self.df) > 1:
                x = np.arange(len(self.df))
                y_rendimentos = self.df['Total_Rendimentos'].values
                coef_rendimentos = np.polyfit(x, y_rendimentos, 1)

                y_custodia = self.df['Vlr_Custodia'].values
                coef_custodia = np.polyfit(x, y_custodia, 1)

                rendimento_medio = coef_rendimentos[0]  # Inclinação
                crescimento_custodia = coef_custodia[0] / ultima_custodia
                yield_medio = self.df['Yield_Decimal'].mean()
            else:
                rendimento_medio = self.df['Total_Rendimentos'].mean()
                yield_medio = self.df['Yield_Decimal'].mean()
                crescimento_custodia = 0

        elif metodo == 'crescimento_composto':
            # Taxa de crescimento composto
            if len(self.df) > 1:
                crescimento_rendimentos = (self.df['Total_Rendimentos'].iloc[-1] /
                                          self.df['Total_Rendimentos'].iloc[0]) ** (1 / len(self.df)) - 1
                crescimento_custodia = (self.df['Vlr_Custodia'].iloc[-1] /
                                       self.df['Vlr_Custodia'].iloc[0]) ** (1 / len(self.df)) - 1
                rendimento_medio = self.df['Total_Rendimentos'].iloc[-1]
                yield_medio = self.df['Yield_Decimal'].mean()
            else:
                rendimento_medio = self.df['Total_Rendimentos'].mean()
                yield_medio = self.df['Yield_Decimal'].mean()
                crescimento_custodia = 0
                crescimento_rendimentos = 0

        # Gerar projeções
        custodia_projetada = ultima_custodia

        for i in range(1, meses_futuros + 1):
            data_futura = ultima_data + pd.DateOffset(months=i)

            if metodo == 'crescimento_composto':
                rendimento_projetado = rendimento_medio * ((1 + crescimento_rendimentos) ** i)
                custodia_projetada = ultima_custodia * ((1 + crescimento_custodia) ** i)
            elif metodo == 'crescimento_linear':
                rendimento_projetado = self.df['Total_Rendimentos'].iloc[-1] + (rendimento_medio * i)
                custodia_projetada = ultima_custodia + (crescimento_custodia * ultima_custodia * i)
            else:
                custodia_projetada *= (1 + crescimento_custodia)
                rendimento_projetado = rendimento_medio

            yield_projetado = (rendimento_projetado / custodia_projetada) * 100 if custodia_projetada > 0 else yield_medio * 100

            projecoes.append({
                'Mes_Ano': data_futura.strftime('%b/%Y').upper(),
                'Data': data_futura,
                'Vlr_Custodia_Projetado': custodia_projetada,
                'Total_Rendimentos_Projetado': rendimento_projetado,
                'Yield_Projetado': yield_projetado,
                'Metodo': metodo
            })

        return pd.DataFrame(projecoes)

    def gerar_relatorio_completo(self, salvar_json: bool = False) -> Dict:
        """
        Gera relatório completo com todas as análises

        Args:
            salvar_json: Se True, salva relatório em JSON

        Returns:
            Dicionário com relatório completo
        """
        relatorio = {
            'data_geracao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'estatisticas_gerais': self.estatisticas_gerais(),
            'analise_categorias': self.analise_por_categoria().to_dict('records'),
            'crescimento_mensal': self.calcular_crescimento_mensal().to_dict('records'),
            'projecoes_12_meses': {
                'media_simples': self.projetar_dividendos(12, 'media_simples').to_dict('records'),
                'media_movel': self.projetar_dividendos(12, 'media_movel').to_dict('records'),
                'crescimento_composto': self.projetar_dividendos(12, 'crescimento_composto').to_dict('records'),
            }
        }

        if salvar_json:
            with open('relatorio_dividendos.json', 'w', encoding='utf-8') as f:
                json.dump(relatorio, f, indent=2, ensure_ascii=False)
            print("Relatório salvo em: relatorio_dividendos.json")

        return relatorio

    def visualizar_evolucao(self, salvar_fig: bool = False):
        """
        Cria visualizações da evolução dos investimentos

        Args:
            salvar_fig: Se True, salva figura em arquivo
        """
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Análise de Dividendos e Investimentos', fontsize=16, fontweight='bold')

        # 1. Evolução da Custódia
        ax1 = axes[0, 0]
        ax1.plot(self.df['Data'], self.df['Vlr_Custodia'], marker='o', linewidth=2, markersize=6)
        ax1.set_title('Evolução do Valor em Custódia', fontweight='bold')
        ax1.set_xlabel('Data')
        ax1.set_ylabel('Valor (R$)')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)

        # 2. Rendimentos Mensais
        ax2 = axes[0, 1]
        ax2.bar(self.df['Data'], self.df['Total_Rendimentos'], color='green', alpha=0.7)
        ax2.set_title('Rendimentos Mensais', fontweight='bold')
        ax2.set_xlabel('Data')
        ax2.set_ylabel('Rendimento (R$)')
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.tick_params(axis='x', rotation=45)

        # 3. Yield Mensal
        ax3 = axes[1, 0]
        ax3.plot(self.df['Data'], self.df['Retorno_Yield'], marker='s',
                color='orange', linewidth=2, markersize=6)
        ax3.set_title('Yield Mensal (%)', fontweight='bold')
        ax3.set_xlabel('Data')
        ax3.set_ylabel('Yield (%)')
        ax3.grid(True, alpha=0.3)
        ax3.tick_params(axis='x', rotation=45)

        # 4. Distribuição por Categoria
        ax4 = axes[1, 1]
        analise_cat = self.analise_por_categoria()
        categorias_top = analise_cat.nlargest(5, 'Total_Recebido')

        if not categorias_top.empty:
            ax4.pie(categorias_top['Total_Recebido'], labels=categorias_top['Categoria'],
                   autopct='%1.1f%%', startangle=90)
            ax4.set_title('Distribuição de Rendimentos por Categoria (Top 5)', fontweight='bold')

        plt.tight_layout()

        if salvar_fig:
            plt.savefig('analise_dividendos.png', dpi=300, bbox_inches='tight')
            print("Gráfico salvo em: analise_dividendos.png")

        plt.show()

    def visualizar_projecoes(self, meses: int = 12, salvar_fig: bool = False):
        """
        Visualiza projeções futuras

        Args:
            meses: Número de meses a projetar
            salvar_fig: Se True, salva figura
        """
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        fig.suptitle(f'Projeções para os Próximos {meses} Meses', fontsize=16, fontweight='bold')

        metodos = ['media_movel', 'crescimento_composto']
        cores = ['blue', 'red']

        # Dados históricos
        datas_hist = self.df['Data']

        for idx, metodo in enumerate(metodos):
            proj = self.projetar_dividendos(meses, metodo)

            # Gráfico 1: Custódia
            axes[0].plot(datas_hist, self.df['Vlr_Custodia'],
                        'o-', color='black', label='Histórico', linewidth=2, markersize=6)
            axes[0].plot(proj['Data'], proj['Vlr_Custodia_Projetado'],
                        's--', color=cores[idx], label=f'Projeção ({metodo})', linewidth=2, markersize=6)

            # Gráfico 2: Rendimentos
            axes[1].plot(datas_hist, self.df['Total_Rendimentos'],
                        'o-', color='black', label='Histórico', linewidth=2, markersize=6)
            axes[1].plot(proj['Data'], proj['Total_Rendimentos_Projetado'],
                        's--', color=cores[idx], label=f'Projeção ({metodo})', linewidth=2, markersize=6)

        axes[0].set_title('Projeção do Valor em Custódia', fontweight='bold')
        axes[0].set_xlabel('Data')
        axes[0].set_ylabel('Valor (R$)')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        axes[0].tick_params(axis='x', rotation=45)

        axes[1].set_title('Projeção de Rendimentos Mensais', fontweight='bold')
        axes[1].set_xlabel('Data')
        axes[1].set_ylabel('Rendimento (R$)')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        axes[1].tick_params(axis='x', rotation=45)

        plt.tight_layout()

        if salvar_fig:
            plt.savefig('projecoes_dividendos.png', dpi=300, bbox_inches='tight')
            print("Gráfico salvo em: projecoes_dividendos.png")

        plt.show()

    def imprimir_relatorio_console(self):
        """Imprime relatório formatado no console"""
        stats = self.estatisticas_gerais()

        print("\n" + "="*80)
        print(" RELATÓRIO DE ANÁLISE DE DIVIDENDOS ".center(80, "="))
        print("="*80 + "\n")

        print("📊 ESTATÍSTICAS GERAIS")
        print("-" * 80)
        print(f"Período analisado: {stats['periodo_inicial']} até {stats['periodo_final']} ({stats['total_meses']} meses)")
        print(f"\nValor em Custódia:")
        print(f"  • Inicial: R$ {stats['custodia_inicial']:,.2f}")
        print(f"  • Final: R$ {stats['custodia_final']:,.2f}")
        print(f"  • Crescimento: R$ {stats['crescimento_custodia']:,.2f} ({stats['crescimento_custodia_pct']:.2f}%)")
        print(f"\nRendimentos:")
        print(f"  • Total recebido: R$ {stats['total_dividendos']:,.2f}")
        print(f"  • Média mensal: R$ {stats['media_dividendos_mes']:,.2f}")
        print(f"  • Mediana mensal: R$ {stats['mediana_dividendos']:,.2f}")
        print(f"  • Maior rendimento: R$ {stats['maior_rendimento']:,.2f}")
        print(f"  • Menor rendimento: R$ {stats['menor_rendimento']:,.2f}")
        print(f"\nYield:")
        print(f"  • Yield médio: {stats['yield_medio']:.4f}%")
        print(f"  • Yield mediano: {stats['yield_mediano']:.4f}%")

        print("\n" + "="*80)
        print("📈 ANÁLISE POR CATEGORIA")
        print("-" * 80)
        analise_cat = self.analise_por_categoria()
        print(analise_cat.to_string(index=False))

        print("\n" + "="*80)
        print("🔮 PROJEÇÕES (Próximos 12 meses - Método: Crescimento Composto)")
        print("-" * 80)
        proj = self.projetar_dividendos(12, 'crescimento_composto')
        print(f"\nRendimento total projetado: R$ {proj['Total_Rendimentos_Projetado'].sum():,.2f}")
        print(f"Custódia final projetada: R$ {proj['Vlr_Custodia_Projetado'].iloc[-1]:,.2f}")
        print(f"Yield médio projetado: {proj['Yield_Projetado'].mean():.4f}%")

        print("\n" + "="*80 + "\n")


def main():
    """Função principal para executar análises"""
    print("Analisador de Dividendos v1.0")
    print("=" * 80)

    # Carregar dados
    arquivo = input("\nDigite o caminho do arquivo CSV (ou Enter para usar 'dividendos_exemplo.csv'): ").strip()
    if not arquivo:
        arquivo = 'dividendos_exemplo.csv'

    try:
        analisador = AnalisadorDividendos(arquivo)
        print(f"\n✓ Dados carregados com sucesso! ({len(analisador.df)} registros)")

        # Menu interativo
        while True:
            print("\n" + "="*80)
            print("MENU DE OPÇÕES")
            print("-" * 80)
            print("1. Exibir relatório completo no console")
            print("2. Gerar visualizações (gráficos)")
            print("3. Visualizar projeções futuras")
            print("4. Exportar relatório para JSON")
            print("5. Salvar gráficos em arquivos")
            print("0. Sair")
            print("="*80)

            opcao = input("\nEscolha uma opção: ").strip()

            if opcao == '1':
                analisador.imprimir_relatorio_console()

            elif opcao == '2':
                analisador.visualizar_evolucao(salvar_fig=False)

            elif opcao == '3':
                meses = input("Quantos meses deseja projetar? (padrão: 12): ").strip()
                meses = int(meses) if meses.isdigit() else 12
                analisador.visualizar_projecoes(meses, salvar_fig=False)

            elif opcao == '4':
                analisador.gerar_relatorio_completo(salvar_json=True)

            elif opcao == '5':
                analisador.visualizar_evolucao(salvar_fig=True)
                analisador.visualizar_projecoes(12, salvar_fig=True)
                print("\n✓ Gráficos salvos com sucesso!")

            elif opcao == '0':
                print("\nEncerrando programa...")
                break

            else:
                print("\n❌ Opção inválida!")

    except FileNotFoundError:
        print(f"\n❌ Erro: Arquivo '{arquivo}' não encontrado!")
    except Exception as e:
        print(f"\n❌ Erro ao processar dados: {e}")


if __name__ == "__main__":
    main()
