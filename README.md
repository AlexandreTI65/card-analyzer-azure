# 🏦 Sistema de Análise de Cartão com Azure AI# Sistema de Análise de Cartões com Azure



[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)Um sistema completo em Python para análise de cartões de crédito/débito usando APIs do Azure Cognitive Services.

[![Azure](https://img.shields.io/badge/Azure-Computer%20Vision-0078d4.svg)](https://azure.microsoft.com/services/cognitive-services/computer-vision/)

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)## 🚀 Funcionalidades

[![Status](https://img.shields.io/badge/status-Active-success.svg)](https://github.com/seu-usuario/card-analyzer)

- **OCR Avançado**: Extração de texto usando Azure Computer Vision

Sistema inteligente para análise e validação de cartões de crédito usando Azure Computer Vision e algoritmos de validação padrão da indústria.- **Análise Estruturada**: Processamento de documentos com Azure Form Recognizer

- **Validação Inteligente**: Sistema de validação com algoritmo de Luhn

## 🚀 Funcionalidades- **API Web**: Interface REST completa com FastAPI

- **Múltiplos Métodos**: Form Recognizer, OCR ou ambos combinados

### 📝 Validação Manual- **Relatórios Detalhados**: Geração automática de relatórios

- **Algoritmo de Luhn**: Validação matemática do número do cartão- **Análise de Confiança**: Sistema de scoring para qualidade dos resultados

- **Validação de CVV**: Verificação baseada no tipo do cartão

- **Data de Expiração**: Validação de formato e vencimento## 📋 Pré-requisitos

- **Identificação de Bandeira**: Visa, Mastercard, American Express, Discover

### Serviços Azure Necessários

### 🤖 Análise com Azure AI

- **Computer Vision**: Extração automática de texto da imagem1. **Azure Computer Vision**

- **OCR Inteligente**: Reconhecimento óptico de caracteres   - Endpoint e chave de API

- **Análise de Confiança**: Pontuação de precisão da extração   - Para funcionalidades de OCR

- **Suporte Multi-formato**: JPG, PNG, WEBP

2. **Azure Form Recognizer** (recomendado)

### 🌐 Interface Web   - Endpoint e chave de API

- **Design Responsivo**: Funciona em desktop e mobile   - Para análise estruturada de documentos

- **Upload por Drag & Drop**: Interface intuitiva

- **Resultados em Tempo Real**: Feedback instantâneo### Software

- **API REST**: Endpoints para integração

- Python 3.8 ou superior

## 🛠️ Instalação- pip (gerenciador de pacotes Python)



### Pré-requisitos## 🛠️ Instalação

- Python 3.8 ou superior

- Conta Azure com Computer Vision configurado (opcional)### 1. Clone o projeto

- Git```bash

git clone <seu-repositorio>

### 1. Clonar o repositóriocd dio-doudge

```bash```

git clone https://github.com/seu-usuario/card-analyzer.git

cd card-analyzer### 2. Instale as dependências

``````bash

pip install -r requirements.txt

### 2. Criar ambiente virtual```

```bash

# Windows### 3. Configure as variáveis de ambiente

python -m venv venv

venv\\Scripts\\activateCopie o arquivo de exemplo:

```bash

# Linux/macOScopy .env.example .env

python3 -m venv venv```

source venv/bin/activate

```Edite o arquivo `.env` com suas credenciais do Azure:

```env

### 3. Instalar dependências# Configurações do Azure Computer Vision

```bashAZURE_COMPUTER_VISION_ENDPOINT=https://sua-regiao.cognitiveservices.azure.com/

pip install -r requirements.txtAZURE_COMPUTER_VISION_KEY=sua_chave_computer_vision

```

# Configurações do Azure Form Recognizer

### 4. Configurar Azure (Opcional)AZURE_FORM_RECOGNIZER_ENDPOINT=https://sua-regiao.cognitiveservices.azure.com/

```bashAZURE_FORM_RECOGNIZER_KEY=sua_chave_form_recognizer

# Copiar arquivo de exemplo

cp .env.example .env# Configurações opcionais

DEBUG=True

# Editar com suas credenciais```

# AZURE_COMPUTER_VISION_ENDPOINT=https://sua-instancia.cognitiveservices.azure.com/

# AZURE_COMPUTER_VISION_KEY=sua-chave-aqui## 🎯 Como Usar

```

### Linha de Comando

### 5. Executar o sistema

```bash#### Analisar um único cartão

python app.py```bash

```python main.py caminho/para/imagem.jpg --method form_recognizer --report

```

Acesse: http://localhost:8000

#### Analisar múltiplos cartões

## 🔧 Configuração do Azure```bash

python main.py imagem1.jpg imagem2.jpg imagem3.jpg --method both --output resultados.json

### Criando o recurso Azure Computer Vision```



1. **Azure Portal**: Acesse [portal.azure.com](https://portal.azure.com)#### Opções disponíveis

2. **Criar Recurso**: Busque por "Computer Vision" e configure- `--method`: Método de análise (`form_recognizer`, `ocr`, `both`)

3. **Obter Credenciais**: Copie Endpoint e Chave- `--output`: Arquivo de saída para resultados JSON

4. **Configurar**: Adicione no arquivo `.env`- `--report`: Gera relatório textual adicional



### Variáveis de Ambiente### API Web



```env#### Iniciar o servidor

AZURE_COMPUTER_VISION_ENDPOINT=https://sua-instancia.cognitiveservices.azure.com/```bash

AZURE_COMPUTER_VISION_KEY=sua-chave-de-32-caracterespython api.py

PORT=8000```

```

O servidor estará disponível em: `http://localhost:8000`

## 📚 Como Usar

#### Documentação da API

### 1. Validação ManualAcesse: `http://localhost:8000/docs` (Swagger UI)

1. Acesse a aba "Validação Manual"

2. Preencha os dados do cartão#### Endpoints principais

3. Clique em "Validar Cartão"

4. Veja os resultados da validação**Análise de cartão único:**

```bash

### 2. Análise de Imagem  curl -X POST "http://localhost:8000/analyze/single" \

1. Acesse a aba "Análise de Imagem"     -H "Content-Type: multipart/form-data" \

2. Faça upload da foto do cartão     -F "file=@cartao.jpg" \

3. Clique em "Analisar com Azure AI"     -F "method=form_recognizer" \

4. Veja os dados extraídos e validados     -F "generate_report=true"

```

### 3. API REST

**Análise de múltiplos cartões:**

#### Validação Manual```bash

```bashcurl -X POST "http://localhost:8000/analyze/multiple" \

curl -X POST http://localhost:8000/validate \     -H "Content-Type: multipart/form-data" \

  -H "Content-Type: application/json" \     -F "files=@cartao1.jpg" \

  -d '{     -F "files=@cartao2.jpg" \

    "cardNumber": "4532 1234 5678 9012",     -F "method=both"

    "expiryDate": "12/28",```

    "cvv": "123",

    "holderName": "João Silva"### Uso Programático

  }'

``````python

from main import CardAnalysisSystem

#### Upload de Imagem

```bash# Inicializa o sistema

curl -X POST http://localhost:8000/upload-image \system = CardAnalysisSystem()

  -F "image=@caminho/para/imagem.jpg"

```# Analisa um cartão

results = system.analyze_card_image('caminho/para/cartao.jpg', method='form_recognizer')

## 🧪 Exemplos de Teste

# Verifica se foi bem-sucedido

### Cartões Válidosif results['success']:

- **Visa**: `4532 1234 5678 9012` CVV: `123` Data: `12/28`    card_data = results['card_data']

- **Mastercard**: `5555 5555 5555 4444` CVV: `456` Data: `11/27`      print(f"Número: {card_data.get('card_number')}")

- **Amex**: `3782 822463 10005` CVV: `1234` Data: `08/26`    print(f"Nome: {card_data.get('cardholder_name')}")

    print(f"Expiração: {card_data.get('expiry_date')}")

## 🏗️ Arquitetura    print(f"Confiança: {results['confidence_analysis']['overall_confidence']:.2f}")

else:

```    print(f"Erro: {results.get('error')}")

card-analyzer/```

├── app.py              # Aplicação principal

├── requirements.txt    # Dependências## 📊 Métodos de Análise

├── .env.example       # Configuração exemplo

├── README.md          # Esta documentação### 1. Form Recognizer (Recomendado)

└── .gitignore         # Arquivos ignorados- Usa modelos pré-treinados do Azure

```- Melhor precisão para documentos estruturados

- Extração automática de campos específicos

## 🔍 Algoritmos

### 2. OCR (Computer Vision)

### Algoritmo de Luhn- Extração de texto puro

Validação matemática para números de cartão:- Processamento com detecção de regiões

1. Multiplica dígitos em posições pares por 2- Útil para casos complexos

2. Subtrai 9 se resultado > 9

3. Soma todos os dígitos### 3. Both (Combinado)

4. Válido se soma é múltiplo de 10- Usa ambos os métodos

- Combina resultados para máxima precisão

## 🚀 Deploy- Recomendado para casos críticos



### Heroku## 🔍 Validações Implementadas

```bash

heroku create meu-card-analyzer### Número do Cartão

heroku config:set AZURE_COMPUTER_VISION_ENDPOINT=https://...- Verificação de formato (13-19 dígitos)

heroku config:set AZURE_COMPUTER_VISION_KEY=abc123...- Algoritmo de Luhn

git push heroku main- Identificação do tipo de cartão (Visa, Mastercard, etc.)

```

### Nome do Portador

## 🤝 Contribuindo- Validação de caracteres permitidos

- Verificação de completude

1. Fork o projeto- Detecção de nomes genéricos

2. Crie uma branch (`git checkout -b feature/AmazingFeature`)

3. Commit suas mudanças (`git commit -m 'Add AmazingFeature'`)### Data de Expiração

4. Push para a branch (`git push origin feature/AmazingFeature`)- Múltiplos formatos suportados (MM/YY, MM/YYYY)

5. Abra um Pull Request- Verificação de validade temporal

- Alertas de expiração próxima

## ⚠️ Limitações

## 📈 Sistema de Confiança

- **Segurança**: Não armazena dados de cartão

- **Demonstração**: Para fins educacionaisO sistema calcula scores de confiança baseados em:

- **Azure**: Limitado pela qualidade da imagem

- **Compliance**: Implemente PCI DSS para produção- **Qualidade do OCR**: Confiança individual de cada campo

- **Validações**: Sucesso nas verificações

## 📄 Licença- **Consistência**: Coerência entre dados extraídos

- **Completude**: Presença de campos essenciais

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

### Níveis de Confiança

## 🙏 Agradecimentos- **Muito Alta (≥0.9)**: Dados altamente confiáveis

- **Alta (≥0.7)**: Dados confiáveis

- Microsoft Azure - Computer Vision API- **Média (≥0.5)**: Dados aceitáveis, revisão recomendada

- Python Community - Ferramentas e bibliotecas- **Baixa (≥0.3)**: Dados duvidosos, revisão necessária

- Contributors - Todos que ajudaram no projeto- **Muito Baixa (<0.3)**: Dados não confiáveis



---## 📁 Estrutura do Projeto



<div align="center">```

dio-doudge/

**Desenvolvido com ❤️ usando Python e Azure AI**├── card_analyzer/          # Módulos principais

│   ├── __init__.py

[⭐ Estrele este repositório](https://github.com/seu-usuario/card-analyzer) | [🐛 Reporte um bug](https://github.com/seu-usuario/card-analyzer/issues)│   ├── ocr_processor.py    # Azure Computer Vision OCR

│   ├── document_analyzer.py # Azure Form Recognizer

</div>│   └── validator.py        # Sistema de validação
├── config/                 # Configurações
│   └── settings.py
├── tests/                  # Testes unitários
├── sample_images/          # Imagens de exemplo
├── uploads/               # Upload temporário (criado automaticamente)
├── temp/                  # Arquivos temporários
├── results/               # Resultados salvos
├── main.py                # Aplicação principal
├── api.py                 # API Web FastAPI
├── requirements.txt       # Dependências
├── .env.example          # Exemplo de configuração
└── README.md             # Esta documentação
```

## 🧪 Testes

Execute os testes unitários:
```bash
pytest tests/
```

Para testes com cobertura:
```bash
pytest tests/ --cov=card_analyzer --cov-report=html
```

## 🔧 Configuração Avançada

### Personalização de Validação

Edite `card_analyzer/validator.py` para:
- Adicionar novos tipos de cartão
- Modificar regras de validação
- Personalizar mensagens de erro

### Otimização de Performance

No arquivo `config/settings.py`:
```python
# Timeout para APIs Azure
azure_timeout: int = 30

# Tamanho máximo de arquivo
max_file_size: int = 10 * 1024 * 1024  # 10MB
```

## 🚨 Solução de Problemas

### Erro de Autenticação Azure
```
Verifique se:
- As chaves estão corretas no arquivo .env
- Os endpoints estão no formato correto
- Os serviços estão ativos na sua conta Azure
```

### Erro de Dependências
```bash
# Reinstale as dependências
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Problemas de OCR
```
- Verifique a qualidade da imagem
- Certifique-se de que o texto está legível
- Teste com diferentes métodos de análise
```

## 📝 Logs

O sistema gera logs detalhados em:
- Console (para desenvolvimento)
- Arquivo `card_analyzer.log`

Para ajustar o nível de log, modifique em `main.py`:
```python
logging.basicConfig(level=logging.DEBUG)  # Para mais detalhes
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para detalhes.

## 🆘 Suporte

Para suporte e dúvidas:
- Abra uma issue no GitHub
- Consulte a documentação da API em `/docs`
- Verifique os logs para diagnóstico

## 🔗 Links Úteis

- [Azure Computer Vision](https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/)
- [Azure Form Recognizer](https://docs.microsoft.com/en-us/azure/cognitive-services/form-recognizer/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python Official Documentation](https://docs.python.org/3/)

---

**Desenvolvido com ❤️ para análise inteligente de cartões**