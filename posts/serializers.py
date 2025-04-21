from rest_framework import serializers
from posts.models import Post
from stars.models import Star


class PostCreateSerializer(serializers.ModelSerializer):
    star_id = serializers.PrimaryKeyRelatedField(
        queryset=Star.objects.all(), source='star', write_only=True
    )

    class Meta:
        model = Post
        fields = ['star_id', 'content']

    def create(self, validated_data):
        user = self.context['request'].user
        return Post.objects.create(author=user, **validated_data)


class PostSerializer(serializers.ModelSerializer):
    star = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = ['id', 'star', 'content', 'created_at']


class PostWithVisibilitySerializer(serializers.ModelSerializer):
    star = serializers.StringRelatedField()
    is_visible = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'star', 'content', 'created_at', 'is_visible']

    def get_is_visible(self, obj):
        # Context에서 visibility map or 단일 값 꺼냄
        visible_map = self.context.get('visible_map')
        single_visibility = self.context.get('visible_for_star')

        if visible_map is not None:
            return visible_map.get(obj.id, False)
        if single_visibility is not None:
            return single_visibility
        return False  # 기본값

    def get_content(self, obj):
        visible = self.get_is_visible(obj)
        return obj.content if visible else None  # 또는 '🔒 볼 수 없습니다'
