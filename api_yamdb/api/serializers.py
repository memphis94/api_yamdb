from rest_framework import serializers
from reviews.models import Comment, Review





class CommentSerializer(serializers.ModelSerializer):    
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review', )


class ReviewSerializer(serializers.ModelSerializer):    
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')