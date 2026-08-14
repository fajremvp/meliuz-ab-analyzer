import csv
import os
from datetime import datetime

def log_result(nome_teste, resultado, confianca, p_value, sheet_id=None, creds_path="config/service_account.json"):
    row = [datetime.now().isoformat(), nome_teste, resultado, confianca, f"{p_value:.4f}"]

    # Tenta usar o Google Sheets
    if sheet_id and os.path.exists(creds_path):
        try:
            import gspread
            gc = gspread.service_account(filename=creds_path)
            sh = gc.open_by_key(sheet_id).sheet1
            sh.append_row(row)
            print("\n[OK] Resultado gravado com sucesso no Google Sheets!")
            return
        except Exception as e:
            print(f"\n[AVISO] Falha ao gravar no Sheets: {e}. Usando fallback CSV.")

    # Fallback para CSV Local
    path = "tracking/tests_log.csv"
    os.makedirs("tracking", exist_ok=True)
    write_header = not os.path.exists(path)

    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(["data_registro", "nome_teste", "vencedor_sugerido", "confianca", "p_value"])
        w.writerow(row)
    print(f"\n[OK] Resultado salvo localmente em {path}")
