from django.shortcuts import render, redirect
from django.http import JsonResponse


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


def task(request, number: int = 1):
    # print(request)
    # print(request.method)
    # if request.method == "POST":
    #     source_code = request.POST.get('code')
    #     language = request.POST.get('language')
    #     print(f'source_code: {source_code}')
    #     print(f'language: {language}')
    args = dict()
    args["task_index"] = number
    return render(request, 'PSP/task.html', args)


def task_submit(request):
    print("-=-=-=-=-")
    print(request)
    print(request.method)
    if request.method == "POST":
        source_code = request.POST.get('code')
        language = request.POST.get('language')
        print(f'source_code: {source_code}')
        print(f'language: {language}')
    
    response = {
        "score": 10,
        "time": "2023-01-11"
    }

    return JsonResponse(response)


def lobby(request):
    return render(request, 'PSP/lobby.html')


def monitoring(request):
    return render(request, 'PSP/monitoring.html')


def end(request):
    return render(request, 'PSP/end.html')
