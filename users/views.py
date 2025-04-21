from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer, ProfileSerializer
from posts.models import Post
from posts.serializers import PostWithVisibilitySerializer
from utils.skyfield import is_star_visible


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "회원가입 완료!",
                "user": {
                    "email": user.email,
                    "nickname": user.nickname,
                    "lumen": user.lumen
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = ProfileSerializer(
            request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyPostListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        lat = request.query_params.get("latitude")
        lon = request.query_params.get("longitude")

        if lat is None or lon is None:
            return Response({"detail": "위도(latitude), 경도(longitude)를 쿼리 파라미터로 전달하세요."}, status=400)

        posts = Post.objects.select_related("star").filter(author=request.user)

        # 각 글에 대해 visibility 판단
        visibility_map = {}
        for post in posts:
            visible = is_star_visible(
                post.star.ra, post.star.dec, float(lat), float(lon))
            visibility_map[post.id] = visible

        serializer = PostWithVisibilitySerializer(
            posts, many=True, context={'visible_map': visibility_map}
        )
        return Response(serializer.data)
