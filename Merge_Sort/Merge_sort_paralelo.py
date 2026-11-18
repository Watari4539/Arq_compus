import multiprocessing
import math
import random
import time

# --- 1. Función de Combinación (Merge) Paralela ---
def merge(left, right):
    """Combina dos listas ordenadas en una sola lista ordenada."""
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

# --- 2. Función de Ordenación Secuencial Base para cada Proceso ---
def merge_sort_sequential(data):
    """Merge Sort secuencial recursivo utilizado por cada núcleo."""
    length = len(data)
    if length <= 1:
        return data
    
    middle = length // 2
    left = merge_sort_sequential(data[:middle])
    right = merge_sort_sequential(data[middle:])
    
    return merge(left, right)

# --- 3. Implementación de Merge Sort Paralelo ---
def merge_sort_parallel(data, pool, processes):
    """Divide la lista entre los núcleos del CPU y los procesa en paralelo."""
    
    # 1. DIVIDIR: Dividir la lista inicial en 'processes' partes (chunks)
    size = int(math.ceil(float(len(data)) / processes))
    data_chunks = [data[i * size:(i + 1) * size] for i in range(processes)]
    
    # 2. PARALELIZAR: map distribuye un chunk a cada núcleo para ser ordenado
    data_sorted_chunks = pool.map(merge_sort_sequential, data_chunks)

    # 3. COMBINAR: Mezclar secuencialmente las sub-listas resultantes
    while len(data_sorted_chunks) > 1:
        new_chunks = []
        for i in range(0, len(data_sorted_chunks) - 1, 2):
            merged_chunk = merge(data_sorted_chunks[i], data_sorted_chunks[i+1])
            new_chunks.append(merged_chunk)

        if len(data_sorted_chunks) % 2 != 0:
            new_chunks.append(data_sorted_chunks[-1])
            
        data_sorted_chunks = new_chunks
        
    return data_sorted_chunks[0]

# --- 4. Función para Generar Datos Aleatorios ---
def generar_datos_aleatorios(cantidad, max_value=1_000_000, semilla=42):
    """Genera una lista de números enteros aleatorios."""
    rng = random.Random(semilla)
    return [rng.randint(0, max_value) for _ in range(cantidad)]

# --- 5. Bloque de Ejecución Principal ---
if __name__ == '__main__':
    
    # Mismos tamaños que el programa secuencial: 10^1 hasta 10^8.
    EXPONENTES = list(range(1, 9))
    
    # Obtener el número de núcleos/hilos lógicos del CPU de tu equipo
    num_procesos = multiprocessing.cpu_count()
    
    resultados = []
    
    print(f"--- Prueba de Rendimiento de Merge Sort PARALELO (10^N) ---")
    print(f"Ejecutando en {num_procesos} núcleos de procesador")
    print(f"Exponentes a probar: {EXPONENTES}")
    print("------------------------------------------------------------")
    
    # Creamos el pool de procesos una sola vez fuera del ciclo
    pool = multiprocessing.Pool(processes=num_procesos)
    
    for exponente in EXPONENTES:
        N = 10 ** exponente
        
        print(f"\nGenerando lista para N = 10^{exponente} = {N:,} elementos...")
        
        # ⚠️ Generación de datos FUERA de la medición de tiempo
        unsorted_data = generar_datos_aleatorios(N)
        
        # ⏱️ Medición precisa solo de la ejecución del algoritmo
        start_time = time.perf_counter()

        sorted_data = merge_sort_parallel(unsorted_data, pool, num_procesos)

        end_time_total = time.perf_counter() - start_time
        assert sorted_data == sorted(unsorted_data), "El resultado no está ordenado correctamente."
        
        # Guardar resultado
        resultados.append({
            "Exponente": exponente,
            "N": N,
            "Tiempo (s)": end_time_total
        })
        
        print(f"✅ Prueba de N={N:,} completada. Tiempo: {end_time_total:.6f} segundos.")
        
    pool.close()
    pool.join()

    # --- TABLA DE RESUMEN ---
    print("\n\n========================================================")
    print("📊 RESUMEN DE TIEMPOS DE EJECUCIÓN PARALELO (N = 10^Exponente)")
    print("========================================================")
    print(f"| {'Exponente':<10} | {'N (Cantidad)':<15} | {'Tiempo (segundos)':<20} |")
    print(f"| {'-'*10:<10} | {'-'*15:<15} | {'-'*20:<20} |")
    
    for res in resultados:
        print(f"| 10^{res['Exponente']:<7} | {res['N']:<15,} | {res['Tiempo (s)']:.6f}{'':<14} |")
        
    print("========================================================")
