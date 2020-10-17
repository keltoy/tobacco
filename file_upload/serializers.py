from rest_framework import serializers
from file_upload.models import RelevantDocument, Presentation


class RelevantDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelevantDocument
        fields = '__all__'


class PresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presentation
        fields = '__all__'
