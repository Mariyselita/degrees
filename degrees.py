import csv
import sys

from util import Node, QueueFrontier

# Asigna nombres a un conjunto de person_ids correspondientes
names = {}

# Asigna person_ids a un diccionario de: nombre, nacimiento, películas (un conjunto de movie_ids)
people = {}

# Asigna movie_ids a un diccionario de: título, año, estrellas (un conjunto de person_ids)
movies = {}


def load_data(directory):
    """
    Carga de datos de archivos CSV en la memoria.
    """
    # Carga personas
    with open(f"{directory}/people.csv", encoding="utf-8") as folder:
        reader = csv.DictReader(folder)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Carga películas
    with open(f"{directory}/movies.csv", encoding="utf-8") as folder:
        reader = csv.DictReader(folder)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Carga la relación
    with open(f"{directory}/stars.csv", encoding="utf-8") as folder:
        reader = csv.DictReader(folder)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Cargar datos de archivos en la memoria
    print("Cargando datos del directorio " + directory + '...')
    load_data(directory)
    print("Datos cargados.")

    source = person_id_for_name(input("Nombre: "))
    if source is None:
        sys.exit("Persona no encontrada.")
    target = person_id_for_name(input("Nombre: "))
    if target is None:
        sys.exit("Persona no encontrada.")

    path = shortest_path(source, target)

    if path is None:
        print("No conectado D_:")
    else:
        degrees = len(path)
        print(f"Hay {degrees} grados de separación.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} y {person2} protagonizó en {movie}")


def shortest_path(source, target):
    """
    Devuelve la lista más corta de pares (movie_id, person_id)
    que conectan la fuente con el objetivo.

    Si no hay una ruta posible, devuelve Ninguno.
    """
    # Inicializa el nodo con el primer nombre de la persona, sin datos de procedencia
    next = Node(state=source, parent=None, action=None)
    # Genera la instancia para la cola de personas
    queue = QueueFrontier()
    # Agrega a la instancia la primer nodo con la información de la primera persona
    queue.add(next)
    # Variable que inicializa una lista vacía, nos ayudará a saber si un nodo ya fue visitado
    visited = []

    # Entrará en ciclo hasta que la cola de personas este vacío
    while queue.empty() is False:
        next = queue.remove()  # Obtiene el último nodo de la cola
        visited.append(next.state)  # Agrega el nodo a la lista de visitados
        # obtiene un conjunto con los movie_id y las personas con las que participó
        neighbors = neighbors_for_person(next.state)
        # se recorre el conjunto obtenido
        for movie_id, person_id in neighbors:
            # Si la persona del conjunto obtenido no esta entre los visitados, procede a analizarlo
            if person_id not in visited:
                # genera un nodo con la información del elemento del conjunto
                node = Node(state=person_id, parent=next, action=movie_id)
                # se verifica el la persona del conjuto sea igual al
                # id de la segunda persona ingresada
                
                if person_id == target:
                    # en este caso ya se encontró una relación de nodos entre ambas personas
                    step = node
                    path = []
                    #en esta parte se va realizando el trazado de elementos que da origen a
                    #la relación entre las personas encontradas
                    while step.parent is not None:
                        path.append((step.action, step.state))
                        step = step.parent
                    return path[::-1]

                # para este punto  al ser distinto la persona del conjunto se agrega
                # a la cola principal, posteriormente continua con las demas personas del conjunto
                queue.add(node)
                # en dado caso de que no haya ocurrencias, se seguirá con el siguiente elemento de la pila 
                # e igual obtendra el conjunto de personas
    
    return None
    # En dado caso de que no encuentre nada, retorna None


def person_id_for_name(name):
    """
    Devuelve la identificación de IMDB para el nombre de una persona,
    resolviendo ambigüedades según sea necesario.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"¿Cuál '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Nombre: {name}, Nacimiento: {birth}")
        try:
            person_id = input("ID de la persona prevista: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Devuelve (movie_id, person_id) pares de personas
    que protagonizó con una persona determinada.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
