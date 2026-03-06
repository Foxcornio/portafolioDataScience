import kagglehub, os, random, pandas as pd, time, json as js

def cronometro(func):
    def envoltura(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs) # Aquí se ejecuta tu evaluador
        fin = time.time()
        print(f"\n⏱️  La función '{func.__name__}' tardó {fin - inicio:.4f} segundos.")
        return resultado
    return envoltura

@cronometro
def evaluador_analitico(y_real, y_pred):
    # Inicializamos los contadores de los conjuntos
    tp = 0  # Verdaderos Positivos (S ∩ P)
    fp = 0  # Falsos Positivos (H ∩ P)
    tn = 0  # Verdaderos Negativos
    fn = 0  # Falsos Negativos
    
    # Recorremos ambas listas al mismo tiempo usando un índice
    for i in range(len(y_real)):
        real = y_real[i]
        pred = y_pred[i]
       # print(f"\nDato real: {real}\nDato predictivo: {pred}\n")
        # Aplicamos la lógica de intersecciones
        if real == 1:
            if pred == 1:
                tp += 1  # Intersección exitosa de fraude (S ∩ P)
                #print("Fraude detectado\n")
            else:
                fn += 1  # El fraude se escapó
                #print("Error se filtro.")
        else:
            if pred == 1:
                fp += 1  # Intersección de error con humano (H ∩ P) 
                #print("Alerta posible fraude\n")
            else:
                tn += 1  # Se identificó correctamente como normal
               # print("Operación normal")
                
    return tp, fp, tn, fn

@cronometro
def descarga_datos(ruta:str):
  # Download dataset
  path = kagglehub.dataset_download(ruta)
  # file path to study
  return os.path.join(path, 'creditcard.csv')

@cronometro
def calcular_metricas(tp: int, fp: int, tn: int, fn: int) -> dict[str, float]:
    # Recall: ¿De todos los fraudes reales, cuántos detectamos?
    recall: float = tp / (tp + fn) if (tp + fn) > 0 else 0
    
    # Tasa de Falsos Positivos: ¿A qué % de clientes honestos molestamos?
    fpr: float = fp / (fp + tn) if (fp + tn) > 0 else 0
    
    # Precisión: De lo que dijimos que era fraude, ¿cuánto lo fue realmente?
    precision: float = tp / (tp + fp) if (tp + fp) > 0 else 0
    
    return {"Fraudes detectados": recall, "Clientes afectados": fpr, "Acertividad vs Pronostico": precision}

@cronometro
def analisis_financiero(fp: int, fn: int):
    perdida_por_fraude: int = fn * 2000
    costo_operativo_soporte: int = fp * 150
    impacto_total: int = perdida_por_fraude + costo_operativo_soporte
    
    print("\n--- ANÁLISIS ECONÓMICO ---")
    print(f"💸 Dinero perdido por fraudes no detectados (FN): ${perdida_por_fraude:,} MXN")
    print(f"📞 Costo de atención por bloqueos erróneos (FP): ${costo_operativo_soporte:,} MXN")
    print(f"⚠️  IMPACTO TOTAL AL NEGOCIO: ${impacto_total:,} MXN")

@cronometro
def new_data(data:object):
    y_pred = []
    for valor in data:
        if random.random() < .96:
            y_pred.append(valor)
        else:
            y_pred.append(1 - valor)
    return y_pred

    
data = pd.read_csv(descarga_datos("isaikumar/creditcardfraud")) # init pd read

y_real = data['Class'].tolist() # separe Class colum
# Output the number of items in y_real
print(f"Total de registros : {len(y_real)} registros")

y_pred = new_data(y_real) # Create a group module

# Matriz de confusion        
tp, fp, tn, fn = evaluador_analitico(y_real, y_pred)

print("--- RESULTADOS DEL EVALUADOR ---")
print(f"Verdaderos Positivos (Fraudes detectados): {tp}")
print(f"Falsos Positivos (Clientes bloqueados): {fp}")
print(f"Verdaderos Negativos (Normales correctos): {tn}")
print(f"Falsos Negativos (Fraudes escapados): {fn}")
print("___________________________\n")
metricas = calcular_metricas(tp,fp,tn,fn)

analisis_financiero(fp,fn)
for k,v in metricas.items():
  por = v * 100;
  print(f"{k} : {por:.2f}% \n")