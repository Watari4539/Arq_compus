import heapq
import multiprocessing
import random
import time


def quick_sort(arr):
    """Ordena una parte con Quick Sort iterativo de tres vías."""
    if len(arr) < 2:
        return arr

    pila = [(0, len(arr) - 1)]
    while pila:
        bajo, alto = pila.pop()
        while bajo < alto:
            pivote = arr[random.randint(bajo, alto)]
            menor = actual = bajo
            mayor = alto

            while actual <= mayor:
                if arr[actual] < pivote:
                    arr[menor], arr[actual] = arr[actual], arr[menor]
                    menor += 1
                    actual += 1
                elif arr[actual] > pivote:
                    arr[actual], arr[mayor] = arr[mayor], arr[actual]
                    mayor -= 1
                else:
                    actual += 1

            izquierda = (bajo, menor - 1)
            derecha = (mayor + 1, alto)
            tam_izq = izquierda[1] - izquierda[0]
            tam_der = derecha[1] - derecha[0]
            if tam_izq < tam_der:
                if derecha[0] < derecha[1]:
                    pila.append(derecha)
                bajo, alto = izquierda
            else:
                if izquierda[0] < izquierda[1]:
                    pila.append(izquierda)
                bajo, alto = derecha
    return arr


def quick_sort_paralelo(datos, pool):
    """Ordena fragmentos en procesos y combina sus resultados ordenados."""
    cantidad_partes = min(multiprocessing.cpu_count(), len(datos))
    tamano = (len(datos) + cantidad_partes - 1) // cantidad_partes
    partes = [datos[i:i + tamano] for i in range(0, len(datos), tamano)]
    partes_ordenadas = pool.map(quick_sort, partes)
    return list(heapq.merge(*partes_ordenadas))


def generar_datos_aleatorios(cantidad, max_value=1_000_000, semilla=42):
    rng = random.Random(semilla)
    return [rng.randint(0, max_value) for _ in range(cantidad)]


if __name__ == "__main__":
    EXPONENTES = list(range(1, 9))
    resultados = []
    procesos = multiprocessing.cpu_count()

    print("--- Prueba de Quick Sort PARALELO ---")
    print(f"Procesos disponibles: {procesos}")
    print(f"Exponentes: {EXPONENTES}")

    with multiprocessing.Pool(processes=procesos) as pool:
        for exponente in EXPONENTES:
            n = 10 ** exponente
            print(f"\nGenerando N={n:,} elementos...")
            datos = generar_datos_aleatorios(n)

            inicio = time.perf_counter()
            ordenados = quick_sort_paralelo(datos, pool)
            tiempo = time.perf_counter() - inicio

            assert ordenados == sorted(datos), "El resultado no se ordenó correctamente."
            resultados.append((exponente, n, tiempo))
            print(f"N={n:,}: {tiempo:.6f} segundos")

    print("\n| Exponente | N | Tiempo (segundos) |")
    print("|---:|---:|---:|")
    for exponente, n, tiempo in resultados:
        print(f"| 10^{exponente} | {n:,} | {tiempo:.6f} |")
