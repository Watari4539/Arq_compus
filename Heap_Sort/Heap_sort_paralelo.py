import heapq
import multiprocessing
import random
import time


def heap_sort(arr):
    """Ordena una parte con Heap Sort."""
    n = len(arr)

    def sift_down(root, end):
        while True:
            child = 2 * root + 1
            if child >= end:
                return
            if child + 1 < end and arr[child] < arr[child + 1]:
                child += 1
            if arr[root] >= arr[child]:
                return
            arr[root], arr[child] = arr[child], arr[root]
            root = child

    for start in range(n // 2 - 1, -1, -1):
        sift_down(start, n)
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        sift_down(0, end)
    return arr


def heap_sort_paralelo(datos, pool):
    """Ordena fragmentos en procesos y combina sus resultados ordenados."""
    cantidad_partes = min(multiprocessing.cpu_count(), len(datos))
    tamano = (len(datos) + cantidad_partes - 1) // cantidad_partes
    partes = [datos[i:i + tamano] for i in range(0, len(datos), tamano)]
    partes_ordenadas = pool.map(heap_sort, partes)
    return list(heapq.merge(*partes_ordenadas))


def generar_datos_aleatorios(cantidad, max_value=1_000_000, semilla=42):
    rng = random.Random(semilla)
    return [rng.randint(0, max_value) for _ in range(cantidad)]


if __name__ == "__main__":
    EXPONENTES = list(range(1, 9))
    resultados = []
    procesos = multiprocessing.cpu_count()

    print("--- Prueba de Heap Sort PARALELO ---")
    print(f"Procesos disponibles: {procesos}")
    print(f"Exponentes: {EXPONENTES}")

    with multiprocessing.Pool(processes=procesos) as pool:
        for exponente in EXPONENTES:
            n = 10 ** exponente
            print(f"\nGenerando N={n:,} elementos...")
            datos = generar_datos_aleatorios(n)

            inicio = time.perf_counter()
            ordenados = heap_sort_paralelo(datos, pool)
            tiempo = time.perf_counter() - inicio

            assert ordenados == sorted(datos), "El resultado no se ordenó correctamente."
            resultados.append((exponente, n, tiempo))
            print(f"N={n:,}: {tiempo:.6f} segundos")

    print("\n| Exponente | N | Tiempo (segundos) |")
    print("|---:|---:|---:|")
    for exponente, n, tiempo in resultados:
        print(f"| 10^{exponente} | {n:,} | {tiempo:.6f} |")
