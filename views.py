import uuid
from authentication import authenticate
from models import Movie
from sanic import views, response
from sanic.exceptions import NotFound


class MovieView(views.HTTPMethodView):
    async def get(self, request):
        filter_params = {}
        for filter_key, value in request.args.items():
            filter_params[filter_key] = {"$regex": "/.*" + value[0] + ".*/"}
        movies = await Movie.find(
            {"name": "nilay"},
            as_raw=True
        )
        return response.json({
            'count': len(movies.objects),
            'data': movies.objects,
        }, status=201)

    @authenticate()
    async def post(self, request):
        movie = request.json
        movie["_id"] = uuid.uuid4().hex

        new_movie = await Movie.insert_one(movie) # for bulk create select insert_many
        movie = await Movie.find_one(
            {"_id": new_movie.inserted_id}, as_raw=True
        )
        return response.json({
            'data': movie,
            'count': 1,
        }, status=201)

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
