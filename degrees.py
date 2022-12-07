import csv
import sys

from util import Node, StackFrontier, QueueFrontier

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
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
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
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Carga la relación
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
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
    print("Cargando datos...")
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
        print(f"{degrees} grados de separación.")
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

    # TODO
    raise NotImplementedError


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
