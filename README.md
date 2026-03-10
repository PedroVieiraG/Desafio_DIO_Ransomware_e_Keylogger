# 🛡️ Malwares Simulados com Python — Projeto Educacional

> ⚠️ **AVISO IMPORTANTE**: Todo o conteúdo deste repositório tem **fins exclusivamente educacionais**. Os scripts foram criados para demonstrar o funcionamento interno de malwares em ambiente controlado, como parte de um curso de cibersegurança. O uso destes scripts fora de ambiente autorizado é **ilegal e antiético**.

---

## 📁 Estrutura do Projeto

```
malware-edu/
├── ransomware/
│   └── ransomware_simulator.py   # Simulação de criptografia/descriptografia
├── keylogger/
│   └── keylogger_simulator.py    # Simulação de captura de teclas
└── README.md                     # Este arquivo
```

---

## 🔐 Parte 1 — Ransomware Simulado

### Como funciona um Ransomware real?

Um ransomware é um malware que **criptografa os arquivos da vítima** e exige um pagamento (resgate) para devolver o acesso. O processo típico é:

1. **Infecção** — via phishing, link malicioso, RDP exposto ou USB infectado
2. **Reconhecimento** — o malware mapeia arquivos valiosos (documentos, fotos, banco de dados)
3. **Conexão C2** — o malware se conecta ao servidor do atacante e envia a chave pública
4. **Criptografia** — arquivos são criptografados com AES (simétrico) + RSA (assimétrico)
5. **Extorsão** — mensagem de resgate é exibida; vítima tem prazo para pagar

### O que a simulação faz?

```
[Usuário] → Opção 1: Cria arquivos .txt fictícios em ./arquivos_teste/
          → Opção 2: Gera chave Fernet (AES), criptografa arquivos → .enc
                     Exibe mensagem de "resgate"
          → Opção 3: Lê a chave salva e descriptografa os arquivos
```

### Técnica usada: Fernet (AES-128-CBC + HMAC-SHA256)

```python
from cryptography.fernet import Fernet

chave = Fernet.generate_key()       # Gera chave aleatória
fernet = Fernet(chave)

criptografado = fernet.encrypt(b"dados secretos")
original      = fernet.decrypt(criptografado)
```

### Instalação

```bash
pip install cryptography
python ransomware_simulator.py
```

---

## ⌨️ Parte 2 — Keylogger Simulado

### Como funciona um Keylogger real?

Um keylogger **registra todas as teclas digitadas** pelo usuário, podendo capturar senhas, mensagens, números de cartão, etc. Técnicas comuns:

| Técnica | Descrição |
|---------|-----------|
| **Hook de teclado (API)** | Se registra no sistema operacional para receber eventos de teclado |
| **Polling de estado** | Verifica constantemente o estado das teclas |
| **Rootkit-level** | Opera em nível de kernel (invisível ao SO) |
| **Browser extension** | Keylogger embutido em extensão maliciosa do navegador |

### O que a simulação faz?

```
[Usuário] → Modo Demo:  Simula teclas fictícias (login, senha, cartão)
          → Captura Real (com pynput): Registra teclas reais no arquivo keylog.txt
                                       Thread em background simula envio por e-mail
          → F12: Encerra a captura
```

### Técnica usada: pynput (hook de teclado via API do SO)

```python
from pynput import keyboard

def ao_pressionar(tecla):
    print(f"Tecla: {tecla}")

with keyboard.Listener(on_press=ao_pressionar) as listener:
    listener.join()
```

### Furtividade — como malwares se ocultam?

- **Sem janela visível** — executam em background sem interface
- **Nome disfarçado** — `svchost.exe`, `WindowsUpdate.exe`
- **Startup automático** — entrada no Registro do Windows ou cron job
- **Envio periódico** — exfiltra dados por SMTP, HTTP ou DNS tunneling
- **Polimorfismo** — modifica seu próprio código para evitar assinaturas de antivírus

### Instalação

```bash
pip install pynput
python keylogger_simulator.py
```

---

## 🛡️ Parte 3 — Defesa e Prevenção

### Contra Ransomware

| Medida | Descrição |
|--------|-----------|
| **Backup 3-2-1** | 3 cópias, 2 mídias diferentes, 1 offsite — backups são a ÚNICA garantia real |
| **Segmentação de rede** | Isola servidores críticos; limita propagação lateral |
| **Princípio do menor privilégio** | Usuários não devem ter acesso de escrita em tudo |
| **Patch management** | Atualizar sistemas elimina vetores de entrada conhecidos |
| **EDR/XDR** | Detecta comportamento anômalo de criptografia em massa |
| **Honeypot files** | Arquivos iscas monitorados; qualquer acesso dispara alerta |

### Contra Keylogger

| Medida | Descrição |
|--------|-----------|
| **Antivírus/EDR** | Detecta hooks de teclado suspeitos |
| **Autenticação multifator (MFA)** | Senha capturada sozinha não basta |
| **Teclado virtual** | Evita interceptação em ambientes públicos |
| **Sandboxing** | Executáveis desconhecidos rodam isolados |
| **Monitoramento de rede** | Detecta exfiltração de dados por SMTP/HTTP incomuns |
| **Conscientização** | Não abrir anexos suspeitos, não executar arquivos desconhecidos |

### Modelo de Defesa em Profundidade (Defence in Depth)

```
┌─────────────────────────────────────────┐
│  Camada 7: Conscientização do Usuário   │ ← Treinamentos, simulações de phishing
├─────────────────────────────────────────┤
│  Camada 6: Segurança de Endpoint        │ ← Antivírus, EDR, patch management
├─────────────────────────────────────────┤
│  Camada 5: Controle de Acesso           │ ← MFA, RBAC, menor privilégio
├─────────────────────────────────────────┤
│  Camada 4: Segurança de Rede            │ ← Firewall, IDS/IPS, VLAN
├─────────────────────────────────────────┤
│  Camada 3: Segurança de Aplicação       │ ← WAF, revisão de código, SAST/DAST
├─────────────────────────────────────────┤
│  Camada 2: Segurança de Dados           │ ← Criptografia em repouso e trânsito
├─────────────────────────────────────────┤
│  Camada 1: Backup e Recuperação         │ ← Backup 3-2-1, plano de DR testado
└─────────────────────────────────────────┘
```

---

## 💡 Reflexões e Aprendizados

### O que este projeto nos ensina?

1. **Ransomware não é magia** — é criptografia legítima usada de forma maliciosa. A mesma biblioteca `cryptography` que protege dados pode ser usada para extorquir.

2. **Keyloggers são simples demais** — uma biblioteca de 20 linhas já captura tudo. A defesa precisa ser multicamada porque o ataque é barato.

3. **O elo mais fraco é humano** — a maioria dos ransomwares entra por phishing. Nenhuma tecnologia substitui a conscientização.

4. **Backup é inegociável** — é a única medida que garante recuperação sem pagar resgate.

5. **Conhecer o ataque fortalece a defesa** — profissionais de segurança (blue team) precisam entender como red team pensa.

---

## 📚 Referências

- [MITRE ATT&CK — Ransomware TTPs](https://attack.mitre.org)
- [CISA Ransomware Guide](https://www.cisa.gov/ransomware)
- [cryptography.io — Fernet](https://cryptography.io/en/latest/fernet/)
- [pynput Documentation](https://pynput.readthedocs.io)

---
