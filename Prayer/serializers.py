from rest_framework import serializers
from .models import Category, Video, Pdf


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'content']
        read_only_fields = ['id']

class VideoSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset = Category.objects.all(), source='category', write_only=True)
    class Meta:
        model = Video
        fields = ['id', 'title', 'thumbnail', 'video', 'url', 'category', 'category_id', 'description', 'order', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        url = data.get('url')
        video = data.get('video')

        if self.instance is None :
            if not url and not video :
                raise serializers.ValidationError("يجب رفع رابط او فيديو ع الاقل.")
            if url and video :
                raise serializers.ValidationError("لا يجوز رفع فيديو و رابط معا")
            

        else :
            if self.instance.url and video :
                raise serializers.ValidationError("يوجد رابط بالفعل لا يمكن رفع فيديو معه.")
            
            if self.instance.video and url :
                raise serializers.ValidationError("يوجد فيديو بالفعل لا يمكن رفع رابط معه.")
        
        return data


class PdfSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset = Category.objects.all(), source='category', write_only=True)
    class Meta:
        model = Pdf
        fields = ['id', 'title', 'file', 'category', 'category_id', 'created_at', 'updated_at', 'order']
        read_only_fields = ['id', 'created_at', 'updated_at']