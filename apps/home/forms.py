from django import forms

from betterforms.multiform import MultiModelForm
from django_quill.forms import QuillFormField

from .models import *
from ..middleware import current_user
from django.contrib.auth import get_user_model

User = get_user_model()


class PostForm(forms.ModelForm):
    text = QuillFormField()

    class Meta:
        model = Post
        fields = ['name', 'text', 'template',
                  'photo_1', 'photo_2', 'photo_3', 'photo_4', 'photo_5',
                  'music', 'video', 'document', 'url', 'url_text',
                  'btn_name_1', 'btn_name_2', 'btn_name_3', 'btn_name_4',
                  ]
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Озаглавьте ваш пост, для более удобного управления'}),
            'text': forms.Textarea(attrs={'class': 'form-text', 'style': 'color:black;', 'cols': '60'}),
            'photo_1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_3': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_4': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_5': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'music': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'https://t.me/your_group'}),
            'url_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '...'}),
            'btn_name_1': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-align: center;'}),
            'btn_name_2': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-align: center;'}),
            'btn_name_3': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-align: center;'}),
            'btn_name_4': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-align: center;'}),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        template_set = Template.objects.filter(user_id=current_user.get_current_user_id())
        self.fields['template'].queryset = template_set


class PostPhotoForm(forms.ModelForm):
    class Meta:
        model = PostPhoto
        fields = ['photo_1', 'photo_2', 'photo_3', 'photo_4', 'photo_5']
        widgets = {
            'photo_1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_3': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_4': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_5': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class PostMusicForm(forms.ModelForm):
    class Meta:
        model = PostMusic
        fields = ['music']
        widgets = {
            'music': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class PostVideoForm(forms.ModelForm):
    class Meta:
        model = PostVideo
        fields = ['video']
        widgets = {
            'video': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class PostDocumentForm(forms.ModelForm):
    class Meta:
        model = PostDocument
        fields = ['document']
        widgets = {
            'document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class PostReferenceForm(forms.ModelForm):
    class Meta:
        model = PostReference
        fields = ['reference', 'text']
        widgets = {
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'https://t.me/your_group'}),
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '...'}),
        }


class PostButtonForm(forms.ModelForm):
    class Meta:
        model = Button
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-align: center;'}),
        }


class PostScheduleForm(forms.ModelForm):
    class Meta:
        model = PostSchedule
        fields = ['post', 'schedule', 'is_sent']
        widgets = {
            'post': forms.Select(),
            # 'post': forms.ModelChoiceField(attrs={'class': 'form-control text-info'}),
            'schedule': forms.DateTimeInput(attrs={'class': 'form-control text-info', 'type': 'datetime-local'}),
            'is_sent': forms.HiddenInput(attrs={'value': ''}),
        }

    def __init__(self, *args, **kwargs):
        super(PostScheduleForm, self).__init__(*args, **kwargs)
        post_set = Post.objects.filter(user_id=current_user.get_current_user_id())
        self.fields['post'].queryset = post_set


class PostScheduleMultipleForm(forms.ModelForm):
    class Meta:
        model = PostSchedule
        fields = ['post', 'schedule', 'is_sent']
        widgets = {
            # 'post': forms.ChoiceField(),
            'post': forms.SelectMultiple(),
            # 'post': forms.SelectMultiple(attrs={'class': 'form-control-sm form-control js-multiple-select', 'multiple': 'multiple'}),
            'schedule': forms.DateTimeInput(attrs={'class': 'form-control text-info', 'type': 'datetime-local'}),
            'is_sent': forms.HiddenInput(attrs={'value': ''}),
        }

    def __init__(self, *args, **kwargs):
        super(PostScheduleMultipleForm, self).__init__(*args, **kwargs)
        post_set = Post.objects.filter(user_id=current_user.get_current_user_id())
        self.fields['post'].queryset = post_set


class PostScheduleMultiForm(MultiModelForm):
    form_classes = {
        'post': PostScheduleForm,
    }


class BotForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ['ref', 'token']
        widgets = {
            'ref': forms.TextInput(attrs={'class': 'form-control'}),
            'token': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BotAdminForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ['user', 'ref', 'token']
        widgets = {
            'ref': forms.TextInput(attrs={'class': 'form-control'}),
            'token': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ChatForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ChatForm, self).__init__(*args, **kwargs)
        bot_set = Bot.objects.filter(user_id=current_user.get_current_user_id())
        self.fields['bot'].queryset = bot_set

    class Meta:
        model = Chat
        fields = ['bot', 'chat_type', 'ref']
        widgets = {
            'bot': forms.Select(attrs={'class': 'form-control text-info'}),
            'chat_type': forms.Select(attrs={'class': 'form-control text-info'}),
            'ref': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'https://t.me/blablabla'}),
        }


class ChatAdminForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['bot', 'user', 'chat_type', 'ref']
        widgets = {
            'ref': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'https://t.me/blablabla'}),
        }


class PostAdminForm(forms.ModelForm):
    text = QuillFormField()

    class Meta:
        model = Post
        fields = ['user', 'name', 'text', 'template',
                  'photo_1', 'photo_2', 'photo_3', 'photo_4', 'photo_5',
                  'music', 'video', 'document', 'url', 'url_text',
                  'btn_name_1', 'btn_name_2', 'btn_name_3', 'btn_name_4',
                  ]
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Озаглавьте ваш пост, для более удобного управления'}),
            'text': forms.Textarea(attrs={'class': 'form-text', 'style': 'color:black;', 'cols': '60'}),
            'photo_1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_3': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_4': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_5': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'music': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'адрес ссылки - https://t.me/your_group'}),
            'url_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Текст внутри ссылки'}),
            'btn_name_1': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-align: center;'}),
            'btn_name_2': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-align: center;'}),
            'btn_name_3': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-align: center;'}),
            'btn_name_4': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-align: center;'}),
        }


class PostCreationMultiForm(MultiModelForm):
    form_classes = {
        'post': PostForm,
        'photo': PostPhotoForm,
        'video': PostVideoForm,
        'music': PostMusicForm,
        'document': PostDocumentForm,
        'reference': PostReferenceForm,
        'button': PostButtonForm,
    }


class TemplateForm(forms.ModelForm):
    text = QuillFormField()

    class Meta:
        model = Template
        fields = ['title', 'text']
        widgets = {
            # 'text': forms.TextInput(attrs={'class': 'form-text bg-light'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'например: Шаблон № ...'}),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']


class UserStatusForm(forms.ModelForm):
    class Meta:
        model = UserStatus
        fields = ['is_vip', 'exp_date', 'tz']
        # fields = '__all__'


class UserMultiForm(MultiModelForm):
    form_classes = {
        'user': UserForm,
        'status': UserStatusForm,
    }

