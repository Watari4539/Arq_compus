import random
import time


def insertion_sort(arr):
    """Ordena la lista recibida en el mismo lugar y la devuelve."""
    result = arr

    for i in range(1, len(result)):
        current = result[i]
        j = i - 1
        while j >= 0 and result[j] > current:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = current

    return result


def generar_datos_aleatorios(cantidad, max_value=1_000_000, semilla=42):
    rng = random.Random(semilla)
    return [rng.randint(0, max_value) for _ in range(cantidad)]


if __name__ == "__main__":
    # Insertion Sort es O(n^2) en promedio; empieza con tamaños pequeños.
    EXPONENTES = list(range(1, 9))
    resultados = []

    print("--- Prueba de rendimiento de Insertion Sort (10^N) ---")
    print(f"Exponentes a probar: {EXPONENTES}")

    for exponente in EXPONENTES:
        n = 10 ** exponente
        print(f"\nGenerando lista para N = 10^{exponente} = {n:,} elementos...")
        datos = generar_datos_aleatorios(n)
        datos_para_ordenar = datos.copy()

        inicio = time.perf_counter()
        ordenados = insertion_sort(datos_para_ordenar)
        tiempo = time.perf_counter() - inicio

        assert ordenados == sorted(datos), "El resultado no está ordenado correctamente."
        resultados.append((exponente, n, tiempo))
        print(f"Prueba de N={n:,} completada. Tiempo: {tiempo:.6f} segundos.")

    print("\n| Exponente | N (cantidad) | Tiempo (segundos) |")
    print("|-----------|--------------|-------------------|")
    for exponente, n, tiempo in resultados:
        print(f"| 10^{exponente:<7} | {n:<12,} | {tiempo:.6f}          |")
