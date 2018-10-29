from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from . import file_sys
from .models import Category, File
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

fs = file_sys.FileSys()


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('test')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required(login_url='accounts/login')
def index(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'index.html', {'fs': fs.get_content(), 'categories': categories})


@csrf_exempt
def add_category(request):
    name = request.POST.get('name', None)

    if Category.objects.filter(name=name, user=request.user).count() == 0:
        category = Category(name=name, user=request.user)
        category.save()

    data = [cat.name for cat in Category.objects.filter(user=request.user)]
    return JsonResponse(data, safe=False)


@csrf_exempt
def del_category(request):
    name = request.POST.get('name', None)
    Category.objects.filter(name=name, user=request.user).delete()

    data = [cat.name for cat in Category.objects.filter(user=request.user)]
    return JsonResponse(data, safe=False)


@csrf_exempt
def go_to(request):
    folder = request.POST.get('folder', None)
    data = fs.go_to(folder)
    return JsonResponse(data, safe=False)


@csrf_exempt
def add_file(request):
    file_name = request.POST.get('file', None)
    category = Category.objects.filter(name=request.POST.get('category', None), user=request.user)[0]
    if File.objects.filter(name=file_name, category=category).count() == 0:
        file = File(name=file_name, category=category)
        file.save()
        files = [cat.name for cat in category.file_set.all()]
        return JsonResponse(files, safe=False)
    else:
        return JsonResponse(False, safe=False)


@csrf_exempt
def del_file(request):
    file_name = request.POST.get('file', None)
    cat_name = request.POST.get('category', None)

    category = Category.objects.filter(name=cat_name, user=request.user)[0]

    File.objects.filter(name=file_name, category=category).delete()
    files = [cat.name for cat in category.file_set.all()]
    return JsonResponse(files, safe=False)


@csrf_exempt
def get_files(request):
    category = Category.objects.filter(name=request.POST.get('category', None), user=request.user)[0]
    files = [cat.name for cat in category.file_set.all()]
    return JsonResponse(files, safe=False)
