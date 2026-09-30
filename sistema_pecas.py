"""
Sistema de Gestão de Peças, Qualidade e Armazenamento
======================================================

Desafio: prototipar, em Python, um sistema lógico de apoio à inspeção de
qualidade de uma linha de montagem industrial. O sistema recebe os dados
de cada peça produzida, avalia automaticamente se ela é aprovada ou
reprovada segundo critérios de qualidade, organiza as peças aprovadas em
caixas de capacidade limitada e gera relatórios consolidados.

Disciplina: Algoritmos e Lógica de Programação
Autor: Andre Neves Frare D'Errico
"""

from dataclasses import dataclass, field
from typing import List, Optional


# ---------------------------------------------------------------------------
# Constantes de negócio (critérios de qualidade e regras de armazenamento)
# ---------------------------------------------------------------------------
PESO_MINIMO = 95.0        # gramas
PESO_MAXIMO = 105.0       # gramas
CORES_ACEITAS = ("azul", "verde")
COMPRIMENTO_MINIMO = 10.0  # cm
COMPRIMENTO_MAXIMO = 20.0  # cm
CAPACIDADE_CAIXA = 10      # peças por caixa


# ---------------------------------------------------------------------------
# Modelo de dados
# ---------------------------------------------------------------------------
@dataclass
class Peca:
    """Representa uma peça produzida na linha de montagem."""
    id: str
    peso: float
    cor: str
    comprimento: float
    status: str = ""                       # "Aprovada" ou "Reprovada"
    motivos_reprovacao: List[str] = field(default_factory=list)
    caixa: Optional[int] = None            # número da caixa em que foi guardada (se aprovada)


# ---------------------------------------------------------------------------
# Sistema principal
# ---------------------------------------------------------------------------
class SistemaControleQualidade:
    """
    Encapsula todo o estado e as regras de negócio do sistema:
    cadastro de peças, avaliação de qualidade, organização em caixas
    e geração de relatórios.
    """

    def __init__(self):
        self.pecas_cadastradas: List[Peca] = []   # histórico completo (aprovadas + reprovadas)
        self.caixa_atual: List[Peca] = []         # caixa aberta no momento
        self.caixas_fechadas: List[List[Peca]] = []  # lista de caixas já fechadas
        self._proximo_numero_caixa = 1

    # -- Avaliação de qualidade -------------------------------------------------
    def avaliar_peca(self, peso: float, cor: str, comprimento: float):
        """
        Aplica as regras de qualidade e devolve (status, motivos).

        Critérios de aprovação (todos precisam ser atendidos):
            - Peso entre 95g e 105g
            - Cor azul ou verde
            - Comprimento entre 10cm e 20cm
        """
        motivos = []

        if not (PESO_MINIMO <= peso <= PESO_MAXIMO):
            motivos.append(
                f"Peso fora do padrão ({peso:.2f}g, permitido {PESO_MINIMO}-{PESO_MAXIMO}g)"
            )

        if cor.strip().lower() not in CORES_ACEITAS:
            motivos.append(
                f"Cor não aceita ({cor}, permitido: {', '.join(CORES_ACEITAS)})"
            )

        if not (COMPRIMENTO_MINIMO <= comprimento <= COMPRIMENTO_MAXIMO):
            motivos.append(
                f"Comprimento fora do padrão ({comprimento:.2f}cm, "
                f"permitido {COMPRIMENTO_MINIMO}-{COMPRIMENTO_MAXIMO}cm)"
            )

        status = "Reprovada" if motivos else "Aprovada"
        return status, motivos

    # -- Cadastro -----------------------------------------------------------
    def cadastrar_peca(self, id_peca: str, peso: float, cor: str, comprimento: float) -> Peca:
        """Cadastra uma nova peça, avalia sua qualidade e a armazena se aprovada."""

        if any(p.id == id_peca for p in self.pecas_cadastradas):
            raise ValueError(f"Já existe uma peça cadastrada com o id '{id_peca}'.")

        status, motivos = self.avaliar_peca(peso, cor, comprimento)
        peca = Peca(id=id_peca, peso=peso, cor=cor, comprimento=comprimento,
                     status=status, motivos_reprovacao=motivos)

        self.pecas_cadastradas.append(peca)

        if status == "Aprovada":
            self._armazenar_em_caixa(peca)

        return peca

    def _armazenar_em_caixa(self, peca: Peca) -> None:
        """Guarda uma peça aprovada na caixa aberta; fecha a caixa ao atingir a capacidade."""
        peca.caixa = self._proximo_numero_caixa
        self.caixa_atual.append(peca)

        if len(self.caixa_atual) == CAPACIDADE_CAIXA:
            self._fechar_caixa_atual()

    def _fechar_caixa_atual(self) -> None:
        self.caixas_fechadas.append(self.caixa_atual)
        self.caixa_atual = []
        self._proximo_numero_caixa += 1

    # -- Listagens ------------------------------------------------------------
    def listar_por_status(self, status: str) -> List[Peca]:
        status = status.capitalize()
        return [p for p in self.pecas_cadastradas if p.status == status]

    def listar_caixas_fechadas(self) -> List[List[Peca]]:
        return self.caixas_fechadas

    # -- Remoção --------------------------------------------------------------
    def remover_peca(self, id_peca: str) -> bool:
        """
        Remove uma peça cadastrada pelo id. Se ela estiver armazenada em uma
        caixa (aberta ou já fechada), também é removida de lá. Retorna True
        se a remoção ocorreu, False se o id não foi encontrado.
        """
        peca = next((p for p in self.pecas_cadastradas if p.id == id_peca), None)
        if peca is None:
            return False

        self.pecas_cadastradas.remove(peca)

        if peca in self.caixa_atual:
            self.caixa_atual.remove(peca)
        else:
            for caixa in self.caixas_fechadas:
                if peca in caixa:
                    caixa.remove(peca)
                    break

        return True

    # -- Relatório --------------------------------------------------------------
    def gerar_relatorio(self) -> str:
        aprovadas = self.listar_por_status("Aprovada")
        reprovadas = self.listar_por_status("Reprovada")

        contagem_motivos = {}
        for peca in reprovadas:
            for motivo in peca.motivos_reprovacao:
                chave = motivo.split(" (")[0]  # agrupa pelo tipo do motivo
                contagem_motivos[chave] = contagem_motivos.get(chave, 0) + 1

        total_caixas = len(self.caixas_fechadas) + (1 if self.caixa_atual else 0)

        linhas = []
        linhas.append("=" * 60)
        linhas.append("RELATÓRIO FINAL - CONTROLE DE QUALIDADE".center(60))
        linhas.append("=" * 60)
        linhas.append(f"Total de peças cadastradas : {len(self.pecas_cadastradas)}")
        linhas.append(f"Total de peças aprovadas    : {len(aprovadas)}")
        linhas.append(f"Total de peças reprovadas   : {len(reprovadas)}")

        if contagem_motivos:
            linhas.append("\nMotivos de reprovação:")
            for motivo, qtd in contagem_motivos.items():
                linhas.append(f"  - {motivo}: {qtd} peça(s)")

        linhas.append(f"\nQuantidade de caixas utilizadas : {total_caixas}")
        linhas.append(f"  - Caixas fechadas (cheias)     : {len(self.caixas_fechadas)}")
        linhas.append(f"  - Caixa em aberto (parcial)    : "
                       f"{'1 (' + str(len(self.caixa_atual)) + ' peça(s))' if self.caixa_atual else '0'}")
        linhas.append("=" * 60)

        return "\n".join(linhas)


# ---------------------------------------------------------------------------
# Funções auxiliares de entrada (validação de dados digitados pelo usuário)
# ---------------------------------------------------------------------------
def ler_float(mensagem: str) -> float:
    while True:
        valor = input(mensagem).strip().replace(",", ".")
        try:
            return float(valor)
        except ValueError:
            print("  ⚠ Valor inválido. Digite um número (ex: 98.5).")


def ler_texto_nao_vazio(mensagem: str) -> str:
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("  ⚠ Este campo não pode ficar vazio.")


# ---------------------------------------------------------------------------
# Interface de menu (camada de apresentação / interação com o usuário)
# ---------------------------------------------------------------------------
def exibir_menu() -> None:
    print("\n" + "-" * 60)
    print("SISTEMA DE GESTÃO DE PEÇAS, QUALIDADE E ARMAZENAMENTO".center(60))
    print("-" * 60)
    print("1. Cadastrar nova peça")
    print("2. Listar peças aprovadas/reprovadas")
    print("3. Remover peça cadastrada")
    print("4. Listar caixas fechadas")
    print("5. Gerar relatório final")
    print("0. Sair")
    print("-" * 60)


def opcao_cadastrar(sistema: SistemaControleQualidade) -> None:
    print("\n-- Cadastro de nova peça --")
    id_peca = ler_texto_nao_vazio("ID da peça: ")
    peso = ler_float("Peso (g): ")
    cor = ler_texto_nao_vazio("Cor: ")
    comprimento = ler_float("Comprimento (cm): ")

    try:
        peca = sistema.cadastrar_peca(id_peca, peso, cor, comprimento)
    except ValueError as erro:
        print(f"  ⚠ {erro}")
        return

    if peca.status == "Aprovada":
        print(f"  ✅ Peça '{peca.id}' APROVADA e armazenada na caixa {peca.caixa}.")
    else:
        print(f"  ❌ Peça '{peca.id}' REPROVADA. Motivo(s):")
        for motivo in peca.motivos_reprovacao:
            print(f"     - {motivo}")


def opcao_listar(sistema: SistemaControleQualidade) -> None:
    print("\n-- Listar peças --")
    filtro = input("Ver (A)provadas, (R)eprovadas ou (T)odas? ").strip().lower()

    if filtro.startswith("a"):
        pecas, titulo = sistema.listar_por_status("Aprovada"), "APROVADAS"
    elif filtro.startswith("r"):
        pecas, titulo = sistema.listar_por_status("Reprovada"), "REPROVADAS"
    else:
        pecas, titulo = sistema.pecas_cadastradas, "TODAS"

    print(f"\nPeças {titulo} ({len(pecas)}):")
    if not pecas:
        print("  (nenhuma peça encontrada)")
        return

    for p in pecas:
        info = f"  ID: {p.id} | Peso: {p.peso}g | Cor: {p.cor} | Comprimento: {p.comprimento}cm | {p.status}"
        if p.status == "Aprovada":
            info += f" | Caixa: {p.caixa}"
        else:
            info += f" | Motivo: {'; '.join(p.motivos_reprovacao)}"
        print(info)


def opcao_remover(sistema: SistemaControleQualidade) -> None:
    print("\n-- Remover peça cadastrada --")
    id_peca = ler_texto_nao_vazio("ID da peça a remover: ")
    if sistema.remover_peca(id_peca):
        print(f"  ✅ Peça '{id_peca}' removida com sucesso.")
    else:
        print(f"  ⚠ Nenhuma peça encontrada com o id '{id_peca}'.")


def opcao_listar_caixas(sistema: SistemaControleQualidade) -> None:
    print("\n-- Caixas fechadas --")
    caixas = sistema.listar_caixas_fechadas()
    if not caixas:
        print("  (nenhuma caixa fechada ainda)")
        return

    for numero, caixa in enumerate(caixas, start=1):
        ids = ", ".join(p.id for p in caixa)
        print(f"  Caixa {numero}: {len(caixa)} peça(s) -> [{ids}]")

    if sistema.caixa_atual:
        ids = ", ".join(p.id for p in sistema.caixa_atual)
        print(f"  Caixa em aberto (parcial): {len(sistema.caixa_atual)} peça(s) -> [{ids}]")


def opcao_relatorio(sistema: SistemaControleQualidade) -> None:
    print()
    print(sistema.gerar_relatorio())


def main() -> None:
    sistema = SistemaControleQualidade()
    acoes = {
        "1": opcao_cadastrar,
        "2": opcao_listar,
        "3": opcao_remover,
        "4": opcao_listar_caixas,
        "5": opcao_relatorio,
    }

    print("Bem-vindo(a) ao Sistema de Gestão de Peças, Qualidade e Armazenamento!")

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            print("\nEncerrando o sistema. Até logo!")
            break

        acao = acoes.get(opcao)
        if acao:
            acao(sistema)
        else:
            print("  ⚠ Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
