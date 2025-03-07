import os
import json
import pytesseract
import fitz  # PyMuPDF
from pdf2image import convert_from_path
from PIL import Image
from unidecode import unidecode
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# 🔹 Configuração do Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 🔹 Diretórios
PASTA_PDFS = "notas_fiscais"
PASTA_RESULTADOS = "resultados"
os.makedirs(PASTA_RESULTADOS, exist_ok=True)

# 🔹 Configuração do Modelo Local no LM Studio
LLM = ChatOpenAI(
    model_name="mistral-7b-instruct-v0.2:2",
    openai_api_base="http://localhost:1234/v1",
    openai_api_key="sk-xxxx",
    temperature=0.1,
    max_tokens=2048
)

# 🔹 Template do Prompt para IA
TEMPLATE = """
Você é um assistente especializado em extrair dados de notas fiscais em PDF.
Abaixo está o texto extraído de uma nota fiscal:

{nota_texto}

Sua tarefa é estruturar os dados no seguinte formato JSON:
- Número da Nota
- Série
- Data de Emissão
- Chave de Acesso
- Tipo de Nota (Produto/Serviço)
- CNPJ do Emitente
- Nome do Emitente
- Endereço do Emitente
- CNPJ/CPF do Destinatário
- Nome do Destinatário
- Endereço do Destinatário
- Lista de Itens (Código, Descrição, Quantidade, Unidade, Valor Unitário, Valor Total)
- Subtotal
- Impostos (ICMS, IPI, ISS, PIS, COFINS)
- Valor Total da Nota
- Forma de Pagamento
- Valor Pago

Responda APENAS com um JSON formatado corretamente, sem texto adicional.
"""

def extrair_texto_pdf(pdf_path):
    """Extrai texto diretamente de um PDF, se possível."""
    texto_extraido = ""
    with fitz.open(pdf_path) as doc:
        for pagina in doc:
            texto_extraido += pagina.get_text("text") + "\n"
    
    # Se não extraiu texto, marca como PDF escaneado
    if not texto_extraido.strip():
        return None
    return unidecode(texto_extraido.strip())

def extrair_texto_ocr(pdf_path):
    """Converte PDF escaneado em imagem e aplica OCR."""
    imagens = convert_from_path(pdf_path)
    texto_extraido = ""
    
    for img in imagens:
        # Converter imagem para escala de cinza e aplicar OCR
        texto_ocr = pytesseract.image_to_string(img, lang="por")
        texto_extraido += texto_ocr + "\n"
    
    return unidecode(texto_extraido.strip())

def processar_pdf(pdf_path):
    """Processa um PDF e estrutura os dados."""
    try:
        # Tenta extrair texto diretamente
        texto_extraido = extrair_texto_pdf(pdf_path)

        # Se falhar, usa OCR
        if texto_extraido is None:
            print(f"🔹 O PDF '{pdf_path}' parece ser escaneado. Aplicando OCR...")
            texto_extraido = extrair_texto_ocr(pdf_path)

        # Criar prompt para IA
        prompt = PromptTemplate(template=TEMPLATE, input_variables=["nota_texto"])
        entrada_prompt = prompt.format(nota_texto=texto_extraido)

        # Enviar para modelo LLM (Mistral-7B no LM Studio)
        resposta_ia = LLM.invoke(entrada_prompt)

        # Extrair JSON da resposta
        if hasattr(resposta_ia, 'content'):
            resposta_ia = resposta_ia.content.strip()

        # Converter JSON em dicionário
        dados_extraidos = json.loads(resposta_ia)

        return {
            "arquivo": os.path.basename(pdf_path),
            "conteudo_bruto": texto_extraido,
            "dados_extraidos": dados_extraidos
        }
    except Exception as e:
        return {"arquivo": os.path.basename(pdf_path), "erro": str(e)}

def processar_todos_pdfs():
    """Processa todos os PDFs da pasta e salva os resultados em JSON."""
    arquivos = [f for f in os.listdir(PASTA_PDFS) if f.lower().endswith(".pdf")]

    resultados = []
    for arquivo in arquivos:
        caminho_arquivo = os.path.join(PASTA_PDFS, arquivo)
        print(f"🔹 Processando: {arquivo}")
        resultado = processar_pdf(caminho_arquivo)
        resultados.append(resultado)

    # Salvar JSON consolidado
    json_path = os.path.join(PASTA_RESULTADOS, "notas_extraidas.json")
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(resultados, json_file, ensure_ascii=False, indent=4)

    print(f"✅ Processamento concluído! Dados salvos em {json_path}")

if __name__ == "__main__":
    processar_todos_pdfs()
