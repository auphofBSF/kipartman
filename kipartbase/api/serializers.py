from rest_framework import serializers, exceptions
import api.models as models
from django.db.models import Q

class PartCategorySerializer(serializers.ModelSerializer):
    path = serializers.HyperlinkedIdentityField(view_name='parts-categories-detail')
    parent = serializers.HyperlinkedRelatedField(
        queryset=models.PartCategory.objects.all(),
        view_name='parts-categories-detail',
        allow_null=True
    )

    default_error_messages = {
        'recursive': 'Category cannot be child of itself.',
    }
    
    class Meta:
        model = models.PartCategory
        fields = ('id', 'path', 'name', 'parent')

    def update(self, instance, validated_data):
        # check that instance will not be child of itself
        parent = validated_data.get('parent', instance.parent)
        while parent is not None:
            if parent.id==instance.id:
                raise exceptions.PermissionDenied(self.default_error_messages['recursive'])
            parent = parent.parent
        return serializers.ModelSerializer.update(self, instance, validated_data)


# class SubPartSerializer(serializers.ModelSerializer, serializers.PrimaryKeyRelatedField):
#     path = serializers.HyperlinkedIdentityField(view_name='parts-detail')
#     category = serializers.HyperlinkedRelatedField(
#         queryset=models.PartCategory.objects.all(),
#         view_name='parts-categories-detail',
#         allow_null=True
#     )
#     footprint = serializers.HyperlinkedRelatedField(
#         queryset=models.Footprint.objects.all(),
#         view_name='footprints-detail',
#         allow_null=True
#     )
#     class Meta:
#         model = models.Part
#         fields = ('id', 'path', 'category', 'name', 'description', 'footprint', 'comment', 'parts')

class PartParameterSerializer(serializers.ModelSerializer):
    path = serializers.HyperlinkedIdentityField(view_name='part-parameters-detail')
    part = serializers.HyperlinkedRelatedField(
        queryset=models.Part.objects.all(),
        view_name='parts-detail',
        allow_null=True
    )
    unit = serializers.HyperlinkedRelatedField(
        queryset=models.Unit.objects.all(),
        view_name='units-detail',
        allow_null=True
    )
    min_prefix = serializers.HyperlinkedRelatedField(
        queryset=models.UnitPrefix.objects.all(),
        view_name='unitprefixes-detail',
        allow_null=True
    )
    nom_prefix = serializers.HyperlinkedRelatedField(
        queryset=models.UnitPrefix.objects.all(),
        view_name='unitprefixes-detail',
        allow_null=True
    )
    max_prefix = serializers.HyperlinkedRelatedField(
        queryset=models.UnitPrefix.objects.all(),
        view_name='unitprefixes-detail',
        allow_null=True
    )
    class Meta:
        model = models.PartParameter
        fields = ('id', 'path', 'part', 'name', 'description', 'unit', 'numeric', 'text_value', 'min_value', 'min_prefix', 'nom_value', 'nom_prefix', 'max_value', 'max_prefix')

    default_error_messages = {
        'already_exist': '%s: Parameter already exists.',
    }

    def create(self, validated_data):
        # check if name already exist
        if models.PartParameter.objects.filter(part=validated_data.get('part')).filter(name=validated_data.get('name')).count()>0:
            raise exceptions.PermissionDenied((self.default_error_messages['already_exist']) % (validated_data.get('name')))
        return super(PartParameterSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        # check if update to a name that already exist
        if models.PartParameter.objects.filter(part=validated_data.get('part')).filter(~Q(pk=instance.pk)).filter(name=validated_data.get('name')).count()>0:
            raise exceptions.PermissionDenied((self.default_error_messages['already_exist']) % (validated_data.get('name')))
        return super(PartParameterSerializer, self).update(instance, validated_data)


class ManufacturerSerializer(serializers.ModelSerializer):
    path = serializers.HyperlinkedIdentityField(view_name='manufacturers-detail')

    class Meta:
        model = models.Manufacturer
        fields = ('id', 'path', 'name', 'address', 'website', 'email', 'phone', 'comment')

    def create(self, validated_data):
        # check if name already exist
        if models.Manufacturer.objects.filter(name=validated_data.get('name')).count()>0:
            raise exceptions.PermissionDenied((self.default_error_messages['already_exist']) % (validated_data.get('name')))
        return super(ManufacturerSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        # check if update to a name that already exist
        if models.Manufacturer.objects.filter(~Q(pk=instance.pk)).filter(name=validated_data.get('name')).count()>0:
            raise exceptions.PermissionDenied((self.default_error_messages['already_exist']) % (validated_data.get('name')))
        return super(ManufacturerSerializer, self).update(instance, validated_data)


class PartManufacturerSerializer(serializers.ModelSerializer):
    path = serializers.HyperlinkedIdentityField(view_name='manufacturers-detail')
    part = serializers.HyperlinkedRelatedField(
        queryset=models.Part.objects.all(),
        view_name='parts-detail',
        allow_null=True
    )
    manufacturer = serializers.HyperlinkedRelatedField(
        queryset=models.Manufacturer.objects.all(),
        view_name='manufacturers-detail',
        allow_null=True
    )

    class Meta:
        model = models.PartManufacturer
        fields = ('id', 'path', 'part', 'manufacturer', 'part_name')


class DistributorSerializer(serializers.ModelSerializer):
    path = serializers.HyperlinkedIdentityField(view_name='distributors-detail')

    class Meta:
        model = models.Distributor
        fields = ('id', 'path', 'name', 'address', 'website', 'sku_url', 'email', 'phone', 'comment')

    default_error_messages = {
        'already_exist': '%s: Distributor already exists.',
    }

    def create(self, validated_data):
        # check if name already exist
        if models.Distributor.objects.filter(name=validated_data.get('name')).count()>0:
            raise exceptions.PermissionDenied((self.default_error_messages['already_exist']) % (validated_data.get('name')))
        return super(DistributorSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        # check if update to a name that already exist
        if models.Distributor.objects.filter(~Q(pk=instance.pk)).filter(name=validated_data.get('name')).count()>0:
            raise exceptions.PermissionDenied((self.default_error_messages['already_exist']) % (validated_data.get('name')))
        return super(DistributorSerializer, self).update(instance, validated_data)



class PartDistributorSerializer(serializers.ModelSerializer):
    path = serializers.HyperlinkedIdentityField(view_name='part-distributors-detail')
    part = serializers.HyperlinkedRelatedField(
        queryset=models.Part.objects.all(),
        view_name='parts-detail',
        allow_null=True
    )
    distributor = serializers.HyperlinkedRelatedField(
        queryset=models.Distributor.objects.all(),
        view_name='distributors-detail',
        allow_null=True
    )

    class Meta:
        model = models.PartDistributor
        fields = ('id', 'path', 'part', 'distributor', 'packaging_unit', 'unit_price', 'currency', 'sku')


class PartSerializer(serializers.ModelSerializer):
    path = serializers.HyperlinkedIdentityField(view_name='parts-detail')
    category = serializers.HyperlinkedRelatedField(
        queryset=models.PartCategory.objects.all(),
        view_name='parts-categories-detail',
        allow_null=True
    )
    footprint = serializers.HyperlinkedRelatedField(
        queryset=models.Footprint.objects.all(),
        view_name='footprints-detail',
        allow_null=True
    )
    parameters = PartParameterSerializer(
        many=True,
        read_only=True
    )
    distributors = PartDistributorSerializer(
        many=True,
        read_only=True
    )
    manufacturers = PartManufacturerSerializer(
        many=True,
        read_only=True
    )

    default_error_messages = {
        'already_in': 'Part already added',
        'recursive': 'Part cannot be child of itself.',
    }

    class Meta:
        model = models.Part
        fields = ('id', 'path', 'category', 'name', 'description', 'footprint', 'comment', 'parts', 'parameters', 'distributors', 'manufacturers', 'octopart', 'updated')

    def update(self, instance, validated_data):
        # check there is no recursion
        subparts = []
        for part in validated_data.get('parts'):
            subparts.append(part)
        while len(subparts)>0:
            subpart = subparts.pop()
            print "--", type(subpart), subpart.pk
            if subpart.pk==instance.pk:
                raise exceptions.PermissionDenied(self.default_error_messages['recursive'])
#            subpart = models.Part.objects.get(pk=subpart_id)
            for part in subpart.parts.all():
                subparts.append(part)
        return super(PartSerializer, self).update(instance, validated_data)


class FootprintCategorySerializer(serializers.ModelSerializer):
    path = serializers.HyperlinkedIdentityField(view_name='footprints-categories-detail')
    parent = serializers.HyperlinkedRelatedField(
        queryset=models.FootprintCategory.objects.all(),
        view_name='footprints-categories-detail',
        allow_null=True
    )

    default_error_messages = {
        'recursive': 'Category cannot be child of itself.',
    }
    
    class Meta:
        model = models.FootprintCategory
        fields = ('id', 'path', 'name', 'parent')

    def update(self, instance, validated_data):
        # check that instance will not be child of itself
        parent = validated_data.get('parent', instance.parent)
        while parent is not None:
            if parent.id==instance.id:
                raise exceptions.PermissionDenied(self.default_error_messages['recursive'])
            parent = parent.parent
        return serializers.ModelSerializer.update(self, instance, validated_data)


class FootprintSerializer(serializers.ModelSerializer):
    path = serializers.HyperlinkedIdentityField(view_name='footprints-detail')
    category = serializers.HyperlinkedRelatedField(
        queryset=models.FootprintCategory.objects.all(),
        view_name='footprints-categories-detail',
        allow_null=True
    )
    class Meta:
        model = models.Footprint
        fields = ('id', 'path', 'category', 'name', 'description', 'comment', 'image', 'footprint', 'snapeda')


class UnitSerializer(serializers.ModelSerializer):
    path = serializers.HyperlinkedIdentityField(view_name='units-detail')
    class Meta:
        model = models.Unit
        fields = ('id', 'path', 'name', 'symbol')


class UnitPrefixSerializer(serializers.ModelSerializer):
    path = serializers.HyperlinkedIdentityField(view_name='unitprefixes-detail')
    class Meta:
        model = models.UnitPrefix
        fields = ('id', 'path', 'name', 'symbol', 'power')
