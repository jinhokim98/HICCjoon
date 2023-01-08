from django.shortcuts import render


def index(request):
    if request.method == "POST":
        id_ = request.POST.get('id_')
        pw = request.POST.get('password')

        print(id_)
        print(pw)

    return render(request, 'PSP/index.html')
