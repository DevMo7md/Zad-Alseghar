from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ContactMessage, ViewLog
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff', 'is_superuser', 'password')
        read_only_fields = ('id', 'is_staff', 'is_superuser')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'
        read_only_fields = ('user', 'admin_reply', 'replied_at', 'created_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ViewLogSerializer(serializers.ModelSerializer):
    model_name = serializers.CharField(write_only=True)

    class Meta:
        model = ViewLog
        fields = ('id', 'model_name', 'object_id', 'timestamp')
        read_only_fields = ('timestamp',)

    def create(self, validated_data):
        model_name = validated_data.pop('model_name')
        try:
            # in future: search all installed apps or assume specific known apps?
            ct = ContentType.objects.get(model=model_name.lower())
        except ContentType.DoesNotExist:
            raise serializers.ValidationError({"model_name": "Invalid content type."})
        
        user = self.context['request'].user
        object_id = validated_data['object_id']
        
        view_log, created = ViewLog.objects.get_or_create(
            user=user,
            content_type=ct,
            object_id=object_id
        )
        return view_log

class DashboardStatsSerializer(serializers.Serializer):
    # Just a dummy serializer to document the response structure if needed, 
    # but the view will handle the logic.
    pass
