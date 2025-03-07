## Projeto de Extração e Estruturação de Dados de Notas Fiscais em PDF

### Descrição

Este projeto utiliza técnicas de OCR e inteligência artificial (modelo Gemini) para extrair e estruturar automaticamente informações de notas fiscais em formato PDF, incluindo aquelas escaneadas.

### Estrutura do Projeto

- **`notas_fiscais/`**: Pasta onde devem ser armazenados os arquivos PDF para processamento.
- **`resultados/`**: Pasta onde serão armazenados os resultados da extração em formato JSON.

### Bibliotecas Principais

- **PyMuPDF (`fitz`)**: Extração direta de texto de PDFs.
- **Pytesseract**: OCR para PDFs escaneados.
- **pdf2image**: Conversão de PDFs para imagens antes do OCR.
- **Pandas**: Estruturação e análise dos dados extraídos.
- **API Gemini**: Interpretação e estruturação inteligente dos dados em JSON. (substitua o campo onde deve ser colocado sua chave de api)

### Instalação das Dependências

Para instalar as dependências diretamente, execute:

```bash
pip install -r requirements.txt
```

### Execução

Execute o script principal para iniciar o processamento:

```bash
python extrator.py -- Modelo para rodar LLM local com LM Studio
```

```
Execute diretamente no notebook com play all
```

Os resultados serão armazenados em `resultados/notas_extraidas.json`.

### Visualização dos Dados

O arquivo JSON resultante pode ser carregado em DataFrames do Pandas para análise e visualização detalhada dos dados extraídos.

