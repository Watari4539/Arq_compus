import heapq
import multiprocessing
import random
import time


def insertion_sort(arr):
    """Ordena una parte con Insertion Sort."""
    for i in range(1, len(arr)):
        actual = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > actual:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = actual
    return arr


def insertion_sort_paralelo(datos, pool):
    """Ordena fragmentos en procesos y combina sus resultados ordenados."""
    cantidad_partes = min(multiprocessing.cpu_count(), len(datos))
    tamano = (len(datos) + cantidad_partes - 1) // cantidad_partes
    partes = [datos[i:i + tamano] for i in range(0, len(datos), tamano)]
    partes_ordenadas = pool.map(insertion_sort, partes)
    return list(heapq.merge(*partes_ordenadas))


def generar_datos_aleatorios(cantidad, max_value=1_000_000, semilla=42):
    rng = random.Random(semilla)
    return [rng.randint(0, max_value) for _ in range(cantidad)]


if __name__ == "__main__":
    EXPONENTES = list(range(1, 9))
    resultados = []
    procesos = multiprocessing.cpu_count()

    print("--- Prueba de Insertion Sort PARALELO ---")
    print(f"Procesos disponibles: {procesos}")
    print(f"Exponentes: {EXPONENTES}")

    with multiprocessing.Pool(processes=procesos) as pool:
        for exponente in EXPONENTES:
            n = 10 ** exponente
            print(f"\nGenerando N={n:,} elementos...")
            datos = generar_datos_aleatorios(n)

            inicio = time.perf_counter()
            ordenados = insertion_sort_paralelo(datos, pool)
            tiempo = time.perf_counter() - inicio

            assert ordenados == sorted(datos), "El resultado no se ordenó correctamente."
            resultados.append((exponente, n, tiempo))
            print(f"N={n:,}: {tiempo:.6f} segundos")

    print("\n| Exponente | N | Tiempo (segundos) |")
    print("|---:|---:|---:|")
    for exponente, n, tiempo in resultados:
        print(f"| 10^{exponente} | {n:,} | {tiempo:.6f} |")
