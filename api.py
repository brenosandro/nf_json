import google.generativeai as genai

# Configuração da API Gemini
GEMINI_API_KEY = "COLOQUE AQUI SUA CHAVE API"
genai.configure(api_key=GEMINI_API_KEY)

# Inicializa o modelo Gemini
model = genai.GenerativeModel("gemini-2.0-flash")