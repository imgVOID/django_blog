from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from .models import Tag
import re
from django.db.models import Q

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
    number_of_post = int(posts.number)
    percentnum = int(posts.number / posts.paginator.num_pages * 100)
    percent = str(percentnum) + '%'
    return render(request, 'index.html', {'page': page, 'posts': posts, 'percent': percent, 'percentnum': percentnum, 'number_of_post':number_of_post})

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

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    query = None 
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['title', 'text',])

        found_entries = Post.objects.filter(entry_query).order_by('-published_date')

    return render(request, 'search.html', { 'query_string': query_string, 'found_entries': found_entries })

def tag_detail(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    count = Tag.objects.all().count()
    posts = Post.objects.all().filter(tag=tag)
    return render(request, 'tag_detail.html', {'tag':tag, 'count':count, 'posts':posts})