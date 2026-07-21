# Modulos-Odoo

Módulos customizados de Odoo. Cada um fica em sua própria pasta na raiz do
repositório, no formato padrão de addon Odoo.

| Módulo | Descrição |
|---|---|
| [`whatsapp_evolution/`](./whatsapp_evolution) | Envio de mensagens WhatsApp para contatos via [Evolution API](https://github.com/EvolutionAPI/evolution-api). |
| [`personal_finance/`](./personal_finance) | Controle de despesas/receitas pessoais (contas, categorias, lançamentos, relatórios), independente do fluxo corporativo de reembolso. |

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

Controle simples de despesas e receitas pessoais/domésticas, separado do
fluxo corporativo de reembolso de funcionários (`hr_expense`). Portado para
Odoo 19 a partir do módulo original
[`odoo-personal-finances`](https://github.com/nicoraynaud/odoo-personal-finances)
(Odoo 8, Nicolas Raynaud, LGPL-3): API antiga (`osv.osv`, Python 2) reescrita
para a API nova do Odoo, views atualizadas (`list`/`pivot` em vez de
`tree`/`graph type="pivot"`, `invisible=` no lugar de `attrs`/`states`),
estrutura de saldo por conta convertida pra Float com 2 casas decimais (o
módulo original truncava centavos), e importação CSV corrigida pra Python 3
com tratamento de erro por linha.

### O que faz

- **Contas**: cadastro de contas/carteiras com saldo atual, saldo previsto no
  fim do mês atual/seguinte e saldo conciliado — tudo calculado
  automaticamente a partir dos lançamentos.
- **Categorias**: hierárquicas (categoria pai/filha), com atribuição
  automática por palavra-chave na descrição do lançamento.
- **Lançamentos**: débito/crédito com estado (Novo / Conciliado / Cancelado),
  local e data efetiva opcionais.
- **Relatórios**: tabelas dinâmicas (pivot) de lançamentos por
  categoria/conta/mês e de evolução de saldo por conta.
- **Importação em lote**: upload de CSV (`data;descrição;referência;
  conciliado;débito;crédito`) associado a uma conta.
- **Ação em massa**: selecionar vários lançamentos na lista e aplicar uma
  categoria de uma vez (`Ação > Definir categoria`).

### Requisitos

- Odoo 19

### Instalação

1. Copie a pasta `personal_finance` para o addons path do seu Odoo.
2. Em Ajustes > Apps, clique em "Atualizar lista de apps".
3. Procure por "Finanças Pessoais" e instale.

### Como usar

1. Crie uma conta em `Finanças Pessoais > Lançamentos > Contas`.
2. Lance despesas/receitas em `Lançamentos Recentes` ou `Todos os
   Lançamentos` (lista editável — não precisa abrir formulário).
3. Cadastre categorias em `Configuração > Categorias` (opcional — se o nome
   da categoria aparecer na descrição do lançamento, ela é aplicada
   automaticamente ao criar).
4. Acompanhe pelos relatórios em `Relatórios > Lançamentos por Categoria` e
   `Relatórios > Evolução do Saldo`.

### Limitações conhecidas

- Sem multi-moeda (todos os valores assumem a mesma moeda).
- Reconciliação é manual (mudar o campo Estado para "Conciliado"), sem
  importação de extrato bancário (OFX/CSV de conciliação automática).
- Acesso liberado para qualquer usuário interno (`base.group_user`) — não há
  separação de dados por usuário, então é pensado para instância de uso
  individual/teste, não multiusuário.

### Licença

LGPL-3
