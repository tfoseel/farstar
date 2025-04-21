from utils.skyfield import is_star_visible
from stars.models import Star as StarModel
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from posts.models import Post
from posts.serializers import PostCreateSerializer, PostSerializer


def clear_star_cache(star_id, lat, lon):
    rounded_lat = round(lat, 0)
    rounded_lon = round(lon, 0)
    cache_key = f"star_posts:{star_id}:lat:{rounded_lat}:lon:{rounded_lon}"
    cache.delete(cache_key)


class CheckVisibilityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        lat = request.data.get("latitude")
        lon = request.data.get("longitude")

        if lat is None or lon is None:
            return Response({"detail": "위치 정보(latitude, longitude)를 포함해주세요."}, status=400)

        post = get_object_or_404(Post.objects.select_related("star"), pk=pk)

        visible = is_star_visible(
            ra=post.star.ra,
            dec=post.star.dec,
            lat=float(lat),
            lon=float(lon)
        )

        if not visible:
            return Response({
                "is_visible": False,
                "detail": "현재 이 글은 볼 수 없습니다. 별이 하늘에 없습니다."
            }, status=403)

        return Response({
            "is_visible": True,
            "post": PostSerializer(post).data
        })


class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        lat = data.get("latitude")
        lon = data.get("longitude")
        star_id = data.get("star_id")

        if lat is None or lon is None or not star_id:
            return Response({"detail": "star_id, latitude, longitude를 모두 입력하세요."}, status=400)

        try:
            star = StarModel.objects.get(id=star_id)
        except StarModel.DoesNotExist:
            return Response({"detail": "해당 별을 찾을 수 없습니다."}, status=404)

        if not is_star_visible(star.ra, star.dec, float(lat), float(lon)):
            return Response({
                "detail": f"현재 위치에서는 {star.name} 별이 보이지 않아 글을 작성할 수 없습니다."
            }, status=403)

        serializer = PostCreateSerializer(
            data=data, context={"request": request})
        if serializer.is_valid():
            post = serializer.save()
            clear_star_cache(star_id, float(lat), float(lon))  # ✅ 캐시 무효화
            return Response(PostSerializer(post).data, status=201)
        return Response(serializer.errors, status=400)


class PostListView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-created_at')


class PostDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        lat = float(request.query_params.get("latitude", 37.0))  # fallback
        lon = float(request.query_params.get("longitude", 127.0))
        clear_star_cache(post.star.id, lat, lon)  # ✅ 캐시 무효화
        post.delete()
        return Response({"detail": "글이 삭제되었습니다."}, status=204)
