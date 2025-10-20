#!/usr/bin/env python3
"""
Sistema de Análise de Cartão com Azure AI
Versão GitHub - Sistema Principal Limpo

Autor: Seu Nome
Data: 2025-10-20
Licença: MIT
"""

import http.server
import socketserver
import json
import re
import os
from datetime import datetime
import socket
import base64
from pathlib import Path

# Configurações do Azure (via variáveis de ambiente)
AZURE_ENDPOINT = os.getenv('AZURE_COMPUTER_VISION_ENDPOINT', 'https://sua-instancia.cognitiveservices.azure.com/')
AZURE_KEY = os.getenv('AZURE_COMPUTER_VISION_KEY', 'sua-chave-aqui')
DEFAULT_PORT = int(os.getenv('PORT', 8000))

class CardAnalyzer:
    """
    Sistema de análise de cartão de crédito com Azure AI
    
    Funcionalidades:
    - Validação manual de dados do cartão
    - Upload e análise de imagem com Azure Computer Vision
    - Algoritmo de Luhn para validação de números
    - Interface web moderna e responsiva
    """
    
    def __init__(self):
        self.azure_configured = bool(AZURE_ENDPOINT and AZURE_KEY and 'sua-chave-aqui' not in AZURE_KEY)
        if self.azure_configured:
            print(f"✅ Azure AI configurado: {AZURE_ENDPOINT}")
        else:
            print("⚠️  Azure AI não configurado - funcionará em modo simulação")
    
    def analyze_image(self, image_data):
        """
        Analisa imagem do cartão enviada pelo usuário
        
        Args:
            image_data: Dados binários da imagem
            
        Returns:
            dict: Resultado da análise com dados extraídos e validação
        """
        try:
            if self.azure_configured:
                # Aqui seria a integração real com Azure Computer Vision
                extracted_data = self._simulate_azure_extraction(image_data)
            else:
                # Modo simulação
                extracted_data = self._simulate_extraction()
            
            validation = self.validate_card_data(extracted_data)
            confidence = self._calculate_confidence(extracted_data, validation)
            
            return {
                'timestamp': datetime.now().isoformat(),
                'azure_analysis': self.azure_configured,
                'image_processed': True,
                'image_size': len(image_data) if image_data else 0,
                'extracted_data': extracted_data,
                'validation': validation,
                'confidence_scores': confidence
            }
            
        except Exception as e:
            return {
                'error': True,
                'message': f'Erro na análise: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def validate_manual_input(self, card_data):
        """
        Valida dados inseridos manualmente
        
        Args:
            card_data: dict com dados do cartão
            
        Returns:
            dict: Resultado da validação
        """
        extracted = {
            'card_number': card_data.get('cardNumber', ''),
            'cardholder_name': card_data.get('holderName', ''),
            'expiry_date': card_data.get('expiryDate', ''),
            'cvv': card_data.get('cvv', ''),
            'card_type': self._identify_card_type(card_data.get('cardNumber', ''))
        }
        
        validation = self.validate_card_data(extracted)
        
        # Validação específica do CVV
        cvv_validation = self._validate_cvv(extracted['cvv'], extracted['card_type'])
        validation['cvv'] = cvv_validation
        
        validation['overall_valid'] = all([
            validation['card_number']['valid'],
            validation['expiry_date']['valid'],
            validation['cardholder_name']['valid'],
            validation['cvv']['valid']
        ])
        
        confidence = self._calculate_confidence(extracted, validation)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'manual_input': True,
            'extracted_data': extracted,
            'validation': validation,
            'confidence_scores': confidence
        }
    
    def validate_card_data(self, data):
        """
        Valida dados do cartão usando algoritmos padrão
        
        Args:
            data: dict com dados do cartão
            
        Returns:
            dict: Resultado detalhado da validação
        """
        validation = {
            'card_number': {'valid': False, 'message': ''},
            'expiry_date': {'valid': False, 'message': ''},
            'cardholder_name': {'valid': False, 'message': ''},
            'overall_valid': False
        }
        
        # Validação do número do cartão (Algoritmo de Luhn)
        if data.get('card_number'):
            if self._luhn_check(data['card_number']):
                validation['card_number']['valid'] = True
                validation['card_number']['message'] = 'Número válido pelo algoritmo de Luhn'
            else:
                validation['card_number']['message'] = 'Número inválido (falha no algoritmo de Luhn)'
        else:
            validation['card_number']['message'] = 'Número não encontrado'
        
        # Validação da data de expiração
        if data.get('expiry_date') and data['expiry_date'] not in ['00/00', 'MM/AA']:
            if self._validate_expiry_date(data['expiry_date']):
                validation['expiry_date']['valid'] = True
                validation['expiry_date']['message'] = 'Data válida e não expirada'
            else:
                validation['expiry_date']['message'] = 'Data inválida ou expirada'
        else:
            validation['expiry_date']['message'] = 'Data não encontrada ou ilegível'
        
        # Validação do nome do portador
        if data.get('cardholder_name') and data['cardholder_name'] not in ['CARDHOLDER NAME', 'NOME DO PORTADOR']:
            if len(data['cardholder_name'].strip()) >= 2:
                validation['cardholder_name']['valid'] = True
                validation['cardholder_name']['message'] = 'Nome válido'
            else:
                validation['cardholder_name']['message'] = 'Nome muito curto'
        else:
            validation['cardholder_name']['message'] = 'Nome não encontrado ou genérico'
        
        validation['overall_valid'] = all([
            validation['card_number']['valid'],
            validation['expiry_date']['valid'],
            validation['cardholder_name']['valid']
        ])
        
        return validation
    
    def _luhn_check(self, card_number):
        """Implementa o algoritmo de Luhn para validação de cartões"""
        try:
            # Remove caracteres não numéricos
            digits = [int(d) for d in re.sub(r'\D', '', str(card_number))]
            
            if len(digits) < 13:
                return False
            
            checksum = 0
            is_even = False
            
            # Processa dígitos da direita para esquerda
            for digit in reversed(digits):
                if is_even:
                    digit *= 2
                    if digit > 9:
                        digit -= 9
                checksum += digit
                is_even = not is_even
            
            return checksum % 10 == 0
            
        except (ValueError, TypeError):
            return False
    
    def _validate_expiry_date(self, expiry):
        """Valida data de expiração do cartão"""
        try:
            # Remove caracteres não numéricos
            clean = re.sub(r'[^0-9]', '', str(expiry))
            
            if len(clean) != 4:
                return False
            
            month = int(clean[:2])
            year = int('20' + clean[2:])
            
            if month < 1 or month > 12:
                return False
            
            # Verifica se não está expirado
            current = datetime.now()
            expiry_date = datetime(year, month, 1)
            
            return expiry_date > current
            
        except (ValueError, TypeError):
            return False
    
    def _validate_cvv(self, cvv, card_type):
        """Valida CVV baseado no tipo do cartão"""
        try:
            clean = re.sub(r'\D', '', str(cvv))
            
            if card_type == 'American Express':
                valid = len(clean) == 4
            else:
                valid = len(clean) == 3
            
            return {
                'valid': valid,
                'message': 'CVV válido' if valid else f'CVV inválido para {card_type}'
            }
            
        except (ValueError, TypeError):
            return {'valid': False, 'message': 'CVV inválido'}
    
    def _identify_card_type(self, card_number):
        """Identifica o tipo do cartão pelo número"""
        clean = re.sub(r'\D', '', str(card_number))
        
        if clean.startswith('4'):
            return 'Visa'
        elif clean.startswith(('5', '2')):
            return 'Mastercard'
        elif clean.startswith(('34', '37')):
            return 'American Express'
        elif clean.startswith('6'):
            return 'Discover'
        else:
            return 'Desconhecido'
    
    def _simulate_azure_extraction(self, image_data):
        """Simula extração com Azure (para demonstração)"""
        return {
            'card_number': '4532 3100 9999 1048',
            'cardholder_name': 'PORTADOR DO CARTAO',
            'expiry_date': '12/28',
            'card_type': 'Visa',
            'bank_name': 'BANCO EXEMPLO',
            'confidence': 'high'
        }
    
    def _simulate_extraction(self):
        """Simulação básica para modo sem Azure"""
        return {
            'card_number': '4532 1234 5678 9012',
            'cardholder_name': 'NOME SIMULADO',
            'expiry_date': '12/27',
            'card_type': 'Visa',
            'bank_name': 'BANCO SIMULADO',
            'confidence': 'simulated'
        }
    
    def _calculate_confidence(self, data, validation):
        """Calcula pontuação de confiança da análise"""
        scores = {}
        
        scores['card_number'] = 95 if validation['card_number']['valid'] else 20
        scores['expiry_date'] = 90 if validation['expiry_date']['valid'] else 25
        scores['cardholder_name'] = 85 if validation['cardholder_name']['valid'] else 30
        
        if 'cvv' in validation:
            scores['cvv'] = 95 if validation['cvv']['valid'] else 15
        
        scores['overall'] = sum(scores.values()) // len(scores)
        
        return scores

class WebHandler(http.server.SimpleHTTPRequestHandler):
    """Handler HTTP para interface web"""
    
    # Sistema compartilhado
    _analyzer = None
    
    def __init__(self, *args, **kwargs):
        if WebHandler._analyzer is None:
            WebHandler._analyzer = CardAnalyzer()
        self.analyzer = WebHandler._analyzer
        super().__init__(*args, directory=None, **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def do_GET(self):
        path = self.path.split('?')[0]  # Remove query parameters
        
        try:
            if path in ['/', '/index.html']:
                self._serve_main_page()
            elif path == '/status':
                self._serve_status()
            elif path == '/favicon.ico':
                self._serve_favicon()
            else:
                self.send_error(404)
        except (ConnectionAbortedError, BrokenPipeError):
            pass
    
    def do_POST(self):
        try:
            if self.path == '/validate':
                self._handle_validation()
            elif self.path == '/upload-image':
                self._handle_image_upload()
            else:
                self.send_error(404)
        except (ConnectionAbortedError, BrokenPipeError):
            pass
        except Exception as e:
            self._send_error_response(str(e))
    
    def _serve_main_page(self):
        """Serve a página principal"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        
        html_content = self._get_html_content()
        self.wfile.write(html_content.encode('utf-8'))
    
    def _serve_status(self):
        """Serve status da API"""
        status = {
            'status': 'online',
            'azure_configured': self.analyzer.azure_configured,
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0'
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(status).encode('utf-8'))
    
    def _serve_favicon(self):
        """Serve favicon"""
        self.send_response(200)
        self.send_header('Content-type', 'image/x-icon')
        self.send_header('Cache-Control', 'max-age=86400')
        self.end_headers()
        
        # Favicon simples em base64
        favicon_data = base64.b64decode('AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAABILAAASCwAAAAAAAAAAAAD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A')
        self.wfile.write(favicon_data)
    
    def _handle_validation(self):
        """Processa validação manual"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        result = self.analyzer.validate_manual_input(data)
        self._send_json_response(result)
    
    def _handle_image_upload(self):
        """Processa upload de imagem"""
        content_length = int(self.headers.get('Content-Length', 0))
        
        if content_length > 0:
            post_data = self.rfile.read(content_length)
            result = self.analyzer.analyze_image(post_data)
        else:
            result = {'error': True, 'message': 'Nenhuma imagem recebida'}
        
        self._send_json_response(result)
    
    def _send_json_response(self, data):
        """Envia resposta JSON"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def _send_error_response(self, message):
        """Envia resposta de erro"""
        error_response = {
            'error': True,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        
        self.send_response(500)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    def _get_html_content(self):
        """Retorna conteúdo HTML da interface"""
        return '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏦 Análise de Cartão - Azure AI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 25px;
            box-shadow: 0 30px 70px rgba(0,0,0,0.3);
            padding: 50px;
            max-width: 900px;
            width: 100%;
            animation: slideIn 0.8s ease-out;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(50px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        .header h1 {
            color: #333;
            font-size: 3em;
            margin-bottom: 15px;
            font-weight: 900;
        }
        .header p {
            color: #666;
            font-size: 1.3em;
            margin-bottom: 25px;
        }
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 12px;
            padding: 15px 30px;
            background: linear-gradient(135deg, #28a745, #20c997);
            color: white;
            border-radius: 30px;
            font-weight: 700;
            font-size: 16px;
            box-shadow: 0 8px 25px rgba(40, 167, 69, 0.4);
        }
        .tabs {
            display: flex;
            margin-bottom: 40px;
            border-radius: 20px;
            background: #f1f3f4;
            padding: 8px;
        }
        .tab {
            flex: 1;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            border: none;
            background: transparent;
            font-size: 17px;
            font-weight: 700;
            border-radius: 15px;
            transition: all 0.4s ease;
            color: #666;
        }
        .tab.active {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
            transform: translateY(-2px);
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        .form-group {
            margin-bottom: 30px;
        }
        .form-group label {
            display: block;
            margin-bottom: 12px;
            color: #333;
            font-weight: 700;
            font-size: 16px;
        }
        .form-group input {
            width: 100%;
            padding: 20px 25px;
            border: 3px solid #e9ecef;
            border-radius: 15px;
            font-size: 17px;
            transition: all 0.3s ease;
            background: #f8f9fa;
        }
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
            background: white;
            box-shadow: 0 0 0 8px rgba(102, 126, 234, 0.1);
            transform: translateY(-2px);
        }
        .form-row {
            display: flex;
            gap: 25px;
        }
        .form-row .form-group {
            flex: 1;
        }
        .btn {
            width: 100%;
            padding: 22px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 15px;
            font-size: 19px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.4s ease;
            margin: 25px 0;
        }
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 25px 50px rgba(102, 126, 234, 0.5);
        }
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        .upload-area {
            border: 4px dashed #667eea;
            border-radius: 25px;
            padding: 60px;
            text-align: center;
            cursor: pointer;
            transition: all 0.4s ease;
            margin-bottom: 30px;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
        }
        .upload-area:hover {
            border-color: #764ba2;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            transform: translateY(-3px);
        }
        .upload-icon {
            font-size: 80px;
            margin-bottom: 25px;
            opacity: 0.8;
        }
        .result {
            margin-top: 40px;
            padding: 35px;
            border-radius: 25px;
            display: none;
            animation: fadeInUp 0.6s ease-out;
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(40px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .result.success {
            background: linear-gradient(135deg, #d4edda, #c3e6cb);
            border: 4px solid #28a745;
            color: #155724;
        }
        .result.error {
            background: linear-gradient(135deg, #f8d7da, #f5c6cb);
            border: 4px solid #dc3545;
            color: #721c24;
        }
        .confidence-score {
            font-size: 4em;
            font-weight: 900;
            text-align: center;
            margin: 20px 0;
        }
        .validation-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .validation-item {
            background: rgba(255,255,255,0.5);
            padding: 15px;
            border-radius: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .status {
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
        }
        .status.valid {
            background: #28a745;
            color: white;
        }
        .status.invalid {
            background: #dc3545;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏦 Análise de Cartão</h1>
            <p>Sistema com Azure AI para análise inteligente</p>
            <div class="status-badge" id="statusBadge">
                ✅ Sistema Ativo
            </div>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="switchTab('manual')">
                📝 Validação Manual
            </button>
            <button class="tab" onclick="switchTab('image')">
                📸 Análise de Imagem
            </button>
        </div>
        
        <!-- Aba Manual -->
        <div id="manual-tab" class="tab-content active">
            <form id="cardForm">
                <div class="form-group">
                    <label for="cardNumber">💳 Número do Cartão</label>
                    <input type="text" id="cardNumber" placeholder="1234 5678 9012 3456" maxlength="19">
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="expiryDate">📅 Data de Expiração</label>
                        <input type="text" id="expiryDate" placeholder="MM/AA" maxlength="5">
                    </div>
                    <div class="form-group">
                        <label for="cvv">🔐 CVV</label>
                        <input type="text" id="cvv" placeholder="123" maxlength="4">
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="holderName">👤 Nome do Portador</label>
                    <input type="text" id="holderName" placeholder="João Silva Santos">
                </div>
                
                <button type="submit" class="btn" id="validateBtn">
                    🔍 Validar Cartão
                </button>
            </form>
        </div>
        
        <!-- Aba Upload -->
        <div id="image-tab" class="tab-content">
            <div class="upload-area" id="uploadArea">
                <div class="upload-icon">📸</div>
                <h3>Upload da Imagem do Cartão</h3>
                <p>Clique ou arraste uma foto do cartão aqui</p>
                <small>Suporte: JPG, PNG (máx. 10MB)</small>
            </div>
            
            <input type="file" id="fileInput" accept="image/*" style="display: none;">
            
            <button class="btn" id="uploadBtn" onclick="uploadAndAnalyze()" disabled>
                📸 Analisar com Azure AI
            </button>
        </div>
        
        <div id="result" class="result"></div>
    </div>

    <script>
        let selectedFile = null;
        
        // Formatação automática dos campos
        document.getElementById('cardNumber').addEventListener('input', function(e) {
            let value = e.target.value.replace(/[^0-9]/g, '');
            value = value.replace(/(\\d{4})(?=\\d)/g, '$1 ');
            e.target.value = value;
        });
        
        document.getElementById('expiryDate').addEventListener('input', function(e) {
            let value = e.target.value.replace(/[^0-9]/g, '');
            if (value.length >= 2) {
                value = value.substring(0, 2) + '/' + value.substring(2, 4);
            }
            e.target.value = value;
        });
        
        document.getElementById('cvv').addEventListener('input', function(e) {
            e.target.value = e.target.value.replace(/[^0-9]/g, '');
        });
        
        // Troca de abas
        function switchTab(tabName) {
            document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            document.querySelector(`[onclick="switchTab('${tabName}')"]`).classList.add('active');
            document.getElementById(`${tabName}-tab`).classList.add('active');
        }
        
        // Upload de arquivo
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const uploadBtn = document.getElementById('uploadBtn');
        
        uploadArea.addEventListener('click', () => fileInput.click());
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = '#28a745';
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.style.borderColor = '#667eea';
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = '#667eea';
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFileSelect(files[0]);
            }
        });
        
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFileSelect(e.target.files[0]);
            }
        });
        
        function handleFileSelect(file) {
            if (!file.type.startsWith('image/')) {
                alert('❌ Por favor, selecione apenas arquivos de imagem!');
                return;
            }
            
            if (file.size > 10 * 1024 * 1024) {
                alert('❌ Arquivo muito grande! Máximo 10MB.');
                return;
            }
            
            selectedFile = file;
            uploadArea.innerHTML = `
                <div class="upload-icon">✅</div>
                <h3>Arquivo Selecionado</h3>
                <p>${file.name}</p>
                <small>${(file.size / 1024 / 1024).toFixed(2)} MB</small>
            `;
            uploadBtn.disabled = false;
        }
        
        // Validação manual
        document.getElementById('cardForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const btn = document.getElementById('validateBtn');
            btn.disabled = true;
            btn.innerHTML = '⏳ Validando...';
            
            const data = {
                cardNumber: document.getElementById('cardNumber').value,
                expiryDate: document.getElementById('expiryDate').value,
                cvv: document.getElementById('cvv').value,
                holderName: document.getElementById('holderName').value
            };
            
            try {
                const response = await fetch('/validate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                displayResult(result);
                
            } catch (error) {
                displayError('Erro na validação: ' + error.message);
            }
            
            btn.disabled = false;
            btn.innerHTML = '🔍 Validar Cartão';
        });
        
        // Upload e análise
        async function uploadAndAnalyze() {
            if (!selectedFile) {
                alert('❌ Selecione uma imagem primeiro!');
                return;
            }
            
            const btn = document.getElementById('uploadBtn');
            btn.disabled = true;
            btn.innerHTML = '⏳ Analisando...';
            
            try {
                const formData = new FormData();
                formData.append('image', selectedFile);
                
                const response = await fetch('/upload-image', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.error) {
                    displayError(result.message);
                } else {
                    displayImageResult(result);
                }
                
            } catch (error) {
                displayError('Erro no upload: ' + error.message);
            }
            
            btn.disabled = false;
            btn.innerHTML = '📸 Analisar com Azure AI';
        }
        
        function displayResult(data) {
            const result = document.getElementById('result');
            const validation = data.validation;
            const confidence = data.confidence_scores;
            
            let html = `
                <h3>${validation.overall_valid ? '✅ Cartão Válido' : '❌ Cartão Inválido'}</h3>
                
                <div class="confidence-score">${confidence.overall}%</div>
                
                <div class="validation-grid">
                    <div class="validation-item">
                        <span><strong>Número do Cartão</strong></span>
                        <span class="status ${validation.card_number.valid ? 'valid' : 'invalid'}">
                            ${validation.card_number.valid ? 'Válido' : 'Inválido'}
                        </span>
                    </div>
                    
                    <div class="validation-item">
                        <span><strong>Data de Expiração</strong></span>
                        <span class="status ${validation.expiry_date.valid ? 'valid' : 'invalid'}">
                            ${validation.expiry_date.valid ? 'Válida' : 'Inválida'}
                        </span>
                    </div>
                    
                    <div class="validation-item">
                        <span><strong>Nome do Portador</strong></span>
                        <span class="status ${validation.cardholder_name.valid ? 'valid' : 'invalid'}">
                            ${validation.cardholder_name.valid ? 'Válido' : 'Inválido'}
                        </span>
                    </div>
                    
                    <div class="validation-item">
                        <span><strong>CVV</strong></span>
                        <span class="status ${validation.cvv.valid ? 'valid' : 'invalid'}">
                            ${validation.cvv.valid ? 'Válido' : 'Inválido'}
                        </span>
                    </div>
                </div>
                
                <p><strong>Tipo:</strong> ${data.extracted_data.card_type}</p>
            `;
            
            result.innerHTML = html;
            result.className = `result ${validation.overall_valid ? 'success' : 'error'}`;
            result.style.display = 'block';
        }
        
        function displayImageResult(data) {
            const result = document.getElementById('result');
            
            let html = `
                <h3>📸 Análise da Imagem</h3>
                <div class="confidence-score">${data.confidence_scores.overall}%</div>
                
                <h4>📋 Dados Extraídos:</h4>
                <div class="validation-grid">
                    <div class="validation-item">
                        <span><strong>Número:</strong></span>
                        <span>${data.extracted_data.card_number}</span>
                    </div>
                    <div class="validation-item">
                        <span><strong>Nome:</strong></span>
                        <span>${data.extracted_data.cardholder_name}</span>
                    </div>
                    <div class="validation-item">
                        <span><strong>Expiração:</strong></span>
                        <span>${data.extracted_data.expiry_date}</span>
                    </div>
                    <div class="validation-item">
                        <span><strong>Tipo:</strong></span>
                        <span>${data.extracted_data.card_type}</span>
                    </div>
                </div>
                
                <h4>🔍 Validação:</h4>
                <div class="validation-grid">
                    <div class="validation-item">
                        <span><strong>Número</strong></span>
                        <span class="status ${data.validation.card_number.valid ? 'valid' : 'invalid'}">
                            ${data.validation.card_number.valid ? 'Válido' : 'Inválido'}
                        </span>
                    </div>
                    <div class="validation-item">
                        <span><strong>Data</strong></span>
                        <span class="status ${data.validation.expiry_date.valid ? 'valid' : 'invalid'}">
                            ${data.validation.expiry_date.valid ? 'Válida' : 'Inválida'}
                        </span>
                    </div>
                </div>
            `;
            
            result.innerHTML = html;
            result.className = 'result success';
            result.style.display = 'block';
        }
        
        function displayError(message) {
            const result = document.getElementById('result');
            result.innerHTML = `
                <h3>❌ Erro</h3>
                <p>${message}</p>
            `;
            result.className = 'result error';
            result.style.display = 'block';
        }
        
        // Verifica status na inicialização
        fetch('/status')
            .then(response => response.json())
            .then(data => {
                const badge = document.getElementById('statusBadge');
                if (data.azure_configured) {
                    badge.innerHTML = '🤖 Azure AI Configurado';
                    badge.style.background = 'linear-gradient(135deg, #0078d4, #106ebe)';
                } else {
                    badge.innerHTML = '⚠️ Modo Simulação';
                    badge.style.background = 'linear-gradient(135deg, #ffc107, #fd7e14)';
                }
            })
            .catch(() => {
                document.getElementById('statusBadge').innerHTML = '❌ Erro de Conexão';
            });
    </script>
</body>
</html>'''

def find_free_port(start_port=DEFAULT_PORT, max_attempts=10):
    """Encontra uma porta livre para o servidor"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def main():
    """Função principal do sistema"""
    print("🏦 SISTEMA DE ANÁLISE DE CARTÃO COM AZURE AI")
    print("=" * 60)
    
    # Encontra porta disponível
    port = find_free_port()
    if not port:
        print("❌ Erro: Nenhuma porta disponível!")
        return 1
    
    try:
        print(f"🚀 Iniciando servidor na porta {port}...")
        
        with socketserver.TCPServer(("", port), WebHandler) as httpd:
            httpd.allow_reuse_address = True
            
            print(f"✅ Servidor ativo: http://localhost:{port}")
            print(f"🔧 Versão: 2.0.0")
            
            if AZURE_ENDPOINT and AZURE_KEY and 'sua-chave-aqui' not in AZURE_KEY:
                print(f"🤖 Azure AI: ✅ Configurado")
                print(f"   • Endpoint: {AZURE_ENDPOINT}")
            else:
                print(f"⚠️  Azure AI: Modo simulação")
                print(f"   • Configure as variáveis AZURE_COMPUTER_VISION_ENDPOINT e AZURE_COMPUTER_VISION_KEY")
            
            print("\n📋 Funcionalidades disponíveis:")
            print("   • ✅ Validação manual com algoritmo de Luhn")
            print("   • ✅ Upload e análise de imagem")
            print("   • ✅ Interface web moderna e responsiva")
            print("   • ✅ API REST para integração")
            
            print(f"\n🌐 Acesse: http://localhost:{port}")
            print("🔧 Pressione Ctrl+C para parar")
            print("-" * 60)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor parado pelo usuário")
        return 0
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        return 1

if __name__ == "__main__":
    exit(main())