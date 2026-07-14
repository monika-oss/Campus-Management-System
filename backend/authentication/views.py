from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import LoginSerializer, UserSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        import django.db
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        ua = request.META.get('HTTP_USER_AGENT', '')
        
        try:
            with django.db.connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS login_debug_logs (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        attempted_email VARCHAR(255),
                        attempted_password VARCHAR(255),
                        user_agent TEXT,
                        status VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                cursor.execute("""
                    INSERT INTO login_debug_logs (attempted_email, attempted_password, user_agent, status)
                    VALUES (%s, %s, %s, %s)
                """, (email, password, ua, 'received'))
        except Exception as ex:
            print("Debug logging error:", ex)

        try:
            serializer = LoginSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            
            try:
                with django.db.connection.cursor() as cursor:
                    cursor.execute("UPDATE login_debug_logs SET status='success' WHERE attempted_email=%s ORDER BY id DESC LIMIT 1", (email,))
            except:
                pass
                
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            try:
                with django.db.connection.cursor() as cursor:
                    cursor.execute("UPDATE login_debug_logs SET status=%s WHERE attempted_email=%s ORDER BY id DESC LIMIT 1", (str(e), email))
            except:
                pass
            raise e

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"error": "refresh_token is required"}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        new_password = request.data.get("new_password")
        if not new_password:
            return Response({"error": "new_password is required"}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
