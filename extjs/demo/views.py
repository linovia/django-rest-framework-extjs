from __future__ import unicode_literals

from django.contrib.auth.models import User, Group
from django.http import Http404

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import clone_request

from extjs.demo.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # serializer_class = ExtUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)

        if serializer.is_valid():
            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)
            data = {
                'success': True,
                'data': serializer.data,
                'message': "",
            }
            return Response(data, status=status.HTTP_201_CREATED,
                            headers=headers)

        data = {
            'success': False,
            'data': {},  # serializer.errors,
            'message': "Errors",
        }
        # return Response(data, status=200)
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        self.object_list = self.filter_queryset(self.get_queryset())

        # Default is to allow empty querysets.  This can be altered by setting
        # `.allow_empty = False`, to raise 404 errors on empty querysets.
        if not self.allow_empty and not self.object_list:
            class_name = self.__class__.__name__
            error_msg = self.empty_error % {'class_name': class_name}
            raise Http404(error_msg)

        # Switch between paginated or standard style responses
        page = self.paginate_queryset(self.object_list)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(self.object_list, many=True)

        return Response({
            'success': True,
            'data': serializer.data,
            'message': "",
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        self.object = None
        try:
            self.object = self.get_object()
        except Http404:
            # If this is a PUT-as-create operation, we need to ensure that
            # we have relevant permissions, as if this was a POST request.
            self.check_permissions(clone_request(request, 'POST'))
            created = True
            save_kwargs = {'force_insert': True}
            success_status_code = status.HTTP_201_CREATED
        else:
            created = False
            save_kwargs = {'force_update': True}
            success_status_code = status.HTTP_200_OK

        serializer = self.get_serializer(self.object, data=request.DATA,
                                         files=request.FILES, partial=partial)

        if serializer.is_valid():
            self.pre_save(serializer.object)
            self.object = serializer.save(**save_kwargs)
            self.post_save(self.object, created=created)
            return Response({
                    'success': True,
                    'data': serializer.data,
                    'message': "",
                }, status=success_status_code)

        return Response({
                'success': False,
                'data': {},
                'message': repr(serializer.errors),
            }, status=status.HTTP_400_BAD_REQUEST)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
