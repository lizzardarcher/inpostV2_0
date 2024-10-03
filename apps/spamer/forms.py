from django import forms
from django.contrib.auth import get_user_model

from apps.spamer.models import *
from ..middleware import current_user

User = get_user_model()


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            # 'id_account',
            'first_name',
            'last_name',
            'photo',
            'bio',
            # 'api_id',
            # 'api_hash',
            # 'phone',
            # 'sms_code',
            # 'signed_in',
            # 'status',
            # 'report',
            # 'session',
            # 'session_for_chat',
            # 'session_for_lk',
            'common_text_ref',
            # 'media',
            'auto_answering_text_ref',
            'is_auto_answering_active',
            'is_spam_active',
            # 'is_spam_lk_active',
            'delay',
            'delay_2',
            # 'master_to_forward',
            # 'account_enabled'
        ]
        widgets = {
            # 'id_account': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'username': forms.TextInput(attrs={'class': 'form-control'}),
            # 'api_id': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'api_hash': forms.TextInput(attrs={'class': 'form-control'}),
            # 'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.TextInput(attrs={'class': 'form-control'}),
            # 'photo': forms.ImageField(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            # 'sms_code': forms.TextInput(attrs={'class': 'form-control'}),
            # 'signed_in': forms.CheckboxInput(attrs={'class': 'form-control'}),
            # 'status': forms.CheckboxInput(attrs={'class': 'form-control'}),
            # 'report': forms.TextInput(attrs={'class': 'form-control'}),
            # 'session_for_chat': forms.TextInput(attrs={'class': 'form-control'}),
            # 'session_for_lk': forms.TextInput(attrs={'class': 'form-control'}),
            # 'media': forms.FileInput(attrs={'class': 'form-control'}),
            'common_text_ref': forms.Select(attrs={'class': 'form-control text-info' }),
            'auto_answering_text_ref': forms.Select(attrs={'class': 'form-control text-info' }),
            'is_auto_answering_active': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'is_spam_active': forms.CheckboxInput(attrs={'class': 'form-control'}),
            # 'is_spam_lk_active': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'delay': forms.TextInput(attrs={'class': 'form-control'}),
            'delay_2': forms.NumberInput(attrs={'class': 'form-control'}),

            # 'master_to_forward': forms.CheckboxInput(attrs={'class': 'form-control'}),
            # 'account_enabled': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }


class AccountUploadForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['session','session_aa', 'common_text_ref', 'auto_answering_text_ref', ]
        widgets = {
            'session': forms.FileInput(attrs={'class': 'form-control'}),
            'session_aa': forms.FileInput(attrs={'class': 'form-control'}),
            # 'common_text': forms.Textarea(attrs={'class': 'form-control'}),
            'common_text_ref': forms.Select(attrs={'class': 'form-control text-info'}),
            # 'auto_answering_text': forms.Textarea(attrs={'class': 'form-control'}),
            'auto_answering_text_ref': forms.Select(attrs={'class': 'form-control text-info'}),
        }


class TelegramAccountForm(forms.Form):
    phone = forms.CharField(label='Номер телефона', max_length=15)


class AccountSMSHandlerForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['sms_code', ]
        widgets = {
            'sms_code': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['text', 'delay','is_emoji_allowed',
                  'is_del_mes_available', 'comment']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'delay': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_emoji_allowed': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'is_del_mes_available': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ChatUploadForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['link', ]
        widgets = {
            'link': forms.URLInput(attrs={'class': 'form-control'}),
        }


class ChannelToSubscribeForm(forms.ModelForm):
    class Meta:
        model = ChannelToSubscribe
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AutoAnsweringTemplateForm(forms.ModelForm):
    class Meta:
        model = AutoAnsweringTemplate
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }


class CommonTextTemplateForm(forms.ModelForm):
    class Meta:
        model = CommonTextTemplate
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }