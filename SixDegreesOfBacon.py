import pandas as pd
from collections import deque, defaultdict
import json  # Usar json.loads ao invés de eval para segurança

# Carregar o dataset
movies = pd.read_csv("tmdb_5000_credits.csv")

# Construir o grafo
actor_to_movies = defaultdict(set)
movie_to_actors = defaultdict(set)

for _, row in movies.iterrows():
    try:
        movie_id = row['id']  # Presumindo que a coluna 'id' esteja presente
        cast = json.loads(row['cast'])  # Usar json.loads para parse do JSON

        # Garantir que 'cast' seja uma lista de dicionários
        cast_actors = [actor['name'] for actor in cast]
        
        for actor in cast_actors:
            actor_to_movies[actor].add(movie_id)
            movie_to_actors[movie_id].add(actor)
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Erro ao processar a linha com movie_id {row['id']}: {e}")

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

