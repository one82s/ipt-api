import bcrypt
import django_filters.rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .models import User, Post, Comment, PasswordSingleton, PasswordClass, PasswordFactory
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from django.contrib.auth.hashers import make_password, check_password 
from django.core.cache import cache

class UserListCreate(APIView):
     
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        # Week 5 demo
        # Singleton usage
        passwordSingleton1 = PasswordSingleton("mypassword123")
        passwordSingleton2 = PasswordSingleton("mypassword1234")
        print('First singleton password is: ', passwordSingleton1.password)
        print('Second singleton password is: ', passwordSingleton2.password)
        print('Are they the same? ', passwordSingleton1 is passwordSingleton1) 
        # Explanation:
        # passwordSingleton1 and passwordSingleton2 are both created using the PasswordSingleton class.
        # Even though different arguments are passed, both variables will point to the same instance because of the Singleton pattern.
        # print(passwordSingleton1.password): Outputs "mypassword123" because that was the argument passed during the first instance creation.
        # print(passwordSingleton2.password): Outputs "mypassword123" because it will always be the same instance, and the message will be the one provided when the first instance is created.

        #Factory pattern usage
        factory = PasswordFactory()
        factory.register_class('password', PasswordClass)

        firstPassword = factory.create_instance('password', 'mypassword123')
        secondPassword = factory.create_instance('password', 'mypassword123456')
        print('First password from factory is: ', firstPassword.password)
        print('Second password from factory is: ', secondPassword.password)
        print('Are they the same? ', firstPassword is secondPassword)
        # Explanation:
        # An instance of PasswordFactory is created.
        # The PasswordClass class is registered with the factory using the key "password".
        # Instances are created using the create_instance method of the factory, each with different messages.
        # print('First password from factory is: ', firstPassword.password): Outputs "mypassword123".
        # print('Second password from factory is: ', secondPassword.password): Outputs "mypassword123456".
        # print('Are they the same? ', firstPassword is secondPassword): Outputs False, indicating firstPassword and secondPassword are different instances.



        
        hashed_password = make_password("mypassword123")
        # print(hashed_password)  # Outputs a hashed version of the password

       
        # Verifying the hashed password
        isPasswordValid = check_password("mypassword123", hashed_password)
        # print('Is the password valid? ', isPasswordValid)  # Outputs True if the password matches

        #Salting
        password = b'password1234'
        salt = bcrypt.gensalt()
        #hashWithSaltPassword = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        hashWithSaltPassword = bcrypt.hashpw(password, salt)
        # print('Hash with salt password is: ', hashWithSaltPassword)
        # Verify a password
        passwordToVerify = b'password1234'

        # if bcrypt.checkpw(passwordToVerify, hashWithSaltPassword):
        #    print("Password is correct")
        # else:
        #    print("Invalid password")

        return Response(serializer.data)


    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    cache.set('posts', queryset)
    if cache.get('posts'):
        print('Posts are cached')
    else:
        print('Posts are not cached')
    serializer_class = PostSerializer
    permission_classes = ([IsAuthenticatedOrReadOnly])
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['id','content']
    search_fields = ['id','content']
    ordering_fields = ['id','content', 'created_at']
    cache.delete('posts')
    print('Check if posts are still cached after deletion: ', cache.get('posts'))


class CommentListCreate(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
