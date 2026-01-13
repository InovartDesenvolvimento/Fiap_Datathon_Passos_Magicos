from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI(title="Passos Mágicos - Predição de Defasagem Escolar")

# Carregar modelo e features
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models/model.joblib")
FEATURES_PATH = os.path.join(os.path.dirname(__file__), "models/features.joblib")

model = joblib.load(MODEL_PATH)
features = joblib.load(FEATURES_PATH)

class StudentData(BaseModel):
    data: dict

@app.get("/")
def read_root():
    return {"message": "API de Predição Passos Mágicos está online!"}

@app.post("/predict")
def predict(student: StudentData):
    try:
        # Converter dict para DataFrame
        df_input = pd.DataFrame([student.data])
        
        # Garantir que todas as features necessárias existam (preencher com 0 se faltar)
        for col in features:
            if col not in df_input.columns:
                df_input[col] = 0
        
        # Reordenar colunas
        df_input = df_input[features]
        
        # Predição
        prediction = model.predict(df_input)
        probability = model.predict_proba(df_input).tolist()
        
        return {
            "prediction": int(prediction[0]),
            "probability": probability[0],
            "risk_label": "Alto Risco" if prediction[0] == 1 else "Baixo Risco"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
