from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, Blog, Comment
from .serializers import CustomUserSerializer, BlogSerializer, CommentSerializer


@api_view(['GET'])
def view_blogs(request):
    blogs = Blog.objects.all()
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_blog(request):
    if request.method == 'POST':
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
@api_view(['POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_blog(request, blog_id=None):
    if request.method == 'PUT' or request.method == 'PATCH':
        try:
            blog = Blog.objects.get(pk=blog_id)
        except Blog.DoesNotExist:
            return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is the author of the blog
        if request.user not in blog.authors.all():
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == 'PUT' or request.method == 'PATCH':
            serializer = BlogSerializer(blog, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            blog = Blog.objects.get(pk=blog_id)
        except Blog.DoesNotExist:
            return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

        blog.delete()
        return Response({"message": "Blog deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_blog(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

    blog.like_count += 1
    blog.save()
    return Response({"message": "Blog liked successfully"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upvote_blog(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

    blog.upvote_count += 1
    blog.save()
    return Response({"message": "Blog upvoted successfully"})


@api_view(['GET'])
@permission_classes([AllowAny])
def view_user(request):
    users = CustomUser.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    serializer = CustomUserSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    serializer = CustomUserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_comments(request):
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_comment(request, blog_id, comment_id=None):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            blog.comments.add(serializer.instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if the user is the author of the comment
    if request.user != comment.user:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method in ['PUT', 'PATCH']:
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'DELETE':
        comment.delete()
        return Response({"message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
