import uuid
from authentication import authenticate
from models import Movie
from sanic import views, response
from sanic.exceptions import NotFound


class FooBar(views.HTTPMethodView):
    async def get(self, request):
        movies = await Movie.find(as_raw=True)
        return response.json(movies.objects)

    @authenticate()
    async def post(self, request):
        movie = request.json
        movie["_id"] = uuid.uuid4().hex

        new_movie = await Movie.insert_one(movie)
        movie = await Movie.find_one(
            {"_id": new_movie.inserted_id}, as_raw=True
        )
        return response.json(movie)

    @authenticate()
    async def put(self, request):
        movie = request.json
        id = movie['_id']
        update_result = await Movie.update_one({"_id": id}, {"$set": movie})

        if update_result.modified_count == 1:
            if (
                    updated_movie := await Movie.find_one({"_id": id}, as_raw=True)
            ) is not None:
                return response.json(updated_movie)

        if (
                existing_movie := await Movie.find_one({"_id": id}, as_raw=True)
        ) is not None:
            return response.json(existing_movie)

        raise NotFound(f"movie {id} not found")
    
    @authenticate()
    async def delete(self, request):
        movie = request.json
        id = movie['_id']
        delete_result = await Movie.delete_one({"_id": id})

        if delete_result.deleted_count == 1:
            return response.json({}, status=204)

        raise NotFound(f"movie {id} not found")
