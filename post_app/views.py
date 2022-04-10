from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, FormView
from .models import *
from .forms import *
from django.urls import reverse_lazy,reverse
from django.http import request, Http404
from django.http.response import JsonResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from . import forms

#formの記述(https://qiita.com/box16/items/23f78e1014f6dc8f849e)
posted_comment_text = {"text":""}

# Create your views here.
class ListClass(ListView) :
    template_name = 'home.html'
    model = Post  
    queryset = Post.objects.order_by('-posted_at') # (https://qiita.com/yongjugithub/items/edd69e1ac6d4507f9ad1)
 
    def get_context_data(self, *args, **kwargs): # (https://qiita.com/yongjugithub/items/edd69e1ac6d4507f9ad1)
        context = super().get_context_data(*args, **kwargs)
        context["comment_list"] = Comment.objects.all()
        return context

class FormClass(CreateView): # Post投稿画面
    template_name = 'post_form.html'
    model = Post
    # fields = ['text','upload_img']
    form_class = PostForm
    success_url = reverse_lazy('home') # 投稿完了時の遷移先



    # (https://noumenon-th.net/programming/2019/11/18/django-createview/)
    # def get_form(self):
    #     form = super(FormClass, self).get_form()
    #     form.fields['text'].label = '投稿本文'
    #     form.fields['upload_img'].label = '投稿画像'
    #     return form

class DetailClass(DetailView):
    template_name = 'detail.html'
    model = Post

    def get_context_data(self, **kwargs):
        ctxt = super().get_context_data()
        ctxt["object_list"] = Post.objects.all()
        ctxt["comment_list"] = Comment.objects.all()
        return ctxt
    
    def get_form(self):
        form = super(CommentForm, self).get_form()
        form.fields['subject'].label = '題'
        form.initial['subject'] = self.kwargs['pk'] # フィールドの初期値の設定(https://k-mawa.hateblo.jp/entry/2017/10/31/235640)
        form.fields['text'].required = True
        return form

    success_url = reverse_lazy('list')

# Comment投稿画面
# 参考4/04(https://yu-nix.com/blog/2021/7/31/django-create-view/)
class CommentForm(CreateView):
    template_name = 'detail.html'
    model = Comment
    # (https://qiita.com/onishi_820/items/c9418f95a8e4e828dfc4)
    #form_class = CommentForm
    fields = ['text','subject']
    #(https://stackoverflow.com/questions/51123269/django-formview-pass-pk-in-success-url)
    pk = None

    # コメント投稿画面に投稿先を表示
    def get_context_data(self,**kwargs):
        ctxt = super().get_context_data()
        ctxt["object_list"] = Post.objects.all()
        ctxt["comment_list"] = Comment.objects.all()
        ## pkを元にオブジェクト取得(https://yaruki-strong-zero.hatenablog.jp/entry/django_model_lookup)
        # pkを元にオブジェクト取得2(https://k-mawa.hateblo.jp/entry/2017/10/31/235640)
        ctxt["post"] = Post.objects.get(id=self.kwargs['pk'])
        return ctxt
    
    def get_form(self):
        form = super(CommentForm, self).get_form()
        form.fields['subject'].label = '題'
        form.initial['subject'] = self.kwargs['pk'] # フィールドの初期値の設定(https://k-mawa.hateblo.jp/entry/2017/10/31/235640)
        form.fields['text'].required = True
        return form

    """
    # (https://webty.jp/staffblog/production/post-1158/)
    url = request.path + 
    """
    success_url = reverse_lazy('detail')
    
    #動的にurlを設定する(https://stackoverflow.com/questions/51123269/django-formview-pass-pk-in-success-url)
    def get_success_url(self):
         return reverse('detail', kwargs={'pk': self.kwargs['pk']})


def ApiGoodView(request,pk):
    try:
        obj = Post.objects.get(pk=pk) # pkを元にPostテーブルの対象記事レコードを取得する
    except Post.DoesNotExist:
        raise Http404
    obj.good += 1  # ここでいいねの数を増やす
    obj.save()  # 保存をする
    

    return JsonResponse({"good":obj.good}) # いいねの数をJavaScriptに渡す


class MyLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = "accounts-login.html"

class MyLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "accounts-logout.html"

class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "accounts-create.html"
    success_url = reverse_lazy("login")


def ApiGoodView(request,pk):
    try:
        obj = Post.objects.get(pk=pk) # pkを元にPostテーブルの対象記事レコードを取得する
    except Post.DoesNotExist:
        raise Http404
    obj.good += 1  # ここでいいねの数を増やす
    obj.save()  # 保存をする
    

    return JsonResponse({"good":obj.good}) # いいねの数をJavaScriptに渡す

class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = 'thanks'