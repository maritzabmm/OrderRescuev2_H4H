## Modelo XgBoost para Predecir Sustituciones de SKU

# Instalación de librerías
!pip install xgboost -q

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_recall_curve,
    auc,
    average_precision_score
)

from xgboost import XGBClassifier


# Carga del datos
df = pd.read_csv("/content/merged.csv")

print(df.shape)
print(df.head())


# Limpieza base
df["fecha_pedido"] = pd.to_datetime(df["fecha_pedido"], errors="coerce")

df["anio"] = df["fecha_pedido"].dt.year
df["dia_mes"] = df["fecha_pedido"].dt.day
df["mes"] = df["fecha_pedido"].dt.month
df["hora"] = df["fecha_pedido"].dt.hour
df["dia_semana"] = df["fecha_pedido"].dt.dayofweek

df["pedido_despues_6pm"] = (df["hora"] >= 18).astype(int)
df["fin_semana"] = (df["dia_semana"] >= 5).astype(int)


# Target
target = "fue_sustituida"

df = df[df[target].notna()].copy()
df[target] = df[target].astype(int)

y = df[target]


# Columnas que no se utilizarán
cols_no_usar = [
    "fue_sustituida",
    "sku_solicitado_cambio",
    "nombre_sku_solicitado_cambio",
    "status",
    "status_final",
    "fecha_pedido",
    "id_pedido"
]

X = df.drop(columns=cols_no_usar, errors="ignore")


# Codificación
cat_cols = X.select_dtypes(include=["object"]).columns.tolist()

for col in cat_cols:
    freq = X[col].value_counts(normalize=True)
    X[col] = X[col].map(freq)

X = X.replace([np.inf, -np.inf], np.nan).fillna(-1)


# Train - test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()


# Modelo XGBOOST
modelo = XGBClassifier(
    n_estimators=400,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.85,
    colsample_bytree=0.85,
    objective="binary:logistic",
    eval_metric="logloss",
    scale_pos_weight=scale_pos_weight,
    random_state=42,
    n_jobs=-1
)

modelo.fit(X_train, y_train)


# Evaluación con PR AUC
probabilidades = modelo.predict_proba(X_test)[:, 1]
predicciones = (probabilidades >= 0.50).astype(int)

precision, recall, thresholds = precision_recall_curve(
    y_test,
    probabilidades
)

pr_auc = auc(recall, precision)

average_precision = average_precision_score(
    y_test,
    probabilidades
)

print(f"PR AUC: {pr_auc:.4f}")
print(f"Average Precision: {average_precision:.4f}")

print("\nMatriz de confusión:")
print(confusion_matrix(y_test, predicciones))

print("\nReporte de clasificación:")
print(classification_report(y_test, predicciones))


# Resultado en porcentaje
resultados = X_test.copy()

resultados["real_fue_sustituida"] = y_test.values
resultados["probabilidad_sustitucion"] = probabilidades
resultados["porcentaje_sustitucion"] = probabilidades * 100
resultados["prediccion"] = predicciones

resultados.head()
