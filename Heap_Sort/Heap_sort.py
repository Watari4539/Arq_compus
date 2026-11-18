import random
import time


def heap_sort(arr):
    """Ordena la lista recibida en el mismo lugar y la devuelve."""
    result = arr
    n = len(result)

    def sift_down(root, end):
        while True:
            child = 2 * root + 1
            if child >= end:
                return
            if child + 1 < end and result[child] < result[child + 1]:
                child += 1
            if result[root] >= result[child]:
                return
            result[root], result[child] = result[child], result[root]
            root = child

    # Construir un max-heap.
    for start in range(n // 2 - 1, -1, -1):
        sift_down(start, n)

    # Extraer el máximo y colocarlo al final.
    for end in range(n - 1, 0, -1):
        result[0], result[end] = result[end], result[0]
        sift_down(0, end)

    return result


def generar_datos_aleatorios(cantidad, max_value=1_000_000, semilla=42):
    rng = random.Random(semilla)
    return [rng.randint(0, max_value) for _ in range(cantidad)]


if __name__ == "__main__":
    EXPONENTES = list(range(1, 9))
    resultados = []

    print("--- Prueba de rendimiento de Heap Sort (10^N) ---")
    print(f"Exponentes a probar: {EXPONENTES}")

    for exponente in EXPONENTES:
        n = 10 ** exponente
        print(f"\nGenerando lista para N = 10^{exponente} = {n:,} elementos...")
        datos = generar_datos_aleatorios(n)
        datos_para_ordenar = datos.copy()

        inicio = time.perf_counter()
        ordenados = heap_sort(datos_para_ordenar)
        tiempo = time.perf_counter() - inicio

        assert ordenados == sorted(datos), "El resultado no está ordenado correctamente."
        resultados.append((exponente, n, tiempo))
        print(f"Prueba de N={n:,} completada. Tiempo: {tiempo:.6f} segundos.")

    print("\n| Exponente | N (cantidad) | Tiempo (segundos) |")
    print("|-----------|--------------|-------------------|")
    for exponente, n, tiempo in resultados:
        print(f"| 10^{exponente:<7} | {n:<12,} | {tiempo:.6f}          |")
