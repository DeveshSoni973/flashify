from rest_framework import serializers
from .models import Flashcard

# Flashcard List Serializer (For displaying a list of cards)
class FlashCardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = ['id', 'question', 'answer']

# Flashcard Detail Serializer (For displaying a single card's details)
class FlashCardDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = ['id', 'question', 'answer', 'created_at', 'updated_at']

# Flashcard Creation Serializer (For creating new flashcards)
class FlashCardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = ['id', 'question', 'answer']  # Removed user field since we get it from request

    def create(self, validated_data):
        user = self.context['request'].user  # Automatically get the user from the request context
        validated_data['user'] = user  # Attach the user to the flashcard
        return super().create(validated_data)
