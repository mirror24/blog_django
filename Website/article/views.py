from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import ArticleColumn, ArticlePost
from .forms import ArticlePostForm
import markdown
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from comment.models import Comment
from comment.forms import CommentForm

from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView


def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    article_list = ArticlePost.object.all()

    if search:
        article_list = article_list.filter(
            Q(title_incontains=search) |
            Q(body_icontains=search)
        )
    else:
        search = ' '

    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    if tag and tag != 'None':
        article_list = article_list.filter(tag__name__in=[tag])

    if order == 'total_view':
        article_list = article_list.order_by('-total_views')

    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = {
        'articles': articles,
        'order': order,
        'search': search,
        'column': column,
        'tag': tag,
    }
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    article = get_object_or_404(ArticlePost, id=id)
    comments = Comment.objects.filter(article=id)

    article.total_views += 1
    article.save(update_fields=['total_views'])

    pre_article = ArticlePost.object.filter(id__it=article.id).order_by('-id')
    next_article = ArticlePost.objects.filter(id__gt=article.id).order_by('id')
    if pre_article.count() > 0:
        pre_article = pre_article[0]
    else:
        pre_article = None

    if next_article.count() > 0:
        next_article = next_article[0]
    else:
        next_article = None

    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    article.body = md.covert(article.body)

    comment_form = CommentForm()

    context = {
        'article': article,
        'toc': md.toc,
        'comments': comments,
        'pre_article': pre_article,
        'next_article': next_article,
        'comment_form': comment_form,
    }
    return render(request, 'article/detail.html', context)


@login_required(login_url='/userprofile/login')
def article_create(request):
    if request.method == 'POST':
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.object.get(id=request.POST['column'])
            new_article.save()
            article_post_form.save_m2m()
            return redirect('article:article_list')
        else:
            return HttpResponse("表单内容有误，请重新填写")
    else:
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        context = {
            'article_post_form': article_post_form,
            'columns': columns,
        }
        return render(request, 'article/create.html', context)


@login_required(login_url='/userprofile/login/')
def article_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse('抱歉，你无权修改这篇文章')
    article.delete()
    return redirect('article:article_list')


@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        if request.user != article.author:
            return HttpResponse('抱歉。你无权修改这篇文章')
        article.delete()
        return redirect('article:article_list')
    else:
        return HttpResponse('仅仅允许post请求')


@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse('抱歉，你无权修改这篇文章')
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']

            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None

            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')

            article.tags.set(*request.POST.get('tags').split(','), clear=True)
            article.save()
            return redirect('article:article_detail', id=id)
        else:
            return HttpResponse('表单内容有误，请重新填写')
    else:
        article_post_form = ArticlePostForm

        columns = ArticleColumn.objects.all()
        context = {
            'article': article,
            'article_post_form': article_post_form,
            'columns': columns,
            'tags': ','.join([x for x in article.tags.names()]),
        }
        return render(request, 'article/update.html', context)


class IncreaseLikeView(View):
    def post(self, request, *args, **kwargs):
        article = ArticlePost.objects.get(id=kwargs.get('id'))
        article.likes += 1
        article.save()
        return HttpResponse('成功')


def article_list_example(request):
    if request.method == 'GET':
        articles = ArticlePost.objects.all()
        context = {'articles': articles}
        return render(request, 'article/list.html', context)


class ContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context.data(**kwargs)
        context['order'] = 'total_views'
        return context


class ArticleListView(ContextMixin, ListView):
    context_object_name = 'articles'
    template_name = 'article/list.html'

    def get_queryset(self):
        queryset = ArticlePost.objects.filter(title='Python')
        return queryset


class ArticleDetailView(DetailView):
    queryset = ArticlePost.objects.all()
    context_object_name = 'article'
    template_name = 'article/detail.html'

    def get_object(self):
        obj = super(ArticleDetailView, self).get_object()
        obj.total_views += 1
        obj.save(update_fields=['total_views'])
        return obj


class ArticleCreateView(CreateView):
    model = ArticlePost
    fields = '__all__'
    template_name = 'article/create_by_class_view.html'
