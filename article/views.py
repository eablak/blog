from django.shortcuts import redirect, render,HttpResponse,get_object_or_404,reverse 
from .forms import ArticleForm
from .models import Article,Yorum
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def articles(request):
    articles = Article.objects.all()
    keyword = request.GET.get("keyword")
    
    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(request,"articles.html",{"articles":articles})
    
    articles =Article.objects.all()
    return render(request,"articles.html",{"articles":articles})

def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {
        "articles":articles
    }
    return render(request,"dashboard.html",context)

@login_required(login_url="user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request,"Makale Başarıyla Oluşturuldu.")
        return redirect("article:dashboard")

    return render(request,"addarticle.html",{"form":form})

def detail(request,id):
    #article = Article.objects.filter(id = id).first()
    article = get_object_or_404(Article,id = id)

    yorumlar = article.yorumlar.all()

    return render(request,"detail.html",{"article":article,"yorumlar":yorumlar})

@login_required(login_url="user:login")
def updateArticle(request,id):
    article = get_object_or_404(Article,id = id)
    form = ArticleForm(request.POST or None, request.FILES or None,instance=article)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request,"Makale Başarıyla Güncellendi.")
        return redirect("article:dashboard")

    return render(request,"update.html",{"form":form})

@login_required(login_url="user:login")
def deleteArticle(request,id):
    article = get_object_or_404(Article,id = id)
    article.delete()
    messages.success(request,"Makale Başarıyla Silindi")
    return redirect("article:dashboard")

def addYorum(request,id):
    article = get_object_or_404(Article,id = id)

    if request.method == "POST":
        yorum_author = request.POST.get("yorum_author")
        yorum_content = request.POST.get("yorum_content")

        newYorum = Yorum(yorum_author = yorum_author,yorum_content = yorum_content)
        newYorum.article = article
        newYorum.save()

    return redirect(reverse("article:detail",kwargs={"id":id}))
