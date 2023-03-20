from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement,Favorites


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        is_POST_request = self.context['request']._stream.method == 'POST'
        number_of_publications_no_more_than_10 = len(Advertisement.objects.filter(creator=self.context["request"].user,status="OPEN")) >= 10
        if is_POST_request and number_of_publications_no_more_than_10:
            raise serializers.ValidationError('Достигнут максимальный лимит объявлений')
        # TODO: добавьте требуемую валидацию

        return data

class FavoritesSerializer(serializers.ModelSerializer):
    user = UserSerializer(
        read_only=True,
        
    )
    advertisement = AdvertisementSerializer(
        read_only=True,
    )
    class Meta:
        model = Favorites
        fields = ('id','user','advertisement')
    
    def create(self, validated_data):
        
        validated_data['user'] = self.context['request'].user
        validated_data['advertisement'] = Advertisement.objects.get(id=self.context['request']._data['advertisement'])
        
        return super().create(validated_data)
    
    def validate(self, data):
        user = self.context['request'].user
        try:
            advertisement = Advertisement.objects.get(id=self.context['request']._data['advertisement'])
        except:
            raise serializers.ValidationError('объявление не найдено')
        if user == advertisement.creator:
            raise serializers.ValidationError('Вы являетесь создателем объявления')
        if Favorites.objects.filter(user=user,advertisement=advertisement):
            raise serializers.ValidationError('объявление уже в избранном')
        return data