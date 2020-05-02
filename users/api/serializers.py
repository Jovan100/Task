from rest_framework.serializers import ModelSerializer
from users.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['pk', 'created_at', 'updated_at', 'last_login', 'is_staff', 'is_active', 'is_admin']

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        try:
            instance.set_password(validated_data['password'])
            instance.save()
        except:
            pass

        return instance
