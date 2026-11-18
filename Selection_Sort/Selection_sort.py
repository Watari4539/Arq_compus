import random
import time


def selection_sort(arr):
    """Ordena la lista recibida en el mismo lugar y la devuelve."""
    result = arr
    n = len(result)

    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if result[j] < result[min_index]:
                min_index = j
        if min_index != i:
            result[i], result[min_index] = result[min_index], result[i]

    return result


def generar_datos_aleatorios(cantidad, max_value=1_000_000, semilla=42):
    rng = random.Random(semilla)
    return [rng.randint(0, max_value) for _ in range(cantidad)]


if __name__ == "__main__":
    # Selection Sort es O(n^2); empieza con tamaños pequeños.
    EXPONENTES = list(range(1, 9))
    resultados = []

    print("--- Prueba de rendimiento de Selection Sort (10^N) ---")
    print(f"Exponentes a probar: {EXPONENTES}")

    for exponente in EXPONENTES:
        n = 10 ** exponente
        print(f"\nGenerando lista para N = 10^{exponente} = {n:,} elementos...")
        datos = generar_datos_aleatorios(n)
        datos_para_ordenar = datos.copy()

        inicio = time.perf_counter()
        ordenados = selection_sort(datos_para_ordenar)
        tiempo = time.perf_counter() - inicio

        assert ordenados == sorted(datos), "El resultado no está ordenado correctamente."
        resultados.append((exponente, n, tiempo))
        print(f"Prueba de N={n:,} completada. Tiempo: {tiempo:.6f} segundos.")

    print("\n| Exponente | N (cantidad) | Tiempo (segundos) |")
    print("|-----------|--------------|-------------------|")
    for exponente, n, tiempo in resultados:
        print(f"| 10^{exponente:<7} | {n:<12,} | {tiempo:.6f}          |")
