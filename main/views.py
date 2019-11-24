from django.shortcuts import render
import numpy as np
from PIL import Image
from uuid import UUID

from .models import Person

from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import PersonCreateSerializer, PersonSetVectorSerializer, PersonDetailSerializer


def validate_uuid4(uuid):
    """
    Проверяет совпадает ли переданны id формату UUID.
    Если совпадает возвращает True, если нет - False.
    """
    try:
        val = UUID(uuid, version=4)
    except ValueError:

        return False

    return True

def person_is_exist(id):
    """
    Проверяет есть ли объекта с переданным  id в БД, есть он есть
    возвращает объект, если его нет - False.
    """
    try:
        person = Person.objects.get(id=id)
    except ObjectDoesNotExist:

        return False

    return person


class PersonCreateView(APIView):

    def post(self, request):
        """
        http://127.0.0.1:8000/api/v1/person/create/

        Использует аргументы, передаваемые в теле POST запроса, для создания объекта в базе данных.
        """
        try:
            name = request.data['name']
            last_name = request.data['last_name']
            serializer = PersonCreateSerializer(data={'name': name, 'last_name': last_name})
            if serializer.is_valid(raise_exception=True):
                serializer.save()

            return Response(serializer.data, status.HTTP_201_CREATED)

        except MultiValueDictKeyError:
            pass

        return Response('400 Bad Request', status=status.HTTP_400_BAD_REQUEST)


class PersonsIdsListView(APIView):

    def get(self, request):
        """
        http://127.0.0.1:8000/api/v1/persons/
        Не принимает никаких аргументов.
        Если в БД присутствуют хотя бы один объект возвращает список с id.
        Если объекты отсутствуют, вовзвращает ошибку 404.
        """

        ids =  Person.objects.all().values('id')
        if ids:

            return Response(ids)

        return Response('404 Not Found', status=status.HTTP_404_NOT_FOUND)


class PersonDetailView(APIView):

    def get(self, request, id):
        """
        http://127.0.0.1:8000/api/v1/person/detail/<id>/
        Принимает аргумент из адресной строки и передает в функцию для проверки соответсвия UUID,
        если не соответсвует возвращает ошибку 400, далее проверяем есть ли объект в БД если нету то
        возвращает 404, еслить есть возвращает объект.
        """

        if validate_uuid4(id):
            person = person_is_exist(id)
            if person:
                serializer = PersonDetailSerializer(person)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response('404 Not Found', status=status.HTTP_404_NOT_FOUND)

        return Response("id does not match UUID pattern", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        """
        http://127.0.0.1:8000/api/v1/person/detail/<id>/
        Принимает id из адресной строки и изображение с ключом "vector" в теле PUT запроса
        раскладывает изображение в матрицу и преобразовывает в одномерный массив, осуществляя нормализацию.
        Сохраняет ветктор в поле объекта 'vector'.

        """

        person = Person.objects.get(id=id)

        try:
            img = Image.open(request.data['vector']).convert('L')
            arr = np.array(img)
            vector = list(arr.ravel() / 255)
            person.vector = vector[:len(vector)//100]
            person.save()
        except MultiValueDictKeyError:
            pass

        if person.vector:
            serializer = PersonSetVectorSerializer(person)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response('400 Bad Request ', status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        """
        http://127.0.0.1:8000/api/v1/person/detail/<id>/
        Принимает id из адресной строки, и проверяет есть пользовательс такми id,
        если есть - удаляет его, нет - возвращает 404.

        """

        try:
            person = Person.objects.get(id=id)
            person.delete()
            return Response('200 OK', status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            pass

        return Response('404 Not Found', status=status.HTTP_404_NOT_FOUND)



class CompareVectorsView(APIView):

    def get(self, request, id1, id2):
        """
        http://127.0.0.1:8000/api/v1/persons/compare/usr_1=<str:id>&usr_2=<str:id>/
        Принимает два id, производит поиск объектов с такими id, если такие объекты есть
        и у каждого в поле "vector" присутствует объект проводит их сравнение.
        """

        try:
            person1 = get_object_or_404(Person, id=id1)
            person2 = get_object_or_404(Person, id=id2)
            if person1.vector and person2.vector:
                euclidean_distance = np.linalg.norm(np.asarray(person1.vector) - np.asarray(person2.vector))

                return Response(euclidean_distance)

            return Response("One of the objects has no value in the 'vector' field", status=status.HTTP_404_NOT_FOUND)
        except:
            pass

        return Response('404 Not Found', status=status.HTTP_404_NOT_FOUND)


