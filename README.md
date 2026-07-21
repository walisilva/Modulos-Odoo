# Modulos-Odoo

Módulos customizados de Odoo. Cada um fica em sua própria pasta na raiz do
repositório, no formato padrão de addon Odoo.

| Módulo | Descrição |
|---|---|
| [`whatsapp_evolution/`](./whatsapp_evolution) | Envio de mensagens WhatsApp para contatos via [Evolution API](https://github.com/EvolutionAPI/evolution-api). |
| [`personal_finance/`](./personal_finance) | Controle de despesas/receitas pessoais com importação de extrato OFX, categorização automática e relatórios. |

---

## whatsapp_evolution

Integração com a Evolution API para conectar números de WhatsApp e enviar
mensagens para contatos direto do Odoo.

### O que faz

- **Configuração**: cadastre a URL e a API Key da sua Evolution API pelo Odoo.
- **Números**: crie e conecte instâncias de WhatsApp, com QR Code exibido na
  tela.
- **Envio**: botão "Enviar WhatsApp" na ficha de qualquer contato, com
  histórico de todas as mensagens enviadas.

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

1. **Conectar um número**: `WhatsApp > Números` > Criar > preencha o nome e
   a configuração > "Criar instância na Evolution" > escaneie o QR Code que
   aparece na tela com o WhatsApp do celular (Aparelhos conectados > Conectar
   um aparelho) > "Verificar status" até aparecer "Conectado".
2. **Enviar uma mensagem**: abra um contato com telefone preenchido, clique
   em "Enviar WhatsApp", escolha o número e escreva a mensagem.
3. **Ver histórico**: `WhatsApp > Mensagens Enviadas`.

### Limitações conhecidas

- Envio manual apenas (sem gatilho automático em fatura/pedido confirmado)
- Sem recebimento de mensagens (webhook) — não processa respostas dos
  clientes nem confirmações de entrega/leitura
- O número de telefone da instância não é preenchido automaticamente após
  conectar; pode editar manualmente no registro da instância

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
