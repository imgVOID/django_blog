from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)

    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.page_num)
    percentnum = int(posts.number / posts.paginator.num_pages * 100)
    percent = str(percentnum) + '%'
    return render(request, 'index.html', {'page': page, 'posts': posts, 'percent': percent, 'percentnum': percentnum})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    count = Post.objects.all().count()
    pkprevious = int(pk)-1
    pknext = int(pk)+1
    return render(request, 'post_detail.html', {'post': post,'pkprevious':pkprevious, 'pknext':pknext, 'count':count})

def archieve(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    paginator = Paginator(posts, 20)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)

    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.page_num)
    return render(request, 'archieve.html', {'page': page, 'posts': posts})
