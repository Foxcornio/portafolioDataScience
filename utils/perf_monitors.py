# Por medio de estos decoradores medilos el flujo de trabajo.
import time
import os
import psutil
import cProfile
import pstats
import io

def monitor_memoria(func):
    """
    Medir el consumo de memoria RAM antes y después de la ejecución.

    Args:
        func (callable): La función a monitorear.
    """
    def envoltura(*args, **kwargs):
        proceso = psutil.Process(os.getpid())
        mem_inicial = proceso.memory_info().rss / (1024 ** 2)  # Convertir a MB
        
        resultado = func(*args, **kwargs)
        
        mem_final = proceso.memory_info().rss / (1024 ** 2)
        print(f"🧠 Memoria en '{func.__name__}': {mem_final - mem_inicial:.2f} MB usados.")
        return resultado
    return envoltura

def monitor_io(func):
    """
    Medir la actividad de lectura y escritura en disco (I/O).

    Args:
        func (callable): La función a monitorear.
    """
    def envoltura(*args, **kwargs):
        proceso = psutil.Process(os.getpid())
        io_inicial = proceso.io_counters()
        
        resultado = func(*args, **kwargs)
        
        io_final = proceso.io_counters()
        leido = (io_final.read_bytes - io_inicial.read_bytes) / 1024
        escrito = (io_final.write_bytes - io_inicial.write_bytes) / 1024
        print(f"💾 I/O en '{func.__name__}': {leido:.2f} KB leídos / {escrito:.2f} KB escritos.")
        return resultado
    return envoltura

def perfilador_detallado(func):
    """
    Realizar un perfilado estadístico de las llamadas internas (cProfile).

    Args:
        func (callable): La función a analizar.
    """
    def envoltura(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        
        resultado = func(*args, **kwargs)
        
        pr.disable()
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats(10)  # Mostramos solo las 10 llamadas más pesadas
        print(f"📊 Perfilado de '{func.__name__}':\n{s.getvalue()}")
        return resultado
    return envoltura

def cronometro(func):
    """
    Medir el tiempo de ejecución de la función decorada.

    Args:
        func (callable): La función cuyo rendimiento se desea evaluar.

    Returns:
        callable: La función envuelta que incluye la lógica de medición de tiempo.
    """
    def envoltura(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs) # Aquí se ejecuta la función original
        fin = time.time()
        print(f"\n⏱️  La función '{func.__name__}' tardó {fin - inicio:.4f} segundos.")
        return resultado
    return envoltura