import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import Movie as MovieModel, db
from models import Genre as GenreModel
from sqlalchemy.orm import Session
from graphene import Int

class Movie(SQLAlchemyObjectType):
    class Meta:
        # movie_model = MovieModel # This is mapping to the movie model in our models.py
        model = MovieModel
        interfaces = (graphene.relay.Node,)
       
class Genre(SQLAlchemyObjectType):
    class Meta:
        # genre_model = GenreModel
        model = GenreModel
        interfaces = (graphene.relay.Node,) 

class Query(graphene.ObjectType):
    movies = graphene.List(Movie)
    genres = graphene.List(Genre)

    def resolve_movies(self, info): # Resolver
        return db.session.execute(db.select(MovieModel)).scalars()
        # return MovieModel.query.all()
    def resolve_genres(self, info):
        return db.session.execute(db.select(GenreModel)).scalars()
        # return GenreModel.query.all()


class AddMovie(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        director = graphene.String(required=True)
        year = graphene.Int(required=True)

    movie = graphene.Field(Movie)

    def mutate(self, info, title, director, year):
        with Session(db.engine) as session:
            with session.begin():
                movie = MovieModel(title=title, director=director, year=year)
                session.add(movie)
            
            session.refresh(movie)
            return AddMovie(movie=movie)

class AddGenre(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        movie_id = graphene.Int(required=True)

    genre = graphene.Field(Genre)

    def mutate(self, info, name, movie_id):
        with Session(db.engine) as session:
            with session.begin():
                genre = MovieModel(name=name, movie_id=movie_id)
                session.add(genre)
            
            session.refresh(genre)
            return AddGenre(genre=genre)
        
# Optional change for AddGenre mutation
# class AddGenre(graphene.Mutation):
#     class Arguments:
#         name = graphene.String(required=True)
#         movie_id = graphene.Int(required=True)

#     genre = graphene.Field(Genre)

#     def mutate(self, info, name, movie_id):
#         with Session(db.engine) as session:
#             with session.begin():
#                 genre = GenreModel(name=name, movie_id=movie_id)
#                 session.add(genre)
            
#             session.refresh(genre)
#             return AddGenre(genre=genre)

        
class UpdateMovie(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String(required=True)
        director = graphene.String(required=True)
        year = graphene.Int(required=True)

    movie = graphene.Field(Movie)

    def mutate(self, info, id, title, director, year):
        with Session(db.engine) as session:
            with session.begin():
                movie = session.execute(db.select(MovieModel).where(MovieModel.id == id)).scalars().first()
                if movie:
                    movie.title = title
                    movie.director = director
                    movie.year = year
                else:
                    return None
            session.refresh(movie)
            return UpdateMovie(movie=movie)

class UpdateGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)
        movie_id = graphene.Int(required=True)
        
    genre = graphene.Field(Genre)

    def mutate(self, info, id, name, movie_id):
        with Session(db.engine) as session:
            with session.begin():
                genre = session.execute(db.select(GenreModel).where(GenreModel.id == id)).scalars().first()
                if genre:
                    genre.name = name
                    genre.movie_id = movie_id
                else:
                    return None
            session.refresh(genre)
            return UpdateGenre(genre=genre)

        
class DeleteMovie(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    movie = graphene.Field(Movie)

    def mutate(self, info, id):
        with Session(db.engine) as session:
            with session.begin():
                movie = session.execute(db.select(MovieModel).where(MovieModel.id == id)).scalars().first()
                if movie:
                   session.delete(movie)
                else:
                    return None
            session.refresh(movie)
            return DeleteMovie(movie=movie)

class DeleteGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    genre = graphene.Field(Genre)

    def mutate(self, info, id):
        with Session(db.engine) as session:
            with session.begin():
                genre = session.execute(db.select(GenreModel).where(GenreModel.id == id)).scalars().first()
                if genre:
                   session.delete(genre)
                else:
                    return None
            session.refresh(genre)
            return DeleteGenre(genre=genre)


class Mutation(graphene.ObjectType):
    create_movie = AddMovie.Field()
    update_movie = UpdateMovie.Field()
    delete_movie = DeleteMovie.Field()
    create_genre = AddGenre.Field()
    update_genre = UpdateGenre.Field()
    delete_genre = DeleteGenre.Field()