from django.db.models import F, Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (FollowSerializer, IngredientSerializer,
                             RecipeSerializer, TagSerializer, UsersSerializer)

from recipes.models import (Favorite, Follow, Ingredient, IngredientAmount,
                            Recipe, ShoppingCart, Tag)
from users.models import User


class TagViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с тегами."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с ингредиентами."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter


class UsersViewSet(UserViewSet):
    """Вьюсет для работы с пользователями и подписками. """

    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(
            detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)
        if request.method == 'POST':
            serializer = FollowSerializer(author,
                                          data=request.data,
                                          context={'request': request})
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            get_object_or_404(Follow, user=user, author=author).delete()
            return Response({'detail': 'Вы успешно отписались'},
                            status=status.HTTP_204_NO_CONTENT)

    @action(
            detail=False,
            permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        serializer = FollowSerializer(
            self.paginate_queryset(
                User.objects.filter(following__user=request.user)
            ),
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с рецептами."""

    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def recipe_add(self, model, request, **kwargs):
        user = request.user
        recipe_id = self.kwargs.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        serializer = RecipeSerializer(recipe, data=request.data,
                                      context={'request': request})
        serializer.is_valid(raise_exception=True)
        if not model.objects.filter(recipe=recipe, user=user).exists():
            model.objects.create(recipe=recipe, user=request.user)
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED
            )
        return Response({'errors': 'Рецепт уже добавлен.'},
                        status=status.HTTP_400_BAD_REQUEST)

    def recipe_delete(self, model, request, **kwargs):
        user = request.user
        recipe_id = self.kwargs.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        get_object_or_404(model, user=user, recipe=recipe).delete()
        return Response({'detail': 'Рецепт удален.'},
                        status=status.HTTP_204_NO_CONTENT)

    @action(
            detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, id):
        if request.method == 'POST':
            return self.recipe_add(Favorite, request, id)
        else:
            return self.recipe_delete(Favorite, request, id)

    @action(
            detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, id):
        if request.method == 'POST':
            return self.recipe_add(ShoppingCart, request, id)
        else:
            return self.recipe_delete(ShoppingCart, request, id)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = IngredientAmount.objects.filter(
            recipe__shopping_cart__user=user).values(
            name=F('ingredient__name'),
            unit=F('ingredient__unit')).annotate(
            amount=Sum('amount')
        )
        data = []
        for ingredient in ingredients:
            data.append(
                f'{ingredient["name"]} - '
                f'{ingredient["amount"]} '
                f'{ingredient["unit"]}'
            )
        content = 'Список покупок:\n\n' + '\n'.join(data)
        filename = 'shopping_cart.txt'
        request = HttpResponse(content, content_type='text/plain')
        request['Content-Disposition'] = f'attachment; filename={filename}'
        return request
