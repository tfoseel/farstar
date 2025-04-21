from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from stars.models import Star
from posts.models import Post
from posts.serializers import PostSerializer
from utils.skyfield import is_star_visible


class StarPostListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        lat = request.query_params.get("latitude")
        lon = request.query_params.get("longitude")

        if lat is None or lon is None:
            return Response({
                "detail": "위치 정보(latitude, longitude)를 쿼리 파라미터로 포함해주세요."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            star = Star.objects.get(pk=pk)
        except Star.DoesNotExist:
            return Response({"detail": "해당 별을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        visible = is_star_visible(
            ra=star.ra,
            dec=star.dec,
            lat=float(lat),
            lon=float(lon)
        )

        if not visible:
            return Response({
                "detail": f"현재 위치에서는 {star.name} 별이 하늘에 떠 있지 않아 게시물을 볼 수 없습니다.",
                "is_visible": False
            }, status=status.HTTP_403_FORBIDDEN)

        posts = Post.objects.filter(star=star).select_related("author")
        serializer = PostSerializer(posts, many=True)
        return Response({
            "is_visible": True,
            "posts": serializer.data
        })
