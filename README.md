# Simulador de infecção epidemiologica da COVID

Trata-se de um simulador epidemiologico simplificado focado na COVID-19. Foi utilizado uma generalização do modelo SEIRD (incluido o fator H referente ao agente com status hospitalizado) para modelagem do sistema.

    - [ ] SEIRD: Susceptible-Exposed-Infected-Recovered-Dead
    - [x] SEIRDH: Susceptible-Exposed-Infected-Recovered-Dead-Hospitalized

## 🚀 Começando

### 📋 Pré-requisitos

Instale python, e em seguida, o gerenciador de dependencias pip

### 🔧 Instalação Dependencias

    pip install -r requirements.txt

## 📦 Desenvolvimento

Foi utilizados uma generalização do modelo SEIRD, embutindo uma probabilidade nas relações entre os agentes. É um modelo estocastico.

## 🛠️ Construído com

* [Python](https://www.python.org/) (v3.10) - Linguagem de programação
* [DearPyGUI](https://dearpygui.readthedocs.io/en/latest/) (v1.3.1) - Construção da interface gráfica

## Referencias

* <https://www.youtube.com/watch?v=gxAaO2rsdIs>
* <https://ncase.me/covid-19/>
* <http://www.im.ufrj.br/~coloquiomea/apresentacoes/almeida_2020.pdf>
* <https://www.ufsm.br/coronavirus/simulador/>
