from django.urls import path
from .views import (
   view_blogs,
   create_blog,
   manage_blog,
   like_blog,
   upvote_blog,
   create_user,
   view_user,
   update_user,
   view_comments,
   manage_comment,

)


urlpatterns = [
   path('', view_blogs, name='view_blogs'),
   path('create_blog/', create_blog, name='create_blog'),
   path('<int:blog_id>/', manage_blog, name='manage_blog'),
   path('<int:blog_id>/like/', like_blog, name='like_blog'),
   path('<int:blog_id>/upvote/', upvote_blog, name='upvote_blog'),


   path('users', view_user, name='view_user'),
   path('signup', create_user, name='signup'),
   path('user/update/', update_user, name='update_user'),


   path('comments/', view_comments, name='view_comments'),
   path('<int:blog_id>/comments/', manage_comment, name='manage_comment'),
   path('<int:blog_id>/comments/<int:comment_id>/', manage_comment, name='manage_comment_detail'),
]
