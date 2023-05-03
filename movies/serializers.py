from rest_framework import serializers

from .models import Movie


# create a new class called MovieSerializer from a ModelSerializer
# which outputs all the fields from the model
class MovieSerializer(serializers.ModelSerializer):
    # By identifying certain fields as "read only",
    # we can ensure that they will never be created or updated via the serializer
    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ('id', 'created_date', 'updated_date',)
