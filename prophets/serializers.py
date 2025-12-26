from rest_framework import serializers
from .models import Prophet, Video, Pdf



class VideoSerializer(serializers.ModelSerializer):
    prophet_id = serializers.PrimaryKeyRelatedField(queryset=Prophet.objects.all(), source='prophet', write_only=True)
    class Meta:
        model = Video
        fields = ['id', 'title', 'thumbnail', 'description', 'url', 'video', 'prophet_id', 'created_at', 'updated_at']
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


class PDFSerializer(serializers.ModelSerializer):
    prophet_id = serializers.PrimaryKeyRelatedField(queryset=Prophet.objects.all(), source='prophet', write_only=True)
    class Meta:
        model = Pdf
        fields = ['id', 'title', 'file', 'prophet_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ProphetSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)
    pdfs = PDFSerializer(many=True, read_only=True)
    class Meta:
        model = Prophet
        fields = ['id', 'name', 'age', 'info', 'videos', 'pdfs']
        read_only_fields = ['id']
