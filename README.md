# Modulos-Odoo

Módulos customizados de Odoo. Cada um fica em sua própria pasta na raiz do
repositório, no formato padrão de addon Odoo.

| Módulo | Descrição |
|---|---|
| [`whatsapp_evolution/`](./whatsapp_evolution) | Envio de mensagens WhatsApp para contatos via [Evolution API](https://github.com/EvolutionAPI/evolution-api). |
| [`personal_finance/`](./personal_finance) | Controle de despesas/receitas pessoais com importação de extrato OFX, categorização automática e relatórios. |
| [`contact_whatsapp_number/`](./contact_whatsapp_number) | Campo com o número de WhatsApp "cru" do contato, para integrações automáticas (ex: n8n) casarem mensagens recebidas com o contato certo. |

---

## whatsapp_evolution

Integração com a Evolution API para conectar números de WhatsApp e enviar
mensagens para contatos direto do Odoo.

### O que faz

- **Configuração**: cadastre a URL e a API Key da sua Evolution API pelo Odoo.
- **Números**: crie e conecte instâncias de WhatsApp, com QR Code exibido na
  tela — ou adote uma instância que já existe e já está conectada na
  Evolution, só digitando o nome exato dela.
- **Envio**: botão "Enviar WhatsApp" na ficha de qualquer contato, com
  histórico de todas as mensagens enviadas.
- **Config do funil de CRM por instância**: cada número pode ter sua própria
  equipe de vendas, mapeamento de estágios, padrões de texto (pedido/pedido
  concluído) e janela de reabertura de cliente recorrente — pensado pra um
  workflow externo (ex: n8n) ler esses parâmetros via RPC em vez de ter
  esses dados fixos no workflow.

### Requisitos

- Odoo 19
- Uma instância da [Evolution API](https://github.com/EvolutionAPI/evolution-api)
  já rodando e acessível pelo servidor do Odoo

### Instalação

1. Copie a pasta `whatsapp_evolution` para o addons path do seu Odoo.
2. Em Ajustes > Apps, clique em "Atualizar lista de apps".
3. Procure por "WhatsApp via Evolution API" e instale.

### Configuração

Em `WhatsApp > Configuração` (menu visível só para administradores), crie um
registro com:
- **URL base** da Evolution API (ex: `http://localhost:8080`)
- **API Key global** (o `AUTHENTICATION_API_KEY` da sua Evolution API)

### Como usar

1. **Conectar um número novo (via QR Code)**: `WhatsApp > Números` > Criar >
   preencha o nome e a configuração > "Criar instância na Evolution" >
   escaneie o QR Code que aparece na tela com o WhatsApp do celular
   (Aparelhos conectados > Conectar um aparelho) > "Verificar status" até
   aparecer "Conectado".
2. **Adotar um número que já está conectado na Evolution**: `WhatsApp >
   Números` > Criar > preencha o nome **exatamente igual** ao nome da
   instância já existente na Evolution API e a configuração >
   "Conectar em instância já existente" — não usa QR Code nem cria nada na
   Evolution, só verifica o status e importa o token/número já existentes.
3. **Enviar uma mensagem**: abra um contato com telefone preenchido, clique
   em "Enviar WhatsApp", escolha o número e escreva a mensagem.
4. **Ver histórico**: `WhatsApp > Mensagens Enviadas`.
5. **Configurar o funil de CRM de uma instância**: abra o número em
   `WhatsApp > Números`, aba "Automação de CRM" — escolha a equipe e os 4
   estágios do funil (Novo/Em Andamento/Pedido/Pedido Concluído), ajuste os
   padrões de texto e a janela de reabertura. Um workflow externo (n8n) lê
   esses campos via `search_read` em `evolution.instance` pelo `name` da
   instância — editar aqui muda o comportamento do funil sem mexer no
   workflow.

### Limitações conhecidas

- Envio manual apenas (sem gatilho automático em fatura/pedido confirmado)
- O módulo em si não processa mensagens recebidas (webhook) — isso é feito
  por um workflow externo (n8n), que só *lê* a configuração daqui
- O número de telefone da instância não é preenchido automaticamente ao
  criar via QR Code (fica preenchido ao adotar uma instância existente);
  pode editar manualmente no registro da instância

### Licença

LGPL-3

---

## personal_finance

Controle de despesas e receitas pessoais/domésticas, independente do fluxo
corporativo de reembolso (`hr_expense`) e do app Accounting — construído do
zero para a API do Odoo 19 (não é port de módulo de versão antiga).

### O que faz

- **Cadastros**: bancos, formas de pagamento, cartões de crédito (etiqueta
  informativa com dia de vencimento — sem modelo de fatura), contas com
  saldo calculado (atual, fim do mês, fim do mês seguinte, conciliado).
- **Categorias** hierárquicas, com tipo (despesa/receita/neutro — "neutro"
  cobre transferência entre contas próprias/estorno, fica fora dos totais
  de despesa/receita nos relatórios).
- **Lançamentos** com Entrada e Saída como campos separados (sempre
  positivos, como um extrato bancário — sem sinal de menos), calculados
  automaticamente na importação a partir do valor do extrato.
- **Importação de extrato OFX**: `Lançamentos > Importar OFX`, escolhe a
  conta, sobe o arquivo. Deduplica automaticamente por FITID (não duplica
  se reimportar um período sobreposto), separa entrada/saída automaticamente
  e categoriza automaticamente por regra de padrão de texto.
- **Regras de categorização** (`Cadastros > Regras de Categorização`):
  padrão de texto → categoria. Se mais de uma regra combinar com a
  descrição, vence a mais específica (padrão mais longo). Também são
  criadas/atualizadas automaticamente ao categorizar um lançamento pela
  tela "Não Categorizados" com a opção "Salvar como regra" preenchida —
  assim a próxima importação já reconhece.
- **Relatórios**: uma única tela (`Relatórios > Relatórios`) alternando
  entre sintético (tabela dinâmica por categoria/mês), gráfico (barra,
  linha ou pizza — agrupado por categoria e mês, então dá pra ver tanto a
  fatia de cada categoria no total quanto a evolução mês a mês) e analítico
  (lista detalhada), usando os view switchers nativos do Odoo. Mais um
  relatório de evolução de saldo por conta/mês.

### Requisitos

- Odoo 19
- Biblioteca Python [`ofxtools`](https://github.com/csingley/ofxtools)
  (**não vem instalada por padrão** — ver "Instalação" abaixo)

### Instalação

1. Copie a pasta `personal_finance` para o addons path do seu Odoo.
2. Instale a dependência Python no ambiente do Odoo:
   `pip install ofxtools` (ou, num Dockerfile, adicione
   `RUN pip install --break-system-packages ofxtools` antes do `ENTRYPOINT`).
3. Em Ajustes > Apps, clique em "Atualizar lista de apps".
4. Procure por "Finanças Pessoais" e instale.

### Como usar

1. Cadastre ao menos um banco e uma conta em `Cadastros`.
2. Importe um extrato: `Lançamentos > Importar OFX` > escolha a conta e o
   arquivo `.ofx` > Importar.
3. Revise o que ficou sem categoria em `Lançamentos > Não Categorizados` —
   clique no botão **"Categorizar"** de cada linha (abre um formulário
   rápido já com um padrão de regra sugerido, editável, no campo "Salvar
   como regra"). Pra categorizar várias linhas parecidas de uma vez,
   selecione todas e use a ação "Definir categoria" no menu de ações (⚙)
   da lista — mesmo formulário, aplicado em lote.
4. Use o filtro **"Sem Padrões de Importação"** (na busca, junto com "Sem
   categoria") pra achar depois lançamentos que foram categorizados sem
   criar uma regra (ex: editados direto em "Todos os Lançamentos") — assim
   dá pra voltar e completar a regra quando quiser.
5. Acompanhe em `Relatórios > Relatórios`.

### Limitações conhecidas

- Cartão de crédito é só uma etiqueta informativa (sem fatura mensal,
  fechamento ou geração automática de pagamento na conta).
- Sem lançamentos parcelados ou recorrentes automáticos.
- Sem orçamento (limite de gasto por categoria/mês).
- Importa um extrato OFX por vez, um arquivo = uma conta (não processa
  arquivos com mais de uma conta dentro).
- Sem importação de fatura de cartão em PDF.

### Licença

LGPL-3

---

## contact_whatsapp_number

Módulo pequeno e focado: adiciona um campo `whatsapp_number` em Contatos
com o número de telefone exatamente como recebido de uma integração de
WhatsApp (só dígitos, com código do país, ex: `5583991065820`) — usado
por automações externas (ex: um workflow n8n recebendo webhook da
Evolution API) para casar mensagens recebidas com o contato certo sem
depender de normalizar o campo Telefone (que fica formatado bonito pra
exibição, ex: `55 (83) 99106-5820`).

### O que faz

- Campo `whatsapp_number` visível na ficha do contato pra qualquer
  usuário com acesso a Contatos, sempre **somente leitura**.
- Botão "Editar número do WhatsApp" ao lado do campo, visível **só** pra
  quem estiver no grupo "Pode editar número do WhatsApp" — abre um
  formulário pequeno pra editar manualmente quando precisar (ex:
  corrigir um casamento errado). Ninguém fora do grupo consegue editar
  (nem pela ficha, nem por baixo — o acesso ao modelo do formulário de
  edição também é restrito ao grupo).

### Requisitos

- Odoo 19

### Instalação

1. Copie a pasta `contact_whatsapp_number` para o addons path do seu Odoo.
2. Em Ajustes > Apps, clique em "Atualizar lista de apps".
3. Procure por "Número WhatsApp do Contato" e instale.
4. Em Ajustes > Usuários e Empresas > Grupos, adicione os usuários que
   podem editar o campo ao grupo "Pode editar número do WhatsApp".

### Licença

LGPL-3
