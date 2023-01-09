from django.shortcuts import render, redirect


def index(request):
    if request.method == "POST":
        id_ = request.POST.get('id_')
        pw = request.POST.get('password')

        print(id_)
        print(pw)

        return redirect('PSP:lobby')

    return render(request, 'PSP/index.html')


def signup(request):
    if request.method == "POST":
        new_name = request.POST.get('join_name')
        new_id = request.POST.get('join_id')
        new_pw = request.POST.get('join_pw')

        print(new_name)
        print(new_id)
        print(new_pw)

        return redirect('PSP:index')

    return render(request, 'PSP/signup.html')


def lobby(request):
    return render(request, 'PSP/lobby.html')


def monitoring(request):
    return render(request, 'PSP/monitoring.html')
