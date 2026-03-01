from datetime import datetime
from uniguairaca import baixar_boleto_uniguairaca
from condominio import baixar_boleto_condominio

def executar():
    hoje = datetime.now()
    print(f"=== Script de Boletos — {hoje.strftime('%d/%m/%Y %H:%M')} ===\n")

    # Roda apenas no dia 5
    if hoje.day != 5:
        print(f"Hoje é dia {hoje.day}. O script só roda no dia 5.")
        print("(Para testar agora, comente o bloco 'if hoje.day != 5' temporariamente)")
        return

    print(">>> Dia 5 detectado! Buscando boletos...\n")

    baixar_boleto_uniguairaca()
    print()
    baixar_boleto_condominio()

    print("\n=== Finalizado! Verifique a pasta de saída. ===")

if __name__ == "__main__":
    executar()
