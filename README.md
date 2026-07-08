# Modulos-Odoo

Módulos customizados de Odoo. Cada um fica em sua própria pasta na raiz do
repositório, no formato padrão de addon Odoo.

| Módulo | Descrição |
|---|---|
| [`whatsapp_evolution/`](./whatsapp_evolution) | Envio de mensagens WhatsApp para contatos via [Evolution API](https://github.com/EvolutionAPI/evolution-api). |

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
