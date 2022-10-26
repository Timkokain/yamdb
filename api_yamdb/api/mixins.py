from rest_framework import mixins, viewsets


class CreateOrDeleteListViewSet(mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                mixins.DestroyModelMixin,
                                viewsets.GenericViewSet):
    pass
