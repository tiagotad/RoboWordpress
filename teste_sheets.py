#!/usr/bin/env python3
import gspread
from google.oauth2.service_account import Credentials
import os

# Configurações
GOOGLE_SHEET_ID = '1awAceJjODVNZljmZAPZr198AOzVE7snem14BgK_n97Q'
CREDENTIALS_FILE = 'animated-sign-464518-a7-b7542b615752.json'

def teste_google_sheets():
    try:
        print("1. Verificando arquivo de credenciais...")
        if not os.path.exists(CREDENTIALS_FILE):
            print(f"❌ Arquivo não encontrado: {CREDENTIALS_FILE}")
            return False
        print("✅ Arquivo de credenciais encontrado")
        
        print("2. Configurando credenciais...")
        scope = [
            'https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/drive.readonly'
        ]
        
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scope)
        gc = gspread.authorize(creds)
        print("✅ Credenciais configuradas")
        
        print("3. Tentando abrir planilha...")
        sheet = gc.open_by_key(GOOGLE_SHEET_ID)
        print("✅ Planilha aberta")
        
        print("4. Acessando primeira aba...")
        worksheet = sheet.sheet1
        print("✅ Primeira aba acessada")
        
        print("5. Lendo células A2:A4...")
        values = worksheet.batch_get(['A2:A4'])
        print(f"✅ Valores lidos: {values}")
        
        # Alternativa: ler célula por célula
        print("6. Lendo célula por célula...")
        for row in range(2, 5):
            try:
                cell_value = worksheet.cell(row, 1).value
                print(f"  A{row}: {cell_value}")
            except Exception as e:
                print(f"  Erro na linha {row}: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        print(f"   Tipo: {type(e).__name__}")
        return False

if __name__ == "__main__":
    print("=== TESTE DE CONEXÃO COM GOOGLE SHEETS ===")
    teste_google_sheets()
