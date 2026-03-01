import imaplib
import email
import os
import re
import urllib.request
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def baixar_boleto_condominio():
    print("[Condomínio] Iniciando busca no Gmail...")

    gmail_user  = os.getenv("GMAIL_USER")
    gmail_pass  = os.getenv("GMAIL_APP_PASSWORD")
    remetente   = os.getenv("COND_REMETENTE")
    pasta_saida = os.getenv("PASTA_SAIDA")

    os.makedirs(pasta_saida, exist_ok=True)

    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(gmail_user, gmail_pass)
        mail.select("inbox")
        print("[Condomínio] Conectado ao Gmail.")

        status, mensagens = mail.search(None, f'FROM "{remetente}"')
        ids = mensagens[0].split()

        if not ids:
            print("[Condomínio] ⚠️  Nenhum e-mail da administradora encontrado.")
            mail.logout()
            return

        ultimo_id = ids[-1]
        status, data = mail.fetch(ultimo_id, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])

        link_boleto = None
        for part in msg.walk():
            if part.get_content_type() == "text/html":
                body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                matches = re.findall(
                    r'href=["\']([^"\']*(?:boleto|superlogica|administradora)[^"\']*)["\']',
                    body,
                    re.IGNORECASE
                )
                if matches:
                    link_boleto = matches[0]
                    print(f"[Condomínio] Link encontrado: {link_boleto[:60]}...")
                    break

        if link_boleto:
            mes_ano = datetime.now().strftime("%m-%Y")
            nome_arquivo = os.path.join(pasta_saida, f"boleto_condominio_{mes_ano}.pdf")
            try:
                req = urllib.request.Request(link_boleto, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req) as response:
                    with open(nome_arquivo, "wb") as f:
                        f.write(response.read())
                print(f"[Condomínio] ✅ Boleto salvo em: {nome_arquivo}")
            except Exception as e:
                print(f"[Condomínio] ⚠️  Não foi possível baixar direto: {e}")
                print(f"[Condomínio] 💡 Acesse manualmente: {link_boleto}")
        else:
            print("[Condomínio] ⚠️  Link do boleto não encontrado.")

        mail.logout()

    except Exception as e:
        print(f"[Condomínio] ❌ Erro: {e}")
