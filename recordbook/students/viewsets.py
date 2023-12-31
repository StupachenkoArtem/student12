from django.forms import model_to_dict
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Student, Group
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly, UserPermission
from .serializers import StudentSerializer, StudentDetailSerializer, GroupDetailSerializer, GroupSerializer
from .utils import StudentAPIPagination, GroupsAPIPagination


# class StudentAPIView(ListAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer

# class StudentAPIView(ListCreateAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
# def get(self, request):
#     st = Student.objects.all().values()
#     return Response({'students': list(st)})

# def post(self, request):
#     new_st = Student.objects.create(
#         first_name=request.data['first_name'],
#         last_name=request.data['last_name'],
#         middle_name=request.data['middle_name'],
#         is_study=request.data['is_study'],
#         group_id=request.data['group_id'],
#         slug=request.data['slug'],
#         photo=request.data['photo']
#     )
#     return Response({'group': model_to_dict(new_st)})


# class GroupAPIView(APIView):
#     def get(self, request):
#         gr = Group.objects.all().values()
#         return Response({'groups': list(gr)})
#
#     def post(self, request):
#         new_gr = Group.objects.create(
#             name=request.data['name'],
#             course=request.data['course'],
#             enrollment_year=request.data['enrollment_year']
#         )
#         return Response({'group': model_to_dict(new_gr)})


# class StudentAPIDetailView(RetrieveUpdateAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer


class GroupViewSet(viewsets.ModelViewSet):
    # queryset = Group.objects.all()
    pagination_class = GroupsAPIPagination
    permission_classes = (UserPermission, )

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'create':
            return GroupDetailSerializer
        return GroupSerializer

    def get_queryset(self):
        course = self.request.GET.get('course', '')
        group = self.request.GET.get('group', '')
        print(f'{course= }')
        print(f'{group= }')
        if course or group:
            return Group.objects.filter(course=course, name=group)
        else:
            return Group.objects.all()

    @action(methods=['get'], detail=True)
    def students(self, request, pk=None):
        students = Student.objects.filter(group_id=pk)
        return Response({'students': [f'{st.first_name}-{st.last_name}' for st in students]})


class StudentViewSet(viewsets.ModelViewSet):
    pagination_class = StudentAPIPagination
    permission_classes = (UserPermission, )
    # queryset = Student.objects.all()
    # serializer_class = StudentSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'create':
            return StudentDetailSerializer
        return StudentSerializer

    def get_queryset(self):
        group = self.request.GET.get('group', '')
        if group:
            return Student.objects.filter(group_id=group)
        else:
            return Student.objects.all()

    @action(methods=['get'], detail=False)
    def groups(self, request):
        groups = Group.objects.all()
        return Response({'groups': [f'{gr.course}-{gr.name}' for gr in groups]})

    @action(methods=['get'], detail=True)
    def group(self, request, pk=None):
        group = Group.objects.filter(pk=pk).first()
        if group:
            return Response({'group': f'{group.course}-{group.name}'})
        else:
            return Response({'group': 'Группа не найдена'})
