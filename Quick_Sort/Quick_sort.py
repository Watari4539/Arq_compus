import random
import time


def quick_sort(arr):
    """Ordena la lista recibida en el mismo lugar con Quick Sort iterativo."""
    result = arr
    if len(result) < 2:
        return result

    # Pila de rangos inclusivos; la versión iterativa evita límites recursivos.
    stack = [(0, len(result) - 1)]
    while stack:
        low, high = stack.pop()
        while low < high:
            pivot_index = random.randint(low, high)
            pivot = result[pivot_index]
            # Partición de tres vías: agrupa valores iguales en una sola pasada.
            less = current = low
            greater = high
            while current <= greater:
                if result[current] < pivot:
                    result[less], result[current] = result[current], result[less]
                    less += 1
                    current += 1
                elif result[current] > pivot:
                    result[current], result[greater] = result[greater], result[current]
                    greater -= 1
                else:
                    current += 1

            # Procesar primero el rango menor para limitar el tamaño de la pila.
            left = (low, less - 1)
            right = (greater + 1, high)
            left_size = left[1] - left[0]
            right_size = right[1] - right[0]
            if left_size < right_size:
                if right[0] < right[1]:
                    stack.append(right)
                low, high = left
            else:
                if left[0] < left[1]:
                    stack.append(left)
                low, high = right

    return result


def generar_datos_aleatorios(cantidad, max_value=1_000_000, semilla=42):
    rng = random.Random(semilla)
    return [rng.randint(0, max_value) for _ in range(cantidad)]


if __name__ == "__main__":
    EXPONENTES = list(range(1, 9))
    resultados = []

    print("--- Prueba de rendimiento de Quick Sort (10^N) ---")
    print(f"Exponentes a probar: {EXPONENTES}")

    for exponente in EXPONENTES:
        n = 10 ** exponente
        print(f"\nGenerando lista para N = 10^{exponente} = {n:,} elementos...")
        datos = generar_datos_aleatorios(n)
        datos_para_ordenar = datos.copy()

        inicio = time.perf_counter()
        ordenados = quick_sort(datos_para_ordenar)
        tiempo = time.perf_counter() - inicio

        assert ordenados == sorted(datos), "El resultado no está ordenado correctamente."
        resultados.append((exponente, n, tiempo))
        print(f"Prueba de N={n:,} completada. Tiempo: {tiempo:.6f} segundos.")

    print("\n| Exponente | N (cantidad) | Tiempo (segundos) |")
    print("|-----------|--------------|-------------------|")
    for exponente, n, tiempo in resultados:
        print(f"| 10^{exponente:<7} | {n:<12,} | {tiempo:.6f}          |")
