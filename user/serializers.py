from rest_framework import serializers
from .models import User,Verify,Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'nickname', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        try:
            verify = Verify.objects.get(email=validated_data['email'])
            if verify.verification:
                user = super().create(validated_data)
                password = user.password
                user.set_password(password)
                user.save()
                verify.delete()
                return user
            else:
                raise serializers.ValidationError('이메일 인증을 완료해야 사용자를 생성할 수 있습니다.', code='not_verify')
        except Verify.DoesNotExist:
            raise serializers.ValidationError('이메일 인증을 해주세요.', code='not_verify')
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'nickname', 'password')
        extra_kwargs = {'password': {'write_only': True}}
      
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('profileimage','introduction')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['nickname']=user.nickname
        return token


# 다른 유저에게 보이는 profile serializer입니다
class UserDetailSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    follower = serializers.SerializerMethodField()
    bookmark = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'nickname', 'following', 'follower','bookmark',] 


    # 프론트에서 구현할 수 있는 부분이라 일단 주석달아둡니다
    # def get_followers_count(self, obj):
    #     return obj.username.follower.count()

    # def get_following_count(self, obj):
    #     return obj.username.following.count()