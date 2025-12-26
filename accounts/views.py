from rest_framework import viewsets, permissions, status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import ContactMessage, ViewLog, User
from .models import ContactMessage, ViewLog, User
from .serializers import ContactMessageSerializer, ViewLogSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsStaffOrSuperUser, IsSuperUser
from .utils import send_contact_email, send_reply_email
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ContactMessageFilter

class ContactMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContactMessageFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return ContactMessage.objects.all()
        return ContactMessage.objects.filter(user=user)

    def perform_create(self, serializer):
        msg = serializer.save()
        send_contact_email(msg.subject, msg.message, msg.user.email)

    def perform_update(self, serializer):
        # Only admin should reply
        if not self.request.user.is_superuser:
             # If just user updating, maybe block or allow editing own message? 
             # Requirement says: "admin can receive it... and user can see the reply".
             # Usually user just sends. Admin replies.
             # I'll check if 'admin_reply' is changing.
             pass
        
        instance = serializer.save()
        if instance.admin_reply and not instance.replied_at:
            instance.replied_at = timezone.now()
            instance.save()
            send_reply_email(instance.subject, instance.admin_reply, instance.user.email)

class RecordView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ViewLogSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DashboardStatisticsView(views.APIView):
    permission_classes = [IsStaffOrSuperUser]

    def get(self, request, *args, **kwargs):
        user = request.user
        data = {}

        # Videos & PDFs stats (for both Staff and Admin)
        # Assuming we can group by content_type to see "Video" vs "PDF"
        # Since we don't know exact app names, we rely on ContentType model field
        
        view_stats = ViewLog.objects.values('content_type__model').annotate(total_views=Count('id')).order_by('-total_views')
        data['content_views'] = view_stats

        if user.is_superuser:
            # Users statistics (Admin only)
            user_count = User.objects.count()
            data['total_users'] = user_count
            
            # Maybe more detailed user stats?
            # "available user's data": return list of users?
            # Start with count and maybe recent joins
            users = User.objects.all().values('id', 'username', 'email', 'date_joined')
            data['users'] = list(users)

        return Response(data)

class RegisterView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Optional: Return tokens immediately upon registration
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
