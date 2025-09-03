from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('watchlist',)
        

class WatchListSerializer(serializers.ModelSerializer):    
     # Accept ID on input, but don't show it in responses
    platform = serializers.PrimaryKeyRelatedField(
        queryset=StreamPlatform.objects.all(),
        write_only=True 
    )
    # Show human-readable name in responses
    platform_name = serializers.CharField(source='platform.name', read_only=True)

    class Meta:
        model = WatchList
        fields = [
            "id", "title", "storyline",
            "platform",        # id (writable)
            "platform_name",   # name (read-only)
            "active", "avg_rating", "number_rating", "created",
        ]


class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = '__all__'

