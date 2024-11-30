import pandas as pd
from collections import deque, defaultdict

# Carregar o dataset
movies = pd.read_csv("tmdb_5000_credits.csv")

# Construir o grafo
actor_to_movies = defaultdict(set)
movie_to_actors = defaultdict(set)

for _, row in movies.iterrows():
    movie_id = row['id']
    cast = eval(row['cast'])  # Cast é uma lista de dicionários (JSON)
    cast_actors = [actor['name'] for actor in cast]
    
    for actor in cast_actors:
        actor_to_movies[actor].add(movie_id)
        movie_to_actors[movie_id].add(actor)

# Função para encontrar a cadeia de conexão
def find_connection(actor1, actor2):
    if actor1 not in actor_to_movies or actor2 not in actor_to_movies:
        return "Sem conexão"

    queue = deque([(actor1, [])])  # Fila de BFS
    visited = set()               # Visitados

    while queue:
        current_actor, path = queue.popleft()
        
        if current_actor == actor2:
            return path + [actor2]

        visited.add(current_actor)

        # Explorar filmes do ator atual
        for movie in actor_to_movies[current_actor]:
            for co_actor in movie_to_actors[movie]:
                if co_actor not in visited:
                    queue.append((co_actor, path + [(current_actor, movie)]))

    return "Sem conexão"

# Testar
actor1 = "Kevin Bacon"
actor2 = "Tom Hanks"
connection = find_connection(actor1, actor2)
print(connection)
