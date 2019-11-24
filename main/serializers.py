from rest_framework import serializers
from .models import Person


class PersonCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'
        read_only_fields = ['id', 'vector']


class PersonDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'
        read_only_fields = ['id', 'last_name', 'name', 'vector']


class PersonSetVectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'
        read_only_fields = ['id', 'last_name', 'name']






