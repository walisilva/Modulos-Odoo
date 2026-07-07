# Modulos-Odoo

Repositório com módulos customizados de Odoo (Wali Silva). Cada módulo fica em
sua própria pasta na raiz do repositório, no formato padrão de addon Odoo
(`__manifest__.py`, `models/`, `views/`, etc.).

## Módulos disponíveis

| Pasta | Descrição |
|---|---|
| [`whatsapp_evolution/`](./whatsapp_evolution) | Configura a Evolution API, gerencia números/instâncias de WhatsApp (com QR Code) e envia mensagens para contatos direto do Odoo. |

---

## Como implantar um módulo deste repo em qualquer Odoo rodando no Coolify

Este guia é genérico — vale para `whatsapp_evolution` ou qualquer módulo novo
adicionado aqui no futuro. O cenário assumido: Odoo rodando no Coolify via
**build pack "Dockerfile"** (não docker-compose), como documentado em
`Projetos-Locais-Geral/contextos/sistemas.md`.

### Por que não dá pra "instalar via API" direto

Um módulo Odoo é código (Python/XML) que precisa existir no **addons path**
dentro do container *antes* de qualquer instalação. Não existe endpoint HTTP
que receba o código e instale em um passo só. O fluxo sempre tem duas partes:

1. **Levar o código pro container** — via Dockerfile (build) ou volume montado.
2. **Instalar/atualizar o módulo já presente no addons path** — isso sim dá
   pra fazer via API (JSON-RPC do próprio Odoo), sem precisar abrir a tela.

### Passo 1 — Adicionar o módulo ao Dockerfile do Odoo

No Coolify, a aplicação Odoo usa um Dockerfile "colado" (build pack
`dockerfile`, sem repositório git associado). Para incluir um addon deste
repo, adicione ao Dockerfile (antes do `ENTRYPOINT`/`CMD` finais):

```dockerfile
FROM odoo:19

# ... (odoo.conf, etc — ver contextos/sistemas.md) ...

# Clona este repo (público, não precisa de token) e copia o módulo desejado
RUN git clone --depth 1 https://github.com/walisilva/Modulos-Odoo.git /tmp/modulos-odoo \
    && mkdir -p /mnt/extra-addons \
    && cp -r /tmp/modulos-odoo/whatsapp_evolution /mnt/extra-addons/ \
    && rm -rf /tmp/modulos-odoo \
    && chown -R odoo:odoo /mnt/extra-addons
```

E garanta que o `odoo.conf` (embutido no Dockerfile) tenha o addons_path
apontando pra lá, incluindo os paths padrão da imagem:

```
addons_path = /mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons,/usr/lib/python3/dist-packages/addons
```

Como o Coolify não permite editar o campo `dockerfile` de uma aplicação já
criada via API (`PATCH` recusa o campo), o caminho é: **deletar a aplicação e
recriar** com o Dockerfile atualizado (`POST /api/v1/applications/dockerfile`),
reaplicando `ports_exposes`/`ports_mappings` e o storage (volume) do
filestore. O banco de dados Postgres não é afetado — ele é um recurso
separado no Coolify, os dados do Odoo continuam intactos.

Depois, disparar o deploy: `GET /api/v1/deploy?uuid=<uuid_da_app>`.

### Passo 2 — Instalar/atualizar o módulo via API do Odoo (JSON-RPC)

Com o container no ar e o módulo já no addons path, autentique e chame o
`ir.module.module`:

```python
import requests

url = "http://192.168.0.100:8069/jsonrpc"
db, login, password = "odoo", "walison.eng@gmail.com", "<senha>"

def call(service, method, args):
    r = requests.post(url, json={
        "jsonrpc": "2.0", "method": "call",
        "params": {"service": service, "method": method, "args": args},
    })
    return r.json()["result"]

uid = call("common", "login", [db, login, password])

def execute(model, method, args, kwargs=None):
    return call("object", "execute_kw",
                 [db, uid, password, model, method, args, kwargs or {}])

# Atualiza a lista de apps (pra o Odoo "enxergar" o módulo novo no disco)
execute("ir.module.module", "update_list", [[]])

# Localiza e instala o módulo
mod_id = execute("ir.module.module", "search",
                  [[["name", "=", "whatsapp_evolution"]]])
execute("ir.module.module", "button_immediate_install", [mod_id])
```

### Passo 3 — Validar

- Confira em Ajustes > Apps que o módulo aparece como "Instalado"
- Acesse o menu criado pelo módulo (ex: "WhatsApp" no menu principal)
- Teste a conexão com a Evolution API pela tela de Configuração

---

## Módulo: whatsapp_evolution

Integração com a [Evolution API](https://github.com/EvolutionAPI/evolution-api)
(API não-oficial de WhatsApp, baseada em Baileys).

### O que faz

- **Configuração** (`WhatsApp > Configuração`, só admins): URL base e API Key
  global da Evolution API.
- **Números** (`WhatsApp > Números`): cria uma instância na Evolution
  (`POST /instance/create`), mostra o QR Code pra conectar o WhatsApp, e
  permite verificar status / desconectar / excluir.
- **Envio**: botão "Enviar WhatsApp" na ficha de qualquer contato (Contacts),
  abre um assistente pra escolher o número (instância conectada) e escrever a
  mensagem. Todo envio fica registrado em `WhatsApp > Mensagens Enviadas`.

### Configuração inicial já incluída

O módulo já vem com um registro de configuração pré-preenchido apontando pra
instância Evolution da porta 8082 (`http://192.168.0.100:8082`, usada hoje
pelo Marketing-WhatsApp). **Nenhuma instância/número é criada
automaticamente** — isso é proposital, pra você escolher o nome e escanear o
QR Code do número que quiser usar.

### Limitações da v1 (fica pra depois, se precisar)

- Só envio manual (sem gatilho automático em fatura/pedido confirmado)
- Sem recebimento de mensagens (webhook) — não processa respostas dos
  clientes nem confirmações de entrega/leitura
- `phone_number` da instância não é preenchido automaticamente após conectar
  (a Evolution não devolve isso de forma consistente em `/connectionState`);
  pode editar manualmente no registro da instância
