from cgitb import text
from dataclasses import fields
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import forms as auth_forms
from .models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text','upload_img']

    def __init__(self, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs["class"] = "form-control"
        super().__init__(*args, **kwargs)

# (https://qiita.com/onishi_820/items/c9418f95a8e4e828dfc4)
class CommentForm(forms.ModelForm):
    class Meta:
        # どのモデルをフォームにするか指定
        model = Comment
        # そのフォームの中から表示するフィールドを指定
        fields = ['text']

    # フォームを綺麗にするための記載
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TextInputというのはwidgetの種類
        self.fields['text'].widget = forms.TextInput(attrs={'placeholder': 'コメントを追加'}) #(https://blog.narito.ninja/detail/52)
        # subjectを非表示
        self.fields['subject'].widget = forms.HiddenInput()


class LoginForm(auth_forms.AuthenticationForm):
    def __init__(self,*args, **kw):
        super().__init__(*args,**kw)
        for field in self.fields.values():
            field.widget.attrs['placeolder'] = field.label

class ContactForm(forms.Form):
    pass
    # ログインユーザーの名前を設定

    # テキスト入力
    text = forms.CharField()

