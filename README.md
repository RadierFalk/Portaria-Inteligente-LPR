🚗 Portaria Inteligente LPR (License Plate Recognition)

Este projeto utiliza Visão Computacional e Deep Learning para identificar placas de veículos em tempo real, consultar um banco de dados local e autorizar o acesso de moradores em uma portaria inteligente.

🛠️ Tecnologias UtilizadasLinguagem: 
    Python 3.10+Detecção de Objetos: YOLOv8 (Ultralytics) - Modelo treinado para detecção de área única da placa.
    OCR: EasyOCR - Para extração de texto com inteligência artificial.
    Banco de Dados: SQLite3 - Armazenamento leve para placas e nomes de moradores.
    Interface: OpenCV - Processamento de vídeo e interface visual.
    
📋 Pré-requisitosAntes de começar, você deve ter instalado:
    Python 3.10 ou superior.
    Anaconda ou Miniconda (Recomendado para gerenciamento de ambientes).
    C++ Build Tools (Necessário para algumas bibliotecas de visão computacional).
    
🚀 Instalação e Configuração1. 
    Criar Ambiente VirtualNo terminal (ou Anaconda Prompt), 
    execute:conda create -n portaria_lpr python=3.10
            conda activate portaria_lpr

Instalação das Bibliotecas (Versões Estáveis)
    //Instalar primeiro o pacote do Torch
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
    pip install -r requirements.txt

3. Estrutura do ProjetoCertifique-se de que os arquivos estão organizados assim:Plaintext/projeto-lpr
├── main.py            # Código principal do sistema
├── database.py        # Lógica do banco de dados SQLite
├── best.pt            # Seu modelo YOLOv8 treinado
├── portaria.db        # Banco de dados (gerado automaticamente)
└── README.md          # Este arquivo

💻 Como UsarConfigurar o Banco de Dados:No seu arquivo database.py, certifique-se de cadastrar as placas desejadas (Ex: OTM2X22 ou RIO2A18).

Executar o Sistema: python main.py

Funcionamento:
    Aproxime a placa da câmera.
    O retângulo Verde indica acesso liberado para moradores cadastrados.
    O retângulo Vermelho indica placa bloqueada ou não identificada.
    Pressione 'q' para encerrar o sistema.

🧠 Arquitetura de Software
    O sistema opera em um pipeline de três estágios:
    Detecção: O YOLOv8 localiza as coordenadas $(x, y)$ da placa no frame.
    Processamento: Um recorte (crop) da área da placa é enviado para uma thread separada para não travar o vídeo.
    OCR e Validação: O EasyOCR lê os caracteres, que são normalizados (correção de O/0 e I/1) e validados via Regex antes da consulta SQL.