# Manual do Usuário - Simulador de Page-Fault

## Introdução

Este manual descreve como utilizar o Simulador de Page-Fault com Memória Virtual, uma ferramenta educacional que demonstra o funcionamento do gerenciamento de memória virtual em sistemas operacionais.

## Conceitos Básicos

Antes de utilizar o simulador, é importante compreender alguns conceitos básicos:

- **Memória Virtual**: Técnica que permite que um programa utilize um espaço de endereçamento maior que a memória física disponível.
- **Página**: Unidade de alocação na memória virtual, identificada por um nome (ex: P1, P2).
- **Frame (Quadro)**: Unidade de alocação na memória física onde as páginas são carregadas.
- **Page-Fault**: Ocorre quando o programa tenta acessar uma página que não está na memória física.
- **Page-In**: Processo de trazer uma página do disco para a memória física.
- **ETP (Tabela de Páginas)**: Estrutura que mapeia páginas virtuais para frames físicos.

## Instalação

1. Certifique-se de ter o Python 3.x instalado
2. Instale o Tkinter (se não estiver incluído na sua instalação do Python):
   ```
   sudo apt-get install python3-tk  # Para sistemas baseados em Debian/Ubuntu
   ```
   ou
   ```
   pip install tk  # Para outros sistemas
   ```

## Iniciando o Simulador

Execute o arquivo `memory_simulator_gui_reset.py`:
```
python3 memory_simulator_gui_reset.py
```

## Interface do Usuário

A interface do simulador é dividida em quatro seções principais:

### 1. Configuração
- **Número de quadros da memória principal**: Define quantos frames físicos estarão disponíveis.
- **Páginas da memória virtual**: Lista de páginas disponíveis no disco, separadas por vírgula.
- **Botão "Inicializar Simulador"**: Configura o simulador com os parâmetros fornecidos.
- **Botão "Resetar Simulador"**: Limpa o estado atual e permite reconfigurar o simulador com novos parâmetros.

### 2. Acesso a Páginas
- **Menu suspenso**: Permite selecionar uma página para acessar.
- **Botão "Acessar Página"**: Simula o acesso à página selecionada.

### 3. Estado do Sistema
- Área de texto que exibe o estado atual do sistema, incluindo:
  - Conteúdo da memória principal (frames)
  - Tabela de páginas (ETP)
  - Área de memória virtual (disco)
  - Mensagens sobre operações realizadas

### 4. Estatísticas
- **Page Faults**: Contador de page-faults ocorridos durante a simulação.
- **Histórico de Acessos**: Sequência de páginas acessadas durante a simulação.

## Passo a Passo

### Configurando o Simulador

1. Digite o número de quadros da memória principal (ex: 3)
2. Digite as páginas da memória virtual separadas por vírgula (ex: P1,P2,P3,P4,P5)
3. Clique em "Inicializar Simulador"

### Simulando Acessos a Páginas

1. Selecione uma página no menu suspenso
2. Clique em "Acessar Página"
3. Observe o resultado na área de Estado do Sistema:
   - Se a página já estiver na memória, não ocorrerá page-fault
   - Se a página não estiver na memória e houver frames livres, ocorrerá page-fault e a página será carregada
   - Se a página não estiver na memória e não houver frames livres, ocorrerá page-fault e uma página será substituída

### Resetando o Simulador

Se você deseja experimentar com uma configuração diferente:

1. Clique no botão "Resetar Simulador"
2. Os campos de configuração serão reabilitados
3. Digite novos valores para o número de quadros e/ou páginas da memória virtual
4. Clique em "Inicializar Simulador" para começar uma nova simulação

## Exemplos de Uso

### Exemplo 1: Carregamento Inicial

1. Configure o simulador com 3 quadros e páginas P1,P2,P3,P4,P5
2. Inicialize o simulador
3. Acesse P1, P2 e P3 sequencialmente
4. Observe que cada acesso causa um page-fault e as páginas são carregadas em frames diferentes

### Exemplo 2: Substituição de Páginas

1. Configure o simulador com 2 quadros e páginas P1,P2,P3,P4,P5
2. Inicialize o simulador
3. Acesse P1 e P2 (serão carregadas nos frames 0 e 1)
4. Acesse P3 (causará substituição da página P1)
5. Acesse P1 novamente (causará outro page-fault e substituirá P2)

### Exemplo 3: Testando Diferentes Configurações

1. Configure o simulador com 2 quadros e páginas P1,P2,P3
2. Inicialize o simulador e faça alguns acessos
3. Clique em "Resetar Simulador"
4. Configure agora com 4 quadros e páginas P1,P2,P3,P4,P5,P6
5. Inicialize o simulador novamente e compare o comportamento com a configuração anterior

## Interpretando os Resultados

- **Page-fault detectado**: Indica que a página solicitada não está na memória principal.
- **Página X carregada para o Frame Y**: Indica que a página foi carregada com sucesso em um frame livre.
- **Memória cheia. Página X substituída pela Página Y no Frame Z**: Indica que foi necessário substituir uma página existente.
- **Página X já está na memória principal (Frame Y)**: Indica que a página já estava carregada, não causando page-fault.

## Dicas de Uso

- Experimente diferentes configurações de número de frames para observar como isso afeta a taxa de page-faults.
- Tente diferentes sequências de acesso para entender padrões de substituição.
- Observe o histórico de acessos e o contador de page-faults para avaliar o desempenho.
- Use o botão de reset para comparar rapidamente diferentes configurações sem precisar reiniciar o aplicativo.

## Solução de Problemas

- **Erro: O número de quadros deve ser um inteiro positivo**: Verifique se você inseriu um número válido para os quadros.
- **Erro: A lista de páginas não pode estar vazia**: Verifique se você inseriu pelo menos uma página.
- **Erro: Nome de página inválido**: Use apenas letras, números e underscore nos nomes das páginas.
- **Erro: Existem páginas duplicadas na lista**: Remova as páginas duplicadas da lista.

