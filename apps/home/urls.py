# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from django.views.static import serve

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('', views.index, name='home'),

    path('admin_page', views.AdminPageView.as_view(), name='admin page'),
    path('admin_page/user_update/<int:pk>', views.AdminPageUserUpdateView.as_view(), name='admin user update'),
    path('admin_page/user_details/<int:pk>', views.AdminPageUserDetailsView.as_view(), name='admin user details'),
    path('admin_page/user_status_update/<int:pk>', views.AdminPageUserStatusUpdateView.as_view(),
         name='admin user status update'),
    path('admin_page/user_delete/<int:pk>', views.AdminPageUserDeleteView.as_view(), name='admin user delete'),

    path('admin_page/post_create', views.AdminPagePostCreateView.as_view(), name='admin create post'),
    path('admin_page/post_update/<int:pk>', views.AdminPagePostUpdateView.as_view(), name='admin update post'),
    path('admin_page/post_delete/<int:pk>', views.AdminPagePostDeleteView.as_view(), name='admin delete post'),

    path('admin_page/bot_create', views.AdminPageBotCreateView.as_view(), name='admin create bot'),
    path('admin_page/bot_update/<int:pk>', views.AdminPageBotUpdateView.as_view(), name='admin update bot'),
    path('admin_page/bot_delete/<int:pk>', views.AdminPageBotDeleteView.as_view(), name='admin delete bot'),

    path('admin_page/chat_create', views.AdminPageChatCreateView.as_view(), name='admin create chat'),
    path('admin_page/chat_update/<int:pk>', views.AdminPageChatUpdateView.as_view(), name='admin update chat'),
    path('admin_page/chat_delete/<int:pk>', views.AdminPageChatDeleteView.as_view(), name='admin delete chat'),

    path('user_profile', views.UserUpdateView.user_profile, name='user profile fast kostyl'),
    path('user_profile/<int:pk>', views.UserUpdateView.as_view(), name='user profile'),
    path('color_theme_create', views.ColorCreateView.as_view(), name='color create'),
    path('color_theme_update/<int:pk>', views.ColorUpdateView.as_view(), name='color update'),
    path('create_location', views.LocationCreateView.as_view(), name='location create'),
    path('change_location/<int:pk>', views.LocationUpdateView.as_view(), name='location update'),
    path('payment_info', views.PaymentInfoTemplate.as_view(), name='payment info'),

    path('post', views.PostListView.as_view(), name='posts'),
    path('post_details/<int:pk>', views.PostDetailsView.as_view(), name='post details'),

    path('post_create', views.PostCreateView.as_view(), name='create post'),
    path('post_update/<int:pk>', views.PostUpdateView.as_view(), name='update post'),
    path('post_delete/<int:pk>', views.PostDeleteView.as_view(), name='delete post'),

    path('post_photo_update/<int:pk>', views.PostPhotoUpdateView.as_view(), name='post photo update'),
    path('post_photo_delete/<int:pk>', views.PostPhotoDeleteView.as_view(), name='post photo update'),

    path('post_video_update/<int:pk>', views.PostVideoUpdateView.as_view(), name='post video update'),
    path('post_video_delete/<int:pk>', views.PostVideoDeleteView.as_view(), name='post video delete'),

    path('post_music_update/<int:pk>', views.PostMusicUpdateView.as_view(), name='post music update'),
    path('post_music_delete/<int:pk>', views.PostMusicDeleteView.as_view(), name='post music delete'),

    path('post_documet_update/<int:pk>', views.PostDocumentUpdateView.as_view(), name='post document update'),
    path('post_documet_delete/<int:pk>', views.PostDocumentDeleteView.as_view(), name='post document delete'),

    path('template', views.TemplateListView.as_view(), name='template'),
    path('template_create', views.TemplateCreateView.as_view(), name='create template'),
    path('template_update/<int:pk>', views.TemplateUpdateView.as_view(), name='update template'),
    path('template_delete/<int:pk>', views.TemplateDeleteView.as_view(), name='delete template'),

    path('bot', views.BotListView.as_view(), name='bot'),
    path('bot_create', views.BotCreateView.as_view(), name='create bot'),
    path('bot_update/<int:pk>', views.BotUpdateView.as_view(), name='update bot'),
    path('bot_delete/<int:pk>', views.BotDeleteView.as_view(), name='delete bot'),

    path('chat', views.ChatListView.as_view(), name='chat'),
    path('chat_create', views.ChatCreateView.as_view(), name='create chat'),
    path('chat_update/<int:pk>', views.ChatUpdateView.as_view(), name='update chat'),
    path('chat_delete/<int:pk>', views.ChatDeleteView.as_view(), name='delete chat'),

    path('calendar/<int:year>/<int:month>/', views.CalendarView.as_view(), name='calendar'),
    path('calendar_event_create/<int:year>/<int:month>/<int:day>/', views.CalendarEventCreate.as_view(), name='calendar event create'),
    path('calendar_event_create_multiple/<int:year>/<int:month>/<int:day>/', views.CalendarEventMultipleCreate.as_view(), name='calendar event create multiple'),

    path('schedule_update/<int:pk>', views.ScheduleUpdateView.as_view(), name='update schedule'),
    path('schedule_delete/<int:pk>', views.ScheduleDeleteView.as_view(), name='delete schedule'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# handler404 = "apps.home.views.page_not_found_view"
