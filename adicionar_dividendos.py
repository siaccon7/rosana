#!/usr/bin/env python3
"""
Script para adicionar novos dados de dividendos ao arquivo CSV
Facilita a entrada de dados mês a mês
"""

import pandas as pd
import os
from datetime import datetime


class GerenciadorDividendos:
    """Gerencia adição e edição de dados de dividendos"""

    def __init__(self, arquivo_csv: str = 'dividendos.csv'):
        self.arquivo = arquivo_csv
        self.colunas = [
            'Mes_Ano', 'Vlr_Custodia', 'Acoes', 'BDRs', 'FIIs', 'ETFs',
            'FIAGRO_FIDC', 'FI_INFRA', 'FIP', 'DIR_Subscr', 'BDR_ETF',
            'ETF_Renda_Fixa', 'FIAGRO_FII', 'Retorno_Yield', 'Total_Rendimentos'
        ]

        if os.path.exists(arquivo_csv):
            self.df = pd.read_csv(arquivo_csv)
            print(f"✓ Arquivo '{arquivo_csv}' carregado ({len(self.df)} registros)")
        else:
            self.df = pd.DataFrame(columns=self.colunas)
            print(f"✓ Novo arquivo '{arquivo_csv}' será criado")

    def adicionar_mes(self):
        """Adiciona dados de um novo mês"""
        print("\n" + "="*80)
        print(" ADICIONAR DADOS DE DIVIDENDOS ".center(80, "="))
        print("="*80 + "\n")

        # Mês/Ano
        while True:
            mes_ano = input("Mês/Ano (ex: JAN/2024): ").strip().upper()
            if self._validar_mes_ano(mes_ano):
                break
            print("❌ Formato inválido. Use MÊS/ANO (ex: JAN/2024)")

        # Verificar se já existe
        if mes_ano in self.df['Mes_Ano'].values:
            resposta = input(f"⚠️  Já existe dados para {mes_ano}. Sobrescrever? (s/n): ").lower()
            if resposta != 's':
                print("Operação cancelada.")
                return

        # Valor em custódia
        vlr_custodia = self._input_float("Valor total em custódia: R$ ")

        print("\n📊 DIVIDENDOS POR CATEGORIA (deixe vazio para 0):")
        print("-" * 80)

        # Categorias
        acoes = self._input_float("Ações: R$ ", opcional=True)
        bdrs = self._input_float("BDRs: R$ ", opcional=True)
        fiis = self._input_float("FIIs: R$ ", opcional=True)
        etfs = self._input_float("ETFs: R$ ", opcional=True)
        fiagro_fidc = self._input_float("FIAGRO-FIDC: R$ ", opcional=True)
        fi_infra = self._input_float("FI-INFRA: R$ ", opcional=True)
        fip = self._input_float("FIP: R$ ", opcional=True)
        dir_subscr = self._input_float("DIR Subscrição: R$ ", opcional=True)
        bdr_etf = self._input_float("BDR de ETF: R$ ", opcional=True)
        etf_renda_fixa = self._input_float("ETF Renda Fixa: R$ ", opcional=True)
        fiagro_fii = self._input_float("FIAGRO-FII: R$ ", opcional=True)

        # Calcular totais
        total_rendimentos = sum([
            acoes, bdrs, fiis, etfs, fiagro_fidc, fi_infra, fip,
            dir_subscr, bdr_etf, etf_renda_fixa, fiagro_fii
        ])

        retorno_yield = (total_rendimentos / vlr_custodia * 100) if vlr_custodia > 0 else 0

        # Confirmação
        print("\n" + "="*80)
        print(" RESUMO ".center(80, "="))
        print("="*80)
        print(f"Mês/Ano: {mes_ano}")
        print(f"Custódia: R$ {vlr_custodia:,.2f}")
        print(f"Total Rendimentos: R$ {total_rendimentos:,.2f}")
        print(f"Yield: {retorno_yield:.4f}%")
        print("="*80)

        confirma = input("\nConfirmar adição? (s/n): ").lower()
        if confirma != 's':
            print("Operação cancelada.")
            return

        # Criar novo registro
        novo_registro = {
            'Mes_Ano': mes_ano,
            'Vlr_Custodia': vlr_custodia,
            'Acoes': acoes,
            'BDRs': bdrs,
            'FIIs': fiis,
            'ETFs': etfs,
            'FIAGRO_FIDC': fiagro_fidc,
            'FI_INFRA': fi_infra,
            'FIP': fip,
            'DIR_Subscr': dir_subscr,
            'BDR_ETF': bdr_etf,
            'ETF_Renda_Fixa': etf_renda_fixa,
            'FIAGRO_FII': fiagro_fii,
            'Retorno_Yield': retorno_yield,
            'Total_Rendimentos': total_rendimentos
        }

        # Adicionar ou atualizar
        if mes_ano in self.df['Mes_Ano'].values:
            self.df.loc[self.df['Mes_Ano'] == mes_ano] = list(novo_registro.values())
        else:
            self.df = pd.concat([self.df, pd.DataFrame([novo_registro])], ignore_index=True)

        # Ordenar por data
        self.df = self._ordenar_por_data()

        # Salvar
        self.salvar()
        print(f"\n✓ Dados salvos com sucesso!")

    def visualizar_dados(self):
        """Exibe todos os dados do arquivo"""
        if self.df.empty:
            print("\n❌ Nenhum dado cadastrado.")
            return

        print("\n" + "="*80)
        print(" DADOS CADASTRADOS ".center(80, "="))
        print("="*80 + "\n")

        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.float_format', '{:.2f}'.format)

        print(self.df.to_string(index=False))
        print("\n" + "="*80)
        print(f"Total de registros: {len(self.df)}")
        print("="*80)

    def excluir_mes(self):
        """Exclui dados de um mês específico"""
        if self.df.empty:
            print("\n❌ Nenhum dado cadastrado.")
            return

        print("\nMeses disponíveis:")
        for i, mes in enumerate(self.df['Mes_Ano'].values, 1):
            print(f"{i}. {mes}")

        mes_ano = input("\nDigite o Mês/Ano para excluir (ex: JAN/2024): ").strip().upper()

        if mes_ano not in self.df['Mes_Ano'].values:
            print(f"❌ Mês {mes_ano} não encontrado.")
            return

        confirma = input(f"⚠️  Confirmar exclusão de {mes_ano}? (s/n): ").lower()
        if confirma != 's':
            print("Operação cancelada.")
            return

        self.df = self.df[self.df['Mes_Ano'] != mes_ano]
        self.salvar()
        print(f"✓ Dados de {mes_ano} excluídos com sucesso!")

    def salvar(self):
        """Salva dados no arquivo CSV"""
        self.df.to_csv(self.arquivo, index=False)

    def _validar_mes_ano(self, mes_ano: str) -> bool:
        """Valida formato MÊS/ANO"""
        try:
            partes = mes_ano.split('/')
            if len(partes) != 2:
                return False

            mes, ano = partes
            meses_validos = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN',
                           'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']

            return mes in meses_validos and ano.isdigit() and len(ano) == 4
        except:
            return False

    def _input_float(self, mensagem: str, opcional: bool = False) -> float:
        """Solicita input numérico do usuário"""
        while True:
            valor = input(mensagem).strip()

            if opcional and not valor:
                return 0.0

            try:
                # Remover caracteres não numéricos (exceto . e ,)
                valor = valor.replace(',', '.')
                return float(valor)
            except ValueError:
                print("❌ Digite um valor numérico válido.")

    def _ordenar_por_data(self):
        """Ordena DataFrame por data"""
        meses_ordem = {
            'JAN': 1, 'FEV': 2, 'MAR': 3, 'ABR': 4, 'MAI': 5, 'JUN': 6,
            'JUL': 7, 'AGO': 8, 'SET': 9, 'OUT': 10, 'NOV': 11, 'DEZ': 12
        }

        def get_sort_key(mes_ano):
            mes, ano = mes_ano.split('/')
            return (int(ano), meses_ordem.get(mes, 99))

        self.df['_sort_key'] = self.df['Mes_Ano'].apply(get_sort_key)
        self.df = self.df.sort_values('_sort_key').drop('_sort_key', axis=1).reset_index(drop=True)
        return self.df

    def exportar_template(self):
        """Exporta template CSV para preenchimento manual"""
        template = pd.DataFrame(columns=self.colunas)
        template.to_csv('template_dividendos.csv', index=False)
        print("✓ Template exportado: template_dividendos.csv")


def main():
    """Função principal"""
    print("="*80)
    print(" GERENCIADOR DE DIVIDENDOS ".center(80, "="))
    print("="*80)

    arquivo = input("\nDigite o nome do arquivo CSV (ou Enter para 'dividendos.csv'): ").strip()
    if not arquivo:
        arquivo = 'dividendos.csv'

    gerenciador = GerenciadorDividendos(arquivo)

    while True:
        print("\n" + "="*80)
        print(" MENU ".center(80, "="))
        print("="*80)
        print("1. Adicionar dados de um novo mês")
        print("2. Visualizar todos os dados")
        print("3. Excluir dados de um mês")
        print("4. Exportar template CSV")
        print("5. Salvar e sair")
        print("0. Sair sem salvar")
        print("="*80)

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == '1':
            gerenciador.adicionar_mes()

        elif opcao == '2':
            gerenciador.visualizar_dados()

        elif opcao == '3':
            gerenciador.excluir_mes()

        elif opcao == '4':
            gerenciador.exportar_template()

        elif opcao == '5':
            gerenciador.salvar()
            print("\n✓ Dados salvos com sucesso!")
            print("Encerrando programa...")
            break

        elif opcao == '0':
            confirma = input("⚠️  Sair sem salvar? Alterações serão perdidas. (s/n): ").lower()
            if confirma == 's':
                print("Encerrando programa...")
                break

        else:
            print("\n❌ Opção inválida!")


if __name__ == "__main__":
    main()
