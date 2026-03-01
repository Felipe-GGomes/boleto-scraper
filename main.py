from uniguairaca import baixar_boleto_uniguairaca
from condominio import baixar_boleto_condominio
from datetime import datetime

def executar():
    print(f"=== Script de Boletos — {datetime.now().strftime('%d/%m/%Y %H:%M')} ===\n")
    baixar_boleto_uniguairaca()
    print()
    baixar_boleto_condominio()
    print("\n=== Finalizado! Verifique a pasta de saída. ===")

if __name__ == "__main__":
    executar()
