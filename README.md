# Sistema de Gestão de Peças, Qualidade e Armazenamento

Protótipo em Python desenvolvido para o desafio **"Desafio de Automação Digital: Gestão de Peças, Qualidade e Armazenamento"** — disciplina de Algoritmos e Lógica de Programação.

Autor: **Andre Neves Frare D'Errico**

## 1. Sobre o projeto

O sistema simula, em linha de comando, a inspeção automática de peças de uma linha de montagem industrial. Ele:

- Recebe os dados de cada peça (`id`, `peso`, `cor`, `comprimento`).
- Avalia automaticamente se a peça é **aprovada** ou **reprovada**, segundo os critérios:
  - Peso entre **95g e 105g**
  - Cor **azul** ou **verde**
  - Comprimento entre **10cm e 20cm**
- Armazena as peças aprovadas em **caixas de capacidade limitada (10 peças por caixa)**, fechando automaticamente uma caixa ao atingir a capacidade máxima e abrindo a próxima.
- Permite listar, remover e gerar relatórios consolidados sobre as peças cadastradas.

## 2. Funcionalidades (menu interativo)

Ao rodar o programa, um menu é exibido com as seguintes opções:

1. **Cadastrar nova peça** – solicita id, peso, cor e comprimento; avalia e informa se a peça foi aprovada ou reprovada (e o motivo, se reprovada).
2. **Listar peças aprovadas/reprovadas** – permite filtrar por aprovadas, reprovadas ou todas as peças cadastradas.
3. **Remover peça cadastrada** – remove uma peça pelo `id`, inclusive de dentro da caixa em que estiver.
4. **Listar caixas fechadas** – mostra cada caixa já fechada e as peças que ela contém, além da caixa parcial em aberto (se houver).
5. **Gerar relatório final** – exibe total de peças aprovadas, total de reprovadas (com o motivo de cada reprovação agrupado por tipo) e a quantidade de caixas utilizadas.
6. **Sair (opção 0)** – encerra o programa.

## 3. Estrutura do código

O arquivo `sistema_pecas.py` está organizado em:

- **Constantes de negócio**: limites de peso, cores aceitas, limites de comprimento e capacidade da caixa — centralizados no topo do arquivo para fácil manutenção.
- **`Peca` (dataclass)**: estrutura de dados que representa cada peça e seu resultado de inspeção.
- **`SistemaControleQualidade` (classe)**: concentra toda a lógica de negócio (cadastro, avaliação, armazenamento em caixas, remoção e geração de relatório), mantendo o estado do sistema durante a execução.
- **Funções auxiliares de entrada** (`ler_float`, `ler_texto_nao_vazio`): validam os dados digitados pelo usuário, evitando que o programa quebre com uma entrada inválida.
- **Camada de menu** (`exibir_menu`, `opcao_*`, `main`): faz a interação com o usuário e chama as funções do sistema, mantendo a interface separada das regras de negócio.

## 4. Como rodar o programa

Pré-requisito: **Python 3.8 ou superior** instalado (não há dependências externas — apenas biblioteca padrão).

1. Clone o repositório:
   ```bash
   git clone https://github.com/SEU_USUARIO/gestao-pecas-qualidade.git
   cd gestao-pecas-qualidade
   ```
2. Execute o programa:
   ```bash
   python3 sistema_pecas.py
   ```
3. Use o menu numérico exibido no terminal para navegar entre as opções.

## 5. Exemplo de entrada e saída

Sessão de exemplo (entradas digitadas pelo usuário destacadas com `>`):

```
Bem-vindo(a) ao Sistema de Gestão de Peças, Qualidade e Armazenamento!

------------------------------------------------------------
   SISTEMA DE GESTÃO DE PEÇAS, QUALIDADE E ARMAZENAMENTO
------------------------------------------------------------
1. Cadastrar nova peça
2. Listar peças aprovadas/reprovadas
3. Remover peça cadastrada
4. Listar caixas fechadas
5. Gerar relatório final
0. Sair
------------------------------------------------------------
Escolha uma opção: > 1

-- Cadastro de nova peça --
ID da peça: > P001
Peso (g): > 98.5
Cor: > azul
Comprimento (cm): > 15
  ✅ Peça 'P001' APROVADA e armazenada na caixa 1.

Escolha uma opção: > 1

-- Cadastro de nova peça --
ID da peça: > P002
Peso (g): > 120
Cor: > azul
Comprimento (cm): > 15
  ❌ Peça 'P002' REPROVADA. Motivo(s):
     - Peso fora do padrão (120.00g, permitido 95.0-105.0g)

Escolha uma opção: > 2

-- Listar peças --
Ver (A)provadas, (R)eprovadas ou (T)odas? > T

Peças TODAS (2):
  ID: P001 | Peso: 98.5g | Cor: azul | Comprimento: 15.0cm | Aprovada | Caixa: 1
  ID: P002 | Peso: 120.0g | Cor: azul | Comprimento: 15.0cm | Reprovada | Motivo: Peso fora do padrão (120.00g, permitido 95.0-105.0g)

Escolha uma opção: > 5

============================================================
          RELATÓRIO FINAL - CONTROLE DE QUALIDADE
============================================================
Total de peças cadastradas : 2
Total de peças aprovadas    : 1
Total de peças reprovadas   : 1

Motivos de reprovação:
  - Peso fora do padrão: 1 peça(s)

Quantidade de caixas utilizadas : 1
  - Caixas fechadas (cheias)     : 0
  - Caixa em aberto (parcial)    : 1 (1 peça(s))
============================================================

Escolha uma opção: > 0

Encerrando o sistema. Até logo!
```

## 6. Tecnologias utilizadas

- Python 3 (biblioteca padrão apenas — `dataclasses` e `typing`)

## 7. Licença

Projeto acadêmico, desenvolvido para fins educacionais na disciplina de Algoritmos e Lógica de Programação.
