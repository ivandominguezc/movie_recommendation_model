#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


movies = pd.read_csv("C:/Users/Ivan/Desktop/portafolio_proyectos/tmdb_5000_movies.csv")


# In[3]:


credits = pd.read_csv("C:/Users/Ivan/Desktop/portafolio_proyectos/tmdb_5000_credits.csv")


# In[4]:


movies.head(1)


# In[5]:


credits.head()


# In[6]:


movies=movies.merge(credits,on='title')


# In[7]:


movies=movies[['genres','id','keywords','title','overview','cast','crew']]


# In[8]:


movies.head()


# In[9]:


movies.isnull().sum() #getting all null values


# In[10]:


movies.dropna(inplace=True)#droping all rows where there is null value


# In[11]:


movies.duplicated().sum()


# In[12]:


movies.iloc[0].genres #this format is in dictionary


# In[13]:


def convert(obj):
  L=[]
  for i in ast.literal_eval(obj): # here the obj passed in this helper fuction is in list of string format but we want it in the format of just list
    L.append(i["name"]);
  return L


# In[14]:


import ast
movies['genres']=movies['genres'].apply(convert)
movies['keywords']=movies['keywords'].apply(convert)


# In[15]:


def convert3(obj):
  L=[]
  counter=0
  for i in ast.literal_eval(obj): # here the obj passed in this helper fuction is in list of string format but we want it in the format of just list
    if counter !=3:
      L.append(i["name"]);
      L.append(i["character"])
      counter+=1
    else:
      break
  return L


# In[16]:


movies['cast']=movies['cast'].apply(convert3)
movies.head()


# In[17]:


def fetch_director(obj):
  L=[]
  for i in ast.literal_eval(obj): # here the obj passed in this helper fuction is in list of string format but we want it in the format of just list
    if i["job"] =="Director":
      L.append(i["name"]);
      break;
  return L


# In[18]:


movies['crew']=movies['crew'].apply(fetch_director)
movies.head()


# In[19]:


movies['overview']=movies['overview'].apply(lambda x:x.split())
movies.head()


# In[20]:


movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])


# In[21]:


# Crear la columna 'tags' en el DataFrame original
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# Crear un nuevo DataFrame con las columnas deseadas
new_df = movies[['id', 'genres', 'title', 'tags']].copy()

# Aplicar las transformaciones deseadas usando .loc
new_df.loc[:, 'tags'] = new_df['tags'].apply(lambda x: " ".join(x))
new_df.loc[:, 'tags'] = new_df['tags'].apply(lambda x: x.lower())


# In[22]:


new_df.loc[:, 'genres'] = new_df['genres'].apply(lambda x: " ".join(x))
new_df.loc[:, 'genres'] = new_df['genres'].apply(lambda x: x.lower())


# In[23]:


new_df.head(20)


# In[24]:


genero = input("Te ayudaremos eligiendo la pelicula! Que genero te gustaria ver?")


# In[25]:


print(f" Hola, las recomendaciones para ti de peliculas de {genero} son:")


# In[41]:


# Lista para almacenar películas ya recomendadas
already_recommended = []

def recommend_movies_by_genre(df, genre, num_recommendations=10):
    global already_recommended
    
    # Filtrar las películas que contienen el género especificado
    genre_movies = df[df['genres'].str.contains(genre, case=False)]
    
    # Excluir las películas que ya han sido recomendadas
    genre_movies = genre_movies[~genre_movies['title'].isin(already_recommended)]
    
    # Seleccionar las primeras 'num_recommendations' películas
    recommendations = genre_movies[['title']].head(num_recommendations)
    
    # Añadir las películas recomendadas a la lista de ya recomendadas
    already_recommended.extend(recommendations['title'].tolist())
    
    return recommendations


# In[48]:


genre_to_search = "action"
recommended_movies = recommend_movies_by_genre(new_df, genre_to_search)


# In[49]:


print(recommended_movies)


# In[53]:


# Función para interactuar con el usuario
def interact_with_user():
    while True:
        # (1) Preguntar el género
        genre = input("¿Qué género de película te gustaría ver? ")

        # (2) Preguntar cuántas películas quiere que se le recomiende
        while True:
            try:
                num_movies = int(input("¿Cuántas películas te gustaría que te recomendara? "))
                if num_movies > 0:
                    break
                else:
                    print("Por favor, ingresa un número mayor a 0.")
            except ValueError:
                print("Por favor, ingresa un número válido.")

        # (3) Recomendar películas
        recommendations = recommend_movies_by_genre(new_df, genre, num_recommendations=num_movies)

        # Mostrar las recomendaciones
        if not recommendations.empty:
            print("\nAquí tienes tus recomendaciones:")
            print(recommendations)
        else:
            print(f"\nLo siento, no tengo más películas de género '{genre}' para recomendarte.")

        # Preguntar si desea más recomendaciones
        more = input("\n¿Te gustaría recibir más recomendaciones? (sí/no): ").strip().lower()
        if more != 'sí' and more != 'si':
            print("Gracias por usar el recomendador de películas. ¡Hasta luego!")
            break

# Iniciar la interacción con el usuario
interact_with_user()


# In[ ]:




