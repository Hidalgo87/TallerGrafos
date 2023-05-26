"""
Recuerda instalar las librerias para que funcione correctamente el codigo usando las recomendaciones
del IDE o con los siguientes comandos pip en el cmd o consola local:

pip install networkx
pip install matplotlib
"""

import networkx as nx
import matplotlib.pyplot as plt


class NodoLista:

    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None


class Grafo:
    # Trabajaremos con grafos no dirigidos por lo que la matriz necesariamente tienen que ser cuadrada
    def __init__(self, dim):
        self.dim = dim
        self.matriz_adyacencia = [[0] * dim for _ in range(dim)]
        self.listaNombres = [None for _ in range(dim)]
        self.visitados = []
        self.Camino = []

    def obtener_matriz(self):
        return self.matriz_adyacencia

    def actualizar_matriz(self, nueva):
        self.matriz_adyacencia = nueva

    def imprimir_matriz(self):
        max_longitud = max(len(nombre) for nombre in self.listaNombres)  # Longitud máxima de los nombres

        cadena_nombres = " " * (max_longitud + 2)  # Espacios en blanco antes de los nombres
        for nombre in self.listaNombres:
            espacios = " " * (max_longitud - len(nombre))
            cadena_nombres = cadena_nombres + nombre + espacios + " "
        print(cadena_nombres)

        for i in range(self.dim):
            cadena = f"{self.listaNombres[i]} " + " " * (max_longitud - len(self.listaNombres[i]))
            for j in range(self.dim):
                cadena = cadena + " " * max_longitud + str(self.matriz_adyacencia[i][j])
            print(cadena)

    def visualizar_grafo_libreria(self):
        G = nx.Graph()

        # Agregar nodos al grafo
        for nombre in self.listaNombres:
            G.add_node(nombre)

        # Agregar aristas al grafo
        for i in range(self.dim):
            for j in range(self.dim):
                if self.matriz_adyacencia[i][j] != 0:
                    G.add_edge(self.listaNombres[i], self.listaNombres[j])

        # Dibujar el grafo
        pos = nx.spring_layout(G)  # Asignar posiciones a los nodos
        nx.draw_networkx_nodes(G, pos)
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_labels(G, pos)

        # Mostrar el grafo
        plt.axis('off')
        plt.show()

    def encontrar_camino(self, origen, destino):
        if origen in self.listaNombres:
            if destino in self.listaNombres:

                indice_origen = None
                indice_destino = None

                for i in range(0, len(self.listaNombres)):
                    if self.listaNombres[i] == origen:
                        indice_origen = i
                    if self.listaNombres[i] == destino:
                        indice_destino = i

                lista_conexiones = []  # Nombres de los elementos a los que esta conectado el elemnto origen

                for i in range(0, len(self.listaNombres)):
                    if self.matriz_adyacencia[indice_origen][i] == 1:
                        lista_conexiones.append(self.listaNombres[i])

                # print(f"conexiones {origen}: {lista_conexiones}")

                if destino in lista_conexiones:
                    self.Camino.append(f" {origen} -->  {destino} ")
                    return self.Camino

                else:
                    if lista_conexiones.count == 0:
                        return " ñ "
                    else:

                        self.visitados.append(origen)

                        for nuevo_origen in lista_conexiones:

                            if nuevo_origen in self.visitados:
                                continue
                            else:
                                self.Camino.append(f" {origen} --> ")
                                cadena = self.encontrar_camino(nuevo_origen, destino)
                                # print(f"cadena : {cadena}")
                                if cadena == "ñ" or cadena is None:
                                    self.Camino.pop()
                                    continue
                                else:
                                    return cadena
            else:
                print(f"El elemento {destino} no existe en el grafo")
        else:
            print(f"El elemento {origen} no existe en el grafo")

    def agregar_nodo(self, nombre_existente, nuevo_nombre):
        """Metodo para crear un nodo en el grafo y relacionarlos, o en su defecto
        si el lo que se recibe en nuevo_nombre ya existe se relaciona"""

        if nombre_existente not in self.listaNombres:
            print("El nodo ingresado como existente no se encontró en el grafo actual")
            nuevo_nombre_existente = solicitar_caracter("Ingrese el nombre del nodo existente : ")
            self.agregar_nodo(nuevo_nombre_existente, nuevo_nombre)
        else:
            index_existente = -1
            index_nuevo = -1
            for i in range(len(self.listaNombres)):
                if self.listaNombres[i] == nombre_existente:
                    index_existente = i
                if self.listaNombres[i] == nuevo_nombre:
                    # Si el nuevo_nombre está en la lista, se toma ese
                    index_nuevo = i
            # Si el nuevo_nombre no se encontró en la lista, entonces se amplia la matriz
            # y se agrega el nombre a la lista
            if index_nuevo == -1:
                self.listaNombres.append(nuevo_nombre)
                self.dim += 1
                index_nuevo = self.dim - 1
                copia_matriz = self.matriz_adyacencia
                self.matriz_adyacencia = [[0] * self.dim for _ in range(self.dim)]
                # el -1 es para que no toque la nueva fila y columna, pues no existia en la pasada, por lo que no
                # existe en la copia
                for i in range(0, self.dim - 1):
                    for j in range(0, self.dim - 1):
                        self.matriz_adyacencia[i][j] = copia_matriz[i][j]
            # Las dos posiciones simetricas deben conectarse
            self.matriz_adyacencia[index_existente][index_nuevo] = 1
            self.matriz_adyacencia[index_nuevo][index_existente] = 1


def solicitar_numero(mensaje):
    ingreso = input(mensaje)
    try:
        numero = int(ingreso)
    except Exception:
        print("Solo ingresa numeros mi bro")
        return solicitar_numero(mensaje)
    return numero


def solicitar_caracter(mensaje):
    ingreso = input(mensaje)
    if len(ingreso) != 1:
        print("Ingresa sólo un carácter (numero o letra)")
        return solicitar_caracter(mensaje)
    return ingreso


def crear_grafo():
    """Metodo para definir numero de elementos para el grafo, matriz de adyacencia con datos definidos"""
    dimension = solicitar_numero("Ingrese el numero de elementos que desea agregar al grafo : ")
    grafo = Grafo(dimension)
    for i in range(grafo.dim):
        caracter_recibido = solicitar_caracter(f"Cual es el nombre del elemento numero {i + 1} : ")
        while caracter_recibido in grafo.listaNombres:
            print("Ese nombre ya está registrado")
            caracter_recibido = solicitar_caracter(f"Cual es el nombre del elemento numero {i + 1} : ")
        grafo.listaNombres[i] = caracter_recibido

    print("\n")
    print("--------------- INFORMACIÓN IMPORTANTE -------------------")
    print("La diagonal principal se llenara de ceros automaticamente")
    print(" pues no pueden haber referencias hacia si mismos.")
    print("A continuacion llenaras la matriz con 1´s y 0´s")
    print(" donde los 1´s representan una relacion entre los elementos")
    print(" y los 0´s lo contrario.")
    print("---------------------------------------------------------")
    for i in range(0, dimension):
        print(f"Fila numero {i + 1}")
        for j in range(0, dimension):
            if i == j:
                print("Se ingresó el 0 de la diagonal principal")
                continue
            else:
                valor = solicitar_numero("Ingrese un 1 o un 0 : ")
                while valor != 1 and valor != 0:
                    valor = solicitar_numero("Oe, 1 o 0 : ")
                matriz = grafo.obtener_matriz()
                matriz[i][j] = valor
    return grafo


def InsertarEnListaLigada(node, value):
    original = node
    while node.siguiente is not None:
        node = node.siguiente
    node.siguiente = NodoLista(value)
    return original


def crearFila(arr):
    node = NodoLista(arr[0])
    for i in range(len(arr) - 1):
        node = InsertarEnListaLigada(node, arr[i + 1])
    node_return = NodoLista(node)
    return node_return


def obtenerLigada(raiz, lista):
    largo = len(lista)
    if largo == 0:
        return raiz
    else:
        raiz = lista[0]
        raiz.siguiente = obtenerLigada(raiz.siguiente, lista[1:])
        return raiz


def crearListaAdyacencia(matrix, i=0):
    lista = []
    for i in range(len(matrix[0])):
        nodo = crearFila(matrix[i])
        lista.append(nodo)
    lista_ligada = obtenerLigada(None, lista)
    return lista_ligada


def imprimirListaAdyacencia(raiz):
    original = raiz
    contador = 1
    while raiz.siguiente is not None:
        contador += 1
        raiz = raiz.siguiente
    imprimirConsecutivos(original, contador)


def imprimirConsecutivos(cabezas, contador, i=0):
    if contador == i:
        return
    else:
        print(obtenerStrFilaRaizHasta(cabezas.valor, contador))
        return imprimirConsecutivos(cabezas.siguiente, contador, i + 1)


def obtenerStrFilaRaizHasta(raiz, contador, i=0):
    if contador == i:
        return " "
    else:
        return str(raiz.valor) + obtenerStrFilaRaizHasta(raiz.siguiente, contador, i + 1)


def menu():
    haygrafo = False

    el_grafo = None

    while True:
        print("=== Menú Taller Grafos (Sólo funciona para grafos NO dirigidos) ===")
        print("1. Crear grafo")
        print("2. Visualizar grafo por matriz de adyacencia")
        print("3. Agregar nodo")
        print("4. Encontrar camino de A hasta B")
        print("5. (Plus) Cambiar de matriz de adyacencia a lista de adyacencia y mostrarla")
        print("6. (Plus) Visualizar grafo por grafico")
        print("7. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            if haygrafo:
                print("Ya hay un grafo creado, desea crear uno nuevo")
                while True:
                    seleccion = solicitar_caracter("s/n: ")
                    try:
                        int(seleccion)
                        print("s o n")
                    except Exception:
                        break
                if seleccion == "s":
                    el_grafo = crear_grafo()
                    haygrafo = True
                else:
                    pass
            else:
                el_grafo = crear_grafo()
                haygrafo = True

        elif opcion == "2":
            if haygrafo:
                el_grafo.imprimir_matriz()
            else:
                print("No hay un grafo creado, por favor seleccione la opcion 1 y cree uno :)")

        elif opcion == "3":
            if haygrafo:
                existente = solicitar_caracter("Ingrese el nombre del nodo existente : ")
                nuevo = solicitar_caracter("Ingrese el nombre del nodo (existente o nuevo): ")
                el_grafo.agregar_nodo(existente, nuevo)
            else:
                print("No hay un grafo creado, por favor seleccione la opcion 1 y cree uno :)")

        elif opcion == "4":
            if haygrafo:
                origen = solicitar_caracter("Ingrese el origen : ")
                destino = solicitar_caracter("Ingrese el destino : ")

                el_grafo.Camino = []
                el_grafo.visitados = []

                lista_camino = el_grafo.encontrar_camino(origen, destino)
                definitivo = ""
                if lista_camino is None:
                    definitivo = "No se encontró un camino"
                else:
                    for cadena in lista_camino:
                        definitivo += cadena

                print(definitivo)

            else:
                print("No hay un grafo creado, por favor seleccione la opcion 1 y cree uno :)")

        elif opcion == "5":
            if haygrafo:
                lista_ligada = crearListaAdyacencia(el_grafo.matriz_adyacencia)
                imprimirListaAdyacencia(lista_ligada)
            else:
                print("No hay un grafo creado, por favor seleccione la opcion 1 y cree uno :)")
        elif opcion == "6":
            el_grafo.visualizar_grafo_libreria()
        elif opcion == "7":
            print("¡Hasta luego!")
            break

        else:
            print("Opción inválida. Por favor, selecciona una opción válida.")


"""rafo = Grafo(6)
rafo.matriz_adyacencia = [
    [0, 1, 0, 1, 1, 0],
    [1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0]
]
rafo.listaNombres = ['A', 'B', 'C', 'D', 'E', 'F']
estring = ""
primero = "C"
objetivo = "E" """

menu()
