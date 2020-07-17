from abc import abstractmethod
from typing import Type

import pytest
from django.db import models
from factory.django import DjangoModelFactory
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnList


class AbstractModelTest:
    model: Type[models.Model]
    factory: Type[DjangoModelFactory]

    def get_test_unsaved_instance(self):
        return self.factory.build()

    def assert_equal_instances_excluding_id(self, first, second):
        for field_name, value in first.__dict__.items():
            if field_name == 'id' or field_name.startswith('_'):
                continue

            assert second.__getattribute__(field_name) == value

    @pytest.mark.django_db
    def test_should_save_new_instance(self):
        instance = self.get_test_unsaved_instance()

        instance.save()

        assert type(instance.id) == int
        assert type(instance.pk) == int
        self.model.objects.get(pk=instance.pk)

    @pytest.mark.django_db
    def test_should_save_updates(self):
        existing_instance = self.factory.create()
        old_id = existing_instance.id
        new_unsaved_instance = self.get_test_unsaved_instance()

        # Set new params
        for field_name, value in new_unsaved_instance.__dict__.items():
            if field_name == 'id' or field_name.startswith('_'):
                continue
            existing_instance.__setattr__(field_name, value)

        existing_instance.save()

        assert existing_instance.id == old_id
        self.assert_equal_instances_excluding_id(existing_instance, new_unsaved_instance)

    @pytest.mark.django_db
    def test_should_delete_an_instance(self):
        existing_instance = self.factory.create()
        pk = existing_instance.pk
        existing_instance.delete()

        assert existing_instance.id is None
        assert existing_instance.pk is None

        with pytest.raises(self.model.DoesNotExist):
            self.model._default_manager.get(pk=pk)

    def test_str_method(self):
        instance = self.factory.build()
        assert instance.__str__() == f'{self.model.__name__} object ({instance.id})'


class AbstractModelManagerTest:
    model: Type[models.Model]
    factory: Type[DjangoModelFactory]

    @abstractmethod
    def generate_model_kwargs(self) -> dict:
        pass

    @pytest.mark.django_db
    def test_should_create_new_instance(self):
        params = self.generate_model_kwargs()

        instance = self.model._default_manager.create(**params)

        assert type(instance.id) == int
        assert type(instance.pk) == int
        self.model._default_manager.get(pk=instance.pk)

    @pytest.mark.django_db
    def test_should_update_queryset_fields(self):
        instance = self.factory()
        new_values = self.generate_model_kwargs()

        self.model._default_manager.filter(pk=instance.pk).update(**new_values)

        instance.refresh_from_db()
        instance_dict = instance.__dict__
        for key, value in new_values.items():
            assert instance_dict[key] == value

    @pytest.mark.django_db
    def test_should_delete_queryset(self):
        instance = self.factory()

        self.model._default_manager.filter(pk=instance.pk).delete()

        with pytest.raises(self.model.DoesNotExist):
            self.model._default_manager.get(pk=instance.pk)


class AbstractModelSerializerTest:
    serializer_class: Type[serializers.ModelSerializer]
    factory: Type[DjangoModelFactory]
    model: Type[models.Model]

    @abstractmethod
    def generate_parsable_data(self) -> dict:
        pass

    def check_fields_for_existing(self, data: dict):
        fields = self.serializer_class.Meta.fields
        data_fields = data.keys()

        for field_name in fields:
            assert field_name in data_fields

    def check_field_values(self, json_data: dict, instance):
        fields = self.serializer_class.Meta.fields

        for field in fields:
            assert instance.serializable_value(field) == json_data[field]

    @pytest.mark.django_db
    def test_serializer_data(self):
        instance = self.factory()

        serializer = self.serializer_class(instance)

        self.check_field_values(serializer.data, instance)

    @pytest.mark.django_db
    def test_should_wrap_to_list_if_many_is_true(self):
        _first, _second = self.factory(), self.factory()
        queryset = self.model._default_manager.all()

        serializer = self.serializer_class(queryset, many=True)

        assert type(serializer.data) == ReturnList
        assert len(serializer.data) == len(queryset)
        for instance_json in serializer.data:
            self.check_fields_for_existing(instance_json)

    @pytest.mark.django_db
    def test_should_save_new_instance(self):
        data = self.generate_parsable_data()
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        assert type(instance.pk) == int
        self.model._default_manager.get(pk=instance.pk)

    @pytest.mark.django_db
    def test_should_update_existing_instance_data(self):
        instance = self.factory()
        new_data = self.generate_parsable_data()
        new_data['id'] = instance.id
        serializer = self.serializer_class(instance, data=new_data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()
        for key, value in new_data.items():
            assert instance.serializable_value(key) == value
