from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    data={"error": "Refresh token is required."},
                    status=400)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                data={"message": "Successfully logged out."},
                status=200)
        except Exception as e:
            return Response(
                data={"error": str(e)},
                status=400)
