from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Notification, NotificationRead
from .serializers import NotificationSerializer, NotificationCreateUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsAdmin, IsOwnerOrAdmin

class NotificationViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['target_role', 'is_active']
    search_fields = ['title', 'description']

    def get_queryset(self):
        from django.db.models import Q
        user = self.request.user
        
        if user.role == 'admin':
            queryset = Notification.objects.all().order_by('-created_at')
        else:
            queryset = Notification.objects.filter(is_active=True).order_by('-created_at')
            queryset = queryset.filter(
                Q(target_role='all') | 
                Q(target_role=user.role, target_user__isnull=True) |
                Q(target_user=user)
            )
            
        # Exclude deleted notifications
        from .models import NotificationDeleted
        deleted_ids = NotificationDeleted.objects.filter(user=user).values_list('notification_id', flat=True)
        queryset = queryset.exclude(notification_id__in=deleted_ids)
            
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return NotificationCreateUpdateSerializer
        return NotificationSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def read(self, request, pk=None):
        notification = self.get_object()
        NotificationRead.objects.get_or_create(
            notification=notification,
            user=request.user
        )
        return Response({'message': 'Notification marked as read.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def unread(self, request):
        queryset = self.get_queryset()
        read_notification_ids = NotificationRead.objects.filter(user=request.user).values_list('notification_id', flat=True)
        unread_notifications = queryset.exclude(notification_id__in=read_notification_ids)
        
        serializer = self.get_serializer(unread_notifications, many=True)
        return Response({
            'count': unread_notifications.count(),
            'notifications': serializer.data
        })

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        queryset = self.get_queryset()
        read_notification_ids = NotificationRead.objects.filter(user=request.user).values_list('notification_id', flat=True)
        unread_notifications = queryset.exclude(notification_id__in=read_notification_ids)
        
        read_objects = [
            NotificationRead(notification=notif, user=request.user)
            for notif in unread_notifications
        ]
        NotificationRead.objects.bulk_create(read_objects, ignore_conflicts=True)
        
        return Response({'message': 'All notifications marked as read.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def hide(self, request, pk=None):
        """Hides a single notification for the user."""
        notification = self.get_object()
        from .models import NotificationDeleted
        NotificationDeleted.objects.get_or_create(
            notification=notification,
            user=request.user
        )
        return Response({'message': 'Notification deleted.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def delete_all(self, request):
        """Hides all current notifications for the user."""
        queryset = self.get_queryset()
        from .models import NotificationDeleted
        
        deleted_objects = [
            NotificationDeleted(notification=notif, user=request.user)
            for notif in queryset
        ]
        NotificationDeleted.objects.bulk_create(deleted_objects, ignore_conflicts=True)
        
        return Response({'message': 'All notifications deleted.'}, status=status.HTTP_200_OK)
