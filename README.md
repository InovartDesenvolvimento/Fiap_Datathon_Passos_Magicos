# Datathon Passos Mágicos - Machine Learning Engineering

Este projeto foi desenvolvido como parte do Datathon da Pós-Tech FIAP, com o objetivo de criar um modelo preditivo para estimar o risco de defasagem escolar dos alunos da Associação Passos Mágicos.

## 🚀 Solução Proposta

A solução consiste em uma pipeline completa de Machine Learning, desde o processamento dos dados até a disponibilização de uma API para predições em tempo real.

### Stack Tecnológica
- **Linguagem:** Python 3.11
- **Framework ML:** Scikit-learn, Pandas, Joblib
- **API:** FastAPI
- **Containerização:** Docker
- **Testes:** Pytest

## 📁 Estrutura do Projeto
```text
.
├── app/
│   ├── main.py          # API FastAPI
│   └── models/          # Modelos serializados (.joblib)
├── tests/               # Testes unitários
├── Dockerfile           # Configuração do container
├── requirements.txt     # Dependências
├── train_model.py       # Script de treinamento do modelo
└── README.md            # Documentação
```

## 🛠️ Como Executar

### Pré-requisitos
- Docker instalado

### Executando com Docker
1. Construa a imagem:
   ```bash
   docker build -t passos-magicos-api .
   ```
2. Execute o container:
   ```bash
   docker run -p 8000:8000 passos-magicos-api
   ```

### Testando a API
Você pode testar a API enviando um POST para `/predict`:
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"data": {"feature1": 0.5, "feature2": 1.2}}'
```

## 🧪 Testes
Para executar os testes unitários:
```bash
pytest tests/
```

## 📊 Modelo e Métricas
O modelo utiliza um **Random Forest Classifier**. A métrica principal de avaliação foi a **Acurácia**, atingindo mais de 90% nos dados de teste. O modelo foi escolhido por sua robustez e capacidade de lidar com variáveis categóricas e numéricas simultaneamente.
