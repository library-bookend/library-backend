from rest_framework import serializers

class RatingSerializer(serializers.Serializer):
    rating = serializers.IntegerField(max_value=5, min_value=1)
    