from django.urls import include, path


app_name = "api"

urlpatterns = [

    path("schema/", include("abc_back.api.v1.schema.urls")),
    path("users/", include("abc_back.api.v1.users.urls")),
    path("product/", include("abc_back.api.v1.products.urls")),
    path("pages/", include("abc_back.api.v1.pages.urls")),
    path("blogs/", include("abc_back.api.v1.blogs.urls")),
    path("favorites/", include("abc_back.api.v1.favorites.urls")),
    path("questionary/", include("abc_back.api.v1.questionary.urls")),
]
