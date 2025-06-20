from src.models import Book, Review, Image, Favorite
from src.models.stat_views import PopularBook, TopAuthor, ReviewStats
from src.models.user import User
from src.schemas.book import BookSchema
from src.schemas.favorite import FavoriteSchema
from src.schemas.review import ReviewSchema
from src.schemas.image import ImageSchema
from src.schemas.statistics import PopularBookSchema, TopAuthorSchema, ReviewStatsSchema
from src.schemas.user import UserSchema, UserSchemaLogin, UserCodeSchema

from src.mappers.base import DataMapper


class UserDataMapper(DataMapper):
    model_database = User
    model_schema = UserSchema


class UserCodeDataMapper(DataMapper):
    model_database = User
    model_schema = UserCodeSchema


class UserLoginDataMapper(DataMapper):
    model_database = User
    model_schema = UserSchemaLogin


class BookDataMapper(DataMapper):
    model_database = Book
    model_schema = BookSchema


class ReviewDataMapper(DataMapper):
    model_database = Review
    model_schema = ReviewSchema


class FavoriteDataMapper(DataMapper):
    model_database = Favorite
    model_schema = FavoriteSchema


class ImageDataMapper(DataMapper):
    model_database = Image
    model_schema = ImageSchema


class PopularBookDataMapper(DataMapper):
    model_database = PopularBook
    model_schema = PopularBookSchema


class TopAuthorDataMapper(DataMapper):
    model_database = TopAuthor
    model_schema = TopAuthorSchema


class ReviewStatsDataMapper(DataMapper):
    model_database = ReviewStats
    model_schema = ReviewStatsSchema


UserMapper = UserDataMapper()
UserLoginMapper = UserLoginDataMapper()
UserCodeMapper = UserCodeDataMapper()
BookMapper = BookDataMapper()
ReviewMapper = ReviewDataMapper()
FavoriteMapper = FavoriteDataMapper()
ImageMapper = ImageDataMapper()
PopularBookMapper = PopularBookDataMapper()
TopAuthorMapper = TopAuthorDataMapper()
ReviewStatsMapper = ReviewStatsDataMapper()
