from datetime import datetime
from urllib.request import urlopen

import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView)
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from apps.spamer.models import (Account, Message, Client, AccountLogging, GeneralSettings, Chat, ChannelToSubscribe)
from apps.spamer.forms import (AccountForm, ChatUploadForm, AccountUploadForm, ChatForm, ChannelToSubscribeForm)
from apps.middleware.current_user import get_current_user
from apps.home.utils import get_chat_info


class BaseSpamerView(LoginRequiredMixin, TemplateView):
    template_name = "spamer/home/index.html"

    def get_context_data(self, **kwargs):
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        context = super(BaseSpamerView, self).get_context_data(**kwargs)
        context.update({'segment': 'spm',
                        'len_account': Account.objects.all().count(),
                        'len_account_active': Account.objects.filter(status=True).count(),
                        'len_chat': Chat.objects.all().count(),
                        'len_chat_active': Chat.objects.filter(is_active=True).count(),
                        'len_message': Message.objects.all().count(),
                        'len_message_day': Message.objects.filter(datetime__gte=today_start,
                                                                  datetime__lte=today_end).count(),
                        'len_autoanswer': Client.objects.all().count(),
                        })
        return context


class AccountListView(LoginRequiredMixin, ListView):
    model = Account
    context_object_name = 'accounts'
    template_name = 'spamer/home/account.html'

    def get_context_data(self, **kwargs):
        context = super(AccountListView, self).get_context_data(**kwargs)
        context.update({'segment': 'spm', 'spm_segment': 'account'})
        return context


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account
    context_object_name = 'account'
    template_name = 'spamer/home/account_details.html'

    def get_context_data(self, **kwargs):
        context = super(AccountDetailView, self).get_context_data(**kwargs)
        context.update({'segment': 'spm', 'spm_segment': 'account'})
        return context


class AccountCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    form_class = AccountForm
    success_url = '/spm/accs'
    template_name = 'spamer/crud/create.html'
    success_message = 'Аккаунт успешно добавлен!'

    def get_context_data(self, **kwargs):
        context = super(AccountCreateView, self).get_context_data(**kwargs)
        context.update({'segment': 'spm', 'spm_segment': 'account'})
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AccountUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'spamer/crud/create.html'
    success_url = '/spm/accs'
    success_message = 'Аккаунт успешно обновлен!'

    def get_context_data(self, **kwargs):
        context = super(AccountUpdateView, self).get_context_data(**kwargs)
        context.update({'segment': 'spm', 'spm_segment': 'account'})
        return context

    def form_valid(self, form):
        form.instance.is_change_needed = True
        form.instance.user = self.request.user
        return super().form_valid(form)


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = Account
    success_url = '/spm/accs'
    template_name = 'spamer/crud/delete.html'

    def get_context_data(self, **kwargs):
        context = super(AccountDeleteView, self).get_context_data(**kwargs)
        context.update({'segment': 'spm', 'spm_segment': 'account'})
        return context

    @staticmethod
    def delete_view(request, id):
        obj = Account.objects.get(id=id)
        obj.delete()
        return HttpResponseRedirect("/spm/accs")


class AccountUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Account
    form_class = AccountUploadForm
    success_url = '/spm/accs'
    template_name = 'spamer/crud/create.html'

    def get_context_data(self, **kwargs):
        context = super(AccountUploadView, self).get_context_data(**kwargs)
        context.update({'segment': 'spm', 'spm_segment': 'account'})
        return context

    def form_valid(self, form):
        GeneralSettings.objects.filter(id=1).update(is_reload_spam_needed=True)
        form.instance.user = self.request.user
        return super().form_valid(form)


class ChatListView(LoginRequiredMixin, ListView):
    model = Chat
    context_object_name = 'chats'
    template_name = 'spamer/home/chat.html'

    def get_context_data(self, **kwargs):
        context = super(ChatListView, self).get_context_data(**kwargs)
        context.update({'segment': 'spm', 'spm_segment': 'chat'})
        return context


class ChatDetailView(LoginRequiredMixin, DetailView):
    model = Chat
    context_object_name = 'chat'
    template_name = 'spamer/home/chat_details.html'

    def get_context_data(self, **kwargs):
        context = super(ChatDetailView, self).get_context_data(**kwargs)
        context.update({'segment': 'spm', 'spm_segment': 'chat'})
        return context


class ChatCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    form_class = ChatForm
    success_url = '/spm/chat'
    template_name = 'spamer/crud/create.html'
    success_message = 'Чат успешно создан!'

    def get_context_data(self, **kwargs):
        context = super(ChatCreateView, self).get_context_data(**kwargs)
        context.update({'segment': 'spm', 'spm_segment': 'chat'})
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

        # Парсим данные чата с помощью requests

        # chat_data = get_chat_info(form.instance.link)
        # form.instance.title = chat_data[1]
        # if 'data:image' in chat_data[0]:
        #     form.instance.image = chat_data[0]
        # else:
        #     form.instance.data_image = chat_data[0]
        # return super().form_valid(form)

        # Парсим данные чата с помощью requests
        # chat_data = get_chat_info(form.instance.ref)
        # form.instance.subscribers = chat_data[2]
        # form.instance.title = chat_data[1]
        # form.instance.image = chat_data[0]
        # return super().form_valid(form)


class ChatUploadView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    form_class = ChatUploadForm
    success_url = '/spm/chat'
    template_name = 'spamer/crud/create.html'
    success_message = 'Чат успешно создан!'

    def get_context_data(self, **kwargs):
        context = super(ChatUploadView, self).get_context_data(**kwargs)
        context.update({'segment': 'spm', 'spm_segment': 'chat'})
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Парсим данные чата с помощью requests

        chat_data = get_chat_info(form.instance.link)
        form.instance.title = chat_data[1]
        form.instance.subscribers = chat_data[2]
        form.instance.username = str(form.instance.link).split('/')[-1]

        if 'data:image' in chat_data[0]:
            form.instance.data_image = chat_data[0]
        else:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(chat_data[0]).read())
            img_temp.flush()
            form.instance.image = File(img_temp, name=f'chat_{str(datetime.now())}.jpg')

        return super().form_valid(form)


class ChatUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Chat
    form_class = ChatForm
    template_name = 'spamer/crud/create.html'
    success_url = '/spm/chat'
    success_message = 'Чат успешно обновлен!'

    def get_context_data(self, **kwargs):
        context = super(ChatUpdateView, self).get_context_data(**kwargs)
        context.update({'segment': 'spm', 'spm_segment': 'chat'})
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ChatDeleteView(LoginRequiredMixin, DeleteView):
    model = Chat
    success_url = '/spm/chat'
    template_name = 'spamer/crud/delete.html'
    success_message = 'Чат успешно удалён!'

    def get_context_data(self, **kwargs):
        context = super(ChatDeleteView, self).get_context_data(**kwargs)
        context.update({'segment': 'spm', 'spm_segment': 'chat'})
        return context

    @staticmethod
    def delete_view(request, id):
        obj = Chat.objects.get(id=id)
        obj.delete()
        return HttpResponseRedirect("/spm/chat")


class ChannelToSubscribeListView(LoginRequiredMixin, ListView):
    model = ChannelToSubscribe
    context_object_name = 'channels'
    template_name = 'spamer/home/channels_to_sub.html'

    def get_context_data(self, **kwargs):
        context = super(ChannelToSubscribeListView, self).get_context_data(**kwargs)
        context.update({'segment': 'spm', 'spm_segment': 'chat'})
        return context


class ChannelToSubscribeCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    form_class = ChannelToSubscribeForm
    success_url = '/spm/channel/create/'
    template_name = 'spamer/crud/channel_to_sub_create.html'
    success_message = 'Канал успешно добавлен!'

    def get_context_data(self, **kwargs):
        context = super(ChannelToSubscribeCreateView, self).get_context_data(**kwargs)
        context.update({'segment': 'spm', 'spm_segment': 'chat',
                        'channel': ChannelToSubscribe.objects.filter(user=get_current_user())})
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ChannelToSubscribeUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = ChannelToSubscribe
    form_class = ChannelToSubscribeForm
    template_name = 'spamer/crud/create.html'
    success_url = '/spm/chat'
    success_message = 'Канал успешно обновлен!'

    def get_context_data(self, **kwargs):
        context = super(ChannelToSubscribeUpdateView, self).get_context_data(**kwargs)
        context.update({'segment': 'spm', 'spm_segment': 'chat'})
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ChannelToSubscribeDeleteView(LoginRequiredMixin, DeleteView):
    model = ChannelToSubscribe
    success_url = '/spm/chat'
    template_name = 'spamer/crud/delete.html'
    success_message = 'Канал успешно удалён!'

    def get_context_data(self, **kwargs):
        context = super(ChannelToSubscribeDeleteView, self).get_context_data(**kwargs)
        context.update({'segment': 'spm', 'spm_segment': 'chat'})
        return context


class StatisticsDetailView(LoginRequiredMixin, TemplateView):
    template_name = "spamer/home/statistics.html"

    def get_context_data(self, **kwargs):
        context = super(StatisticsDetailView, self).get_context_data(**kwargs)
        context.update({'segment': 'spm', 'spm_segment': 'stats'})
        return context


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = 'msg'
    paginate_by = 100
    template_name = 'spamer/home/msg.html'

    def get_context_data(self, **kwargs):
        context = super(MessageListView, self).get_context_data(**kwargs)
        context.update({'segment': 'spm', 'spm_segment': 'msg'})
        return context


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    context_object_name = 'client'
    paginate_by = 100
    template_name = 'spamer/home/client.html'

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        context.update({'segment': 'spm', 'spm_segment': 'client'})
        return context


class AccountLoggingListView(LoginRequiredMixin, ListView):
    model = AccountLogging
    context_object_name = 'logging'
    paginate_by = 50
    template_name = 'spamer/home/logging.html'

    def get_context_data(self, **kwargs):
        context = super(AccountLoggingListView, self).get_context_data(**kwargs)
        context.update({'segment': 'spm',
                        'spm_segment': 'logging',
                        })
        return context

    def get_queryset(self):
        return AccountLogging.objects.filter(user=self.request.user)


class GeneralSettingsListView(LoginRequiredMixin, ListView):
    model = GeneralSettings
    context_object_name = 'settings'
    paginate_by = 100
    template_name = 'spamer/home/settings.html'

    def get_context_data(self, **kwargs):
        context = super(GeneralSettingsListView, self).get_context_data(**kwargs)
        context.update({'segment': 'spm', 'spm_segment': 'settings'})
        return context
