from django.shortcuts import render
from .forms import PostForm
from .models import Post
from django.db.models import Q
from django.shortcuts import redirect
# Create your views here.


def home_page(request):
    create = request.GET.get("create", False)
    edit = request.GET.get("edit", False)
    delete = request.GET.get("delete", False)
    form = PostForm
    search = request.GET.get('search', False)
    posts = Post.objects.all()

    if delete:
        posts = Post.objects.filter(id=delete)

    if edit:
        post = Post.objects.get(id=edit)
        form = PostForm(instance=post)

    if request.method == "POST":
        if edit:
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                edit = False
        elif delete:
            post = Post.objects.get(id=request.POST.get("post"))
            post.delete()
            return redirect("home")
        else:
            form = PostForm(request.POST)
            if form.is_valid():
                form.save()
                create = False

    if search:
        posts = Post.objects.filter(
            Q(title__icontains=search) | Q(body__icontains=search))

    context = {"edit": edit, "form": form,
               "create": create, "delete": delete, "posts": posts}
    return render(request, 'home.html', context=context)
