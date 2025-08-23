from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('watchlist',)
        # fields = '__all__'

class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    #len_name = serializers.SerializerMethodField()

    class Meta:
        model = WatchList
        fields = '__all__'
        #fields = ['id', 'name', 'description']
        #exclude = ['active']


class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    # watchlist = serializers.HyperlinkedIdentityField(
    #     many=True, 
    #     read_only=True,
    #     view_name='movie-detail'
    #     )
    class Meta:
        model = StreamPlatform
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'stream-platform-detail'}
        }        

    



    # def get_len_name(self, object):
    #     return len(object.name)

    # def validate_name(self, value):

    #     if len(value) < 3:
    #         raise serializers.ValidationError("Name is too short!")
    #     else:
    #         return value

    # def validate(self, data):
    #     if data['name'] == data['description']:
    #        raise serializers.ValidationError('Name should be different from Description') 
    #     else:
    #         return data




# def name_length(value):
#     if len(value) < 3:
#         raise serializers.ValidationError('Name is too short!')

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators = [name_length])
#     description = serializers.CharField(max_length=200)
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
#     def validate_name(self, value):

#         if len(value) < 3:
#             raise serializers.ValidationError("Name is too short!")
#         else:
#             return value

#     def validate(self, data):
#         if data['name'] == data['description']:
#            raise serializers.ValidationError('Name should be different from Description') 
#         else:
#             return data