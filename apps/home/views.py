# -*- encoding: utf-8 -*-
import math
from datetime import datetime
import os

from pathlib import Path
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.template import loader
from django import forms
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (ListView, DeleteView, UpdateView, CreateView, TemplateView, DetailView, View,
                                  FormView)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin

from .models import *
from .forms import *
from .calendar import PostCalendar, PostCalendarAdmin, PostCalendarAdminDetail
from .calendar_mini import PostCalendarMini, PostCalendarMiniAdmin
from .utils import get_chat_info, get_bot_info
from ..middleware import current_user


# ADMIN PAGE ########################################

class AdminPageView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    template_name = 'admin/admin_page.html'
    queryset = {}

    def get_context_data(self, **kwargs):
        context = super(AdminPageView, self).get_context_data(**kwargs)
        context.update({
            'users': User.objects.all(),
            'user_status': UserStatus.objects.all(),
            'cal_mini': PostCalendarMiniAdmin().formatmonth(theyear=int(datetime.now().year),
                                                            themonth=int(datetime.now().month)),
            'cal': PostCalendarAdmin().formatmonth(theyear=int(datetime.now().year),
                                                   themonth=int(datetime.now().month))
        })
        return context


class AdminPageUserUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = 'admin/user_update.html'
    model = User
    form_class = UserForm
    success_url = '/admin_page'
    success_message = 'Данные пользователя обновлены'

    def form_valid(self, form):
        return super().form_valid(form)


class AdminPageUserStatusUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = 'admin/user_status_update.html'
    model = UserStatus
    form_class = UserStatusForm
    success_url = '/admin_page'
    success_message = 'Данные пользователя обновлены'

    def form_valid(self, form):
        return super().form_valid(form)


class AdminPageUserDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = User
    success_url = '/admin_page'
    success_message = 'Пользователь удален'
    template_name = 'admin/user_delete.html'


class AdminPageUserDetailsView(SuccessMessageMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin/user_details.html'

    def get_context_data(self, **kwargs):
        context = super(AdminPageUserDetailsView, self).get_context_data(**kwargs)
        context.update({
            'users': User.objects.all(),
            'bots': Bot.objects.all(),
            'posts': Post.objects.all(),
            'chats': Chat.objects.all(),
            'cal_user': PostCalendarAdminDetail(user=int(self.request.path.split('/')[-1])).formatmonth(
                theyear=int(datetime.now().year),
                themonth=int(datetime.now().month))
        })
        return context


class AdminPagePostCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    form_class = PostAdminForm
    success_url = '/admin_page'
    success_message = 'Пост успешно создан!'
    template_name = 'crud/post_create.html'

    def form_valid(self, form):
        try:
            form.instance.text = str(form.instance.text).split('":"')[-1].replace('\\', '').replace('"}', '').replace(
                '</p>', '</p>\n')
        except IndexError:
            pass
        self.success_url = f'/admin_page/user_details/{form.instance.user.id}'
        return super().form_valid(form)


class AdminPagePostUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'crud/post_update.html'
    success_url = '/admin_page'
    success_message = 'Пост успешно обновлен!'

    def form_valid(self, form):
        try:
            form.instance.text = str(form.instance.text).split('":"')[-1].replace('\\', '').replace('"}', '').replace(
                '</p>', '</p>\n')
        except IndexError:
            pass
        self.success_url = f'/admin_page/user_details/{form.instance.user.id}'
        return super().form_valid(form)


class AdminPagePostDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/admin_page'
    template_name = 'crud/post_delete.html'


class AdminPageBotCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Bot
    form_class = BotAdminForm
    template_name = 'crud/bot_create.html'
    success_url = '/admin_page'
    success_message = 'Бот успешно создан!'

    def form_valid(self, form):
        # Парсим данные бота с помощью requests
        bot_data = get_bot_info(form.instance.ref)
        form.instance.title = bot_data
        self.success_url = f'/admin_page/user_details/{form.instance.user.id}'
        return super().form_valid(form)


class AdminPageBotUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Bot
    form_class = BotForm
    template_name = 'crud/bot_create.html'
    success_url = '/admin_page'
    success_message = 'Бот успешно обновлен'

    def form_valid(self, form):
        self.success_url = f'/admin_page/user_details/{form.instance.user.id}'
        return super().form_invalid(form)


class AdminPageBotDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Bot
    success_url = '/admin_page'
    template_name = 'crud/bot_delete.html'
    success_message = 'Бот успешно удалён'


class AdminPageChatCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Chat
    form_class = ChatAdminForm
    template_name = 'crud/chat_create.html'
    success_url = '/admin_page'
    success_message = 'Канал успешно добавлен!'

    def form_valid(self, form):
        # Парсим данные чата с помощью requests
        chat_data = get_chat_info(form.instance.ref)
        form.instance.subscribers = chat_data[2]
        form.instance.title = chat_data[1]
        form.instance.image = chat_data[0]
        self.success_url = f'/admin_page/user_details/{form.instance.user.id}'
        return super().form_valid(form)


class AdminPageChatUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Chat
    form_class = ChatAdminForm
    template_name = 'crud/chat_create.html'
    success_url = '/admin_page'
    success_message = 'Чат успешно обновлён'

    def form_valid(self, form):
        self.success_url = f'/admin_page/user_details/{form.instance.user.id}'
        return super().form_valid(form)


class AdminPageChatDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Chat
    success_url = '/admin_page'
    template_name = 'crud/chat_delete.html'
    success_message = 'Чат успешно удалён'


class ScheduleUpdateAdminView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = PostSchedule
    template_name = 'crud/calendar_event_create_admin.html'
    form_class = PostScheduleAdminForm
    success_url = f'/calendar_admin/{datetime.now().year}/{datetime.now().month}/'
    success_message = 'Расписание обновлено'

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        if form.cleaned_data['post'].user == form.cleaned_data['user']:
            form.instance.is_sent = False
            return super().form_valid(form)


class CalendarAdminView(LoginRequiredMixin, TemplateView):
    template_name = 'home/calendar.html'

    def get(self, request, year, month, *args, **kwargs):
        cal = PostCalendarAdmin().formatmonth(theyear=int(year), themonth=int(month))
        cal_mini = PostCalendarMiniAdmin().formatmonth(theyear=int(year), themonth=int(month))
        context = {'cal': cal, 'cal_mini': cal_mini, 'segment': 'calendar'}
        return render(request, 'home/calendar.html', context=context)

    def post(self, request, year, month, *args, **kwargs):
        cal = PostCalendarAdmin().formatmonth(theyear=int(year), themonth=int(month))
        cal_mini = PostCalendarMiniAdmin().formatmonth(theyear=int(year), themonth=int(month))
        context = {'cal': cal, 'cal_mini': cal_mini, 'segment': 'calendar'}
        return render(request, 'home/calendar.html', context=context)


class CalendarAdminEventCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = PostSchedule
    form_class = PostScheduleAdminForm
    template_name = 'crud/calendar_event_create_admin.html'
    success_url = f'/admin_page'
    success_message = 'Распиание обновлено'

    def get_context_data(self, **kwargs):
        context = super(CalendarAdminEventCreate, self).get_context_data(**kwargs)
        # context['name'] = self.request.GET.get('name')
        # context['sch'] = PostSchedule.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        # self.object = form.save(commit=False)
        # form.instance.user = self.request.user
        return super().form_valid(form)


class CalendarAdminUserEventCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = PostSchedule
    form_class = PostScheduleAdminUserForm
    template_name = 'crud/calendar_event_create_admin.html'
    success_message = 'Расписание обновлено'

    def get_success_url(self):
        return f'/admin_page/user_details/{self.object.user.id}'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(CalendarAdminUserEventCreate, self).get_form_kwargs()
        kwargs['initial']['post'] = self.request.GET['username']
        return kwargs

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     initial_data = {
    #         'post': Post.objects.filter(user=User.objects.filter(username=self.request.GET['username']).last()),
    #         }
    #     context['form'] = self.form_class(initial=initial_data)
    #     return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        form.instance.user = User.objects.filter(username=self.request.GET['username']).last()
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        # post = self.kwargs['post']
        # initial['po111st'] = Post.objects.filter(user=User.objects.filter(username=self.request.GET['username']).last())
        post_set = Post.objects.filter(user=User.objects.filter(username='administrator').last())
        initial['post'] = post_set
        return initial


# USER ##############################################


class UserUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = 'home/user_profile.html'
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    success_url = '/user_profile'
    extra_context = {'segment': 'user'}
    success_message = 'Профиль успешно обновлён'

    def user_profile(request):
        return redirect(f'/user_profile/{request.user.id}')


class ColorCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'crud/color_theme_update.html'
    model = UserStatus
    fields = ['primary_color']
    success_url = '/user_profile'
    extra_context = {'segment': 'user'}
    success_message = 'Профиль успешно обновлён'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ColorUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = 'crud/color_theme_update.html'
    model = UserStatus
    fields = ['primary_color']
    success_url = '/user_profile'
    extra_context = {'segment': 'user'}
    success_message = 'Профиль успешно обновлён'

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super().form_valid(form)


class LocationCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'crud/change_location.html'
    model = UserStatus
    fields = ['tz']
    success_url = '/'
    extra_context = {'segment': 'user'}
    success_message = 'Текущая локация успешно обновлёна'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class LocationUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = 'crud/change_location.html'
    model = UserStatus
    fields = ['tz']
    success_url = '/'
    extra_context = {'segment': 'user'}
    success_message = 'Текущая локация успешно обновлёна'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PaymentInfoTemplate(LoginRequiredMixin, TemplateView):
    template_name = 'home/payment_info.html'


# POST ##############################################


class PostListView(LoginRequiredMixin, ListView):
    extra_context = {'segment': 'post'}
    model = Post
    context_object_name = 'posts'
    template_name = 'home/post.html'

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context.update({
            'posts': Post.objects.filter(user=self.request.user),
            # 'photos': PostPhoto.objects.filter(post__user=self.request.user),
            # 'videos': PostVideo.objects.filter(post__user=self.request.user),
            # 'musics': PostMusic.objects.filter(post__user=self.request.user),
            # 'documents': PostDocument.objects.filter(post__user=self.request.user),
            # 'buttons': Button.objects.filter(post__user=self.request.user),
            # 'references': PostReference.objects.filter(post__user=self.request.user),
            'cal_mini': PostCalendarMini().formatmonth(theyear=int(datetime.now().year),
                                                       themonth=int(datetime.now().month)),
        })
        return context


class PostDetailsView(LoginRequiredMixin, DetailView):
    model = Post

    context_object_name = 'post'
    template_name = 'home/post_details.html'

    # def get_queryset(self, pk):
    #     return Post.objects.get(id=pk)
    #
    def get_context_data(self, **kwargs):
        context = super(PostDetailsView, self).get_context_data(**kwargs)
        context.update({
            'photos': PostPhoto.objects.filter(post__user=self.request.user),
            'videos': PostVideo.objects.filter(post__user=self.request.user),
            'musics': PostMusic.objects.filter(post__user=self.request.user),
            'documents': PostDocument.objects.filter(post__user=self.request.user),
            'buttons': Button.objects.filter(post__user=self.request.user),
            'references': PostReference.objects.filter(post__user=self.request.user),
            'templates': Template.objects.filter(post__user=self.request.user),
        })
        return context


class PostCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    form_class = PostForm
    success_url = 'post'
    success_message = 'Пост успешно создан!'
    template_name = 'crud/post_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            form.instance.text = str(form.instance.text).split('":"')[-1].replace('\\', '').replace('"}', '').replace(
                '</p>', '</p>\n')
        except IndexError:
            pass
        return super().form_valid(form)


class PostUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'crud/post_update.html'
    success_url = '/post'
    success_message = 'Пост успешно обновлен!'

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            form.instance.text = str(form.instance.text).split('":"')[-1].replace('\\', '').replace('"}', '').replace(
                '</p>', '</p>\n')
        except IndexError:
            pass
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/post'
    template_name = 'crud/post_delete.html'


class PostPhotoUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = PostPhoto
    # form_class = PostPhotoForm
    template_name = 'crud/post_photo_update.html'
    success_url = '/post'
    success_message = 'Фото успешно обновлено'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostPhotoDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = PostPhoto
    success_url = '/post'
    template_name = 'crud/post_photo_delete.html'
    success_message = 'Фото успешно удалено'


class PostVideoUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = PostVideo
    form_class = PostVideoForm
    template_name = 'crud/post_video_update.html'
    success_url = '/post'
    success_message = 'Видео успешно обновлено'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostVideoDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = PostVideo
    success_url = '/post'
    template_name = 'crud/post_video_delete.html'


class PostMusicUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = PostMusic
    form_class = PostMusicForm
    template_name = 'crud/post_music_update.html'
    success_url = '/post'
    success_message = 'Трек успешно обновлен'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostMusicDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = PostMusic
    success_url = '/post'
    template_name = 'crud/post_music_delete.html'


class PostDocumentUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = PostDocument
    form_class = PostDocumentForm
    template_name = 'crud/post_document_update.html'
    success_url = '/post'
    success_message = 'Документ успешно обновлен'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostDocumentDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = PostDocument
    success_url = '/post'
    template_name = 'crud/post_document_delete.html'


# TEMPLATE ###############################################


class TemplateListView(LoginRequiredMixin, ListView):
    model = Template
    context_object_name = 'templates'
    success_url = '/template'
    template_name = 'home/template.html'

    def get_queryset(self):
        return Template.objects.filter(user=self.request.user)


class TemplateCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Template
    form_class = TemplateForm
    template_name = 'crud/template_create.html'
    success_url = '/template'
    success_message = 'Шаблон создан успешно!'

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            form.instance.text = str(form.instance.text).split('":"')[-1].replace('\\', '').replace('"}', '').replace(
                '</p>', '</p>\n')
        except IndexError:
            pass
        return super().form_valid(form)


class TemplateUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Template
    form_class = TemplateForm
    template_name = 'crud/template_create.html'
    success_url = '/template'
    success_message = 'Шаблон обновлён успешно!'

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            form.instance.text = str(form.instance.text).split('":"')[-1].replace('\\', '').replace('"}', '').replace(
                '</p>', '</p>\n')
        except IndexError:
            pass
        return super().form_valid(form)


class TemplateDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Template
    form_class = TemplateForm
    template_name = 'crud/template_delete.html'
    success_url = '/template'
    success_message = 'Шаблон успешно удалён!'


# BOT ###############################################


class BotListView(LoginRequiredMixin, ListView):
    extra_context = {'segment': 'bot'}
    model = Bot
    context_object_name = 'bots'
    template_name = 'home/bot.html'

    def get_queryset(self):
        return Bot.objects.filter(user=self.request.user)


class BotCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Bot
    form_class = BotForm
    template_name = 'crud/bot_create.html'
    success_url = 'bot'
    success_message = '''Вы успешно добавили бота, который будет постить ваши посты.<br/>
            Теперь добавьте канал или чат,
            если у вас нет канала то создайте его и 
            <a class="btn btn-link" href="/chat_create">добавьте канал в наше приложение</a><br/>
            Далее в разделе с каналами: выберете бота который будет постить в данный канал или группу
        '''

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Парсим данные бота с помощью requests
        bot_data = get_bot_info(form.instance.ref)
        form.instance.title = bot_data
        return super().form_valid(form)


class BotUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Bot
    form_class = BotForm
    template_name = 'crud/bot_create.html'
    success_url = '/bot'
    success_message = 'Бот успешно обновлен'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BotDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Bot
    success_url = '/bot'
    template_name = 'crud/bot_delete.html'
    success_message = 'Бот успешно удалён'


# CHANNEL ###############################################

class ChatListView(LoginRequiredMixin, ListView):
    extra_context = {'segment': 'chat'}
    model = Chat
    context_object_name = 'chats'
    template_name = 'home/chat.html'

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user)


class ChatCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Chat
    form_class = ChatForm
    template_name = 'crud/chat_create.html'
    success_url = '/chat'
    success_message = 'Канал успешно добавлен. Не забудьте добавить вашего бота в администраторы канала!'

    def form_valid(self, form):
        form.instance.user = self.request.user

        # Парсим данные чата с помощью requests
        chat_data = get_chat_info(form.instance.ref)
        form.instance.subscribers = chat_data[2]
        form.instance.title = chat_data[1]
        form.instance.image = chat_data[0]
        return super().form_valid(form)


class ChatUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Chat
    form_class = ChatForm
    template_name = 'crud/chat_create.html'
    success_url = '/chat'
    success_message = 'Чат успешно обновлён'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ChatDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Chat
    success_url = '/chat'
    template_name = 'crud/chat_delete.html'
    success_message = 'Чат успешно удалён'


# CALENDAR ###############################################

class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'crud/calendar.html'

    def get(self, request, year, month, *args, **kwargs):
        cal = PostCalendar().formatmonth(theyear=int(year), themonth=int(month))
        cal_mini = PostCalendarMini().formatmonth(theyear=int(year), themonth=int(month))
        context = {'cal': cal, 'cal_mini': cal_mini, 'segment': 'calendar'}
        return render(request, 'home/calendar.html', context=context)

    def post(self, request, year, month, *args, **kwargs):
        cal = PostCalendar().formatmonth(theyear=int(year), themonth=int(month))
        cal_mini = PostCalendarMini().formatmonth(theyear=int(year), themonth=int(month))
        context = {'cal': cal, 'cal_mini': cal_mini, 'segment': 'calendar'}
        return render(request, 'home/calendar.html', context=context)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def calendar_event(request, year, month, day):
    post = Post.objects.filter(user=request.user).last()
    form = PostScheduleForm(request.POST, instance=post)
    if form.is_valid():
        # print(form)
        form.save()
        messages.success(request, "Успешно обновлено")
        # return redirect(f"/calendar/{datetime.now().year}/{datetime.now().month}/")
    return render(request, 'home/calendar_event.html', context={
        'posts': post,
        'year': year,
        'month': month,
        'day': day
    })


def calendar_event(request, year, month, day):
    post = Post.objects.filter(user=request.user).last()
    form = PostScheduleForm(request.POST, instance=post)
    if form.is_valid():
        # print(form)
        form.save()
        messages.success(request, "Успешно обновлено")
        # return redirect(f"/calendar/{datetime.now().year}/{datetime.now().month}/")
    return render(request, 'home/calendar_event.html', context={
        'posts': post,
        'year': year,
        'month': month,
        'day': day
    })


class CalendarEventCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = PostSchedule
    form_class = PostScheduleForm
    template_name = 'crud/calendar_event_create.html'
    success_url = f'/calendar/{datetime.now().year}/{datetime.now().month}/'
    success_message = 'Распиание обновлено'

    def get_context_data(self, **kwargs):
        context = super(CalendarEventCreate, self).get_context_data(**kwargs)
        context['name'] = self.request.GET.get('name')
        context['sch'] = PostSchedule.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        form.instance.user = self.request.user
        return super().form_valid(form)


class CalendarEventMultipleCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = PostSchedule
    form_class = PostScheduleMultipleForm
    template_name = 'crud/calendar_event_create.html'
    # success_url = f'/calendar/{datetime.now().year}/{datetime.now().month}/'
    success_url = f'/post'
    success_message = 'Распиание обновлено'

    def get_context_data(self, **kwargs):
        context = super(CalendarEventMultipleCreate, self).get_context_data(**kwargs)
        context['name'] = self.request.GET.get('name')
        context['sch'] = PostSchedule.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        posts = form.cleaned_data['post']
        for post in posts:
            self.request.datasession['post'] = post.id
            form.save()
        return super().form_valid(form)


class ScheduleUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = PostSchedule
    template_name = 'crud/schedule_update.html'
    form_class = PostScheduleForm
    success_url = f'/calendar/{datetime.now().year}/{datetime.now().month}/'
    success_message = 'Расписание обновлено'

    def form_valid(self, form):
        form.instance.is_sent = False
        return super().form_valid(form)


class ScheduleDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = PostSchedule
    success_url = f'/calendar/{datetime.now().year}/{datetime.now().month}/'
    template_name = 'crud/schedule_delete.html'
    success_message = 'Пост удален из расписания'


@login_required(login_url="/login/")
def index(request):
    subs = 0
    chats = Chat.objects.filter(user=request.user)
    for chat in chats:
        subs += chat.subscribers
    if subs > 10000:
        subs = math.floor(subs / 1000)
        subs = '+' + str(subs) + 'k'

    all_users = len(User.objects.all())
    try:
        user_stats = UserStats.objects.filter(user=request.user)[0]
        user_status = UserStatus.objects.filter(user=request.user)[0]
    except:
        user_stats = {}
        user_status = {}
    context = {
        'segment': 'index',
        'year': datetime.now().year,
        'month': datetime.now().month,
        'subs': subs,
        'all_users': all_users,
        'bots': Bot.objects.filter(user=request.user),
        'posts': Post.objects.filter(user=request.user),
        'chats': Chat.objects.filter(user=request.user),
        'user_stats': user_stats,
        'user_status': user_status,
        'sch': PostSchedule.objects.filter(user=request.user),
        'cal': PostCalendar().formatmonth(theyear=int(datetime.now().year), themonth=int(datetime.now().month)),
    }
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

# def page_not_found_view(request, exception):
#     return render(request, 'home/page-404.html', status=404)
