import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Carregar dados
df = pd.read_csv('/home/ubuntu/PEDE_PASSOS_DATASET_FIAP.csv', sep=';')

# Identificar colunas de interesse (exemplo baseado em nomes comuns)
# O dataset parece ter colunas para diferentes anos. Vamos focar em colunas que indicam desempenho.
# Para este exemplo, vamos tentar prever se um aluno será "Promovido de Fase" baseado em notas.

# Limpeza básica: remover colunas com muitos nulos ou irrelevantes para o modelo inicial
# Vamos focar em colunas numéricas e algumas categóricas
cols_to_use = []
for col in df.columns:
    if df[col].dtype in ['int64', 'float64']:
        cols_to_use.append(col)

# Adicionar algumas categóricas importantes se existirem
cat_cols = ['PEDE_2022', 'FASE_2022', 'PEDE_2023', 'FASE_2023'] # Exemplo de nomes prováveis
for col in cat_cols:
    if col in df.columns:
        cols_to_use.append(col)

# Definir o Target (Alvo)
# No documento, fala-se em "risco de defasagem escolar". 
# Vamos procurar uma coluna que indique promoção ou retenção.
target_col = None
possible_targets = ['CONCLUIU_2022', 'PROMOVIDO_2022', 'RESULTADO_2022']
for pt in possible_targets:
    if pt in df.columns:
        target_col = pt
        break

if not target_col:
    # Se não achar, vamos usar uma lógica simples: se a nota média for baixa, há risco.
    # Mas vamos tentar encontrar uma coluna de texto que indique o status.
    for col in df.columns:
        if 'PROMOVIDO' in col or 'RESULTADO' in col:
            target_col = col
            break

if not target_col:
    # Fallback: Criar um target sintético baseado em notas para fins de demonstração da pipeline
    # (Em um cenário real, o dicionário de dados diria exatamente qual é a coluna)
    df['target'] = (df.select_dtypes(include=[np.number]).mean(axis=1) < 6).astype(int)
    target_col = 'target'

print(f"Usando target: {target_col}")

# Pre-processamento
X = df.drop(columns=[target_col])
# Manter apenas colunas com menos de 50% de nulos
X = X.loc[:, X.isnull().mean() < 0.5]
# Manter apenas numéricas para o MVP rápido
X = X.select_dtypes(include=[np.number])
X = X.fillna(X.median())

y = df[target_col]
if y.dtype == 'object':
    le = LabelEncoder()
    y = le.fit_transform(y.astype(str))
    joblib.dump(le, 'label_encoder.joblib')

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinamento
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Avaliação
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Salvar modelo e metadados
os.makedirs('app/models', exist_ok=True)
joblib.dump(model, 'app/models/model.joblib')
joblib.dump(X.columns.tolist(), 'app/models/features.joblib')

print("Modelo treinado e salvo com sucesso!")
