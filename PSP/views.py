from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime

from django.core.files.storage import FileSystemStorage
import json


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


class Task:
    def __init__(self, index, name, author):
        self.index = index
        self.name = name
        self.author = author


def task_list(request):
    args = dict()
    task_list = [
        Task(1, "test_problem 1", "me"),
        Task(2, "test_problem 2", "you"),
        Task(3, "test_problem 3", "he"),
    ]
    args["task_list"] = task_list
    return render(request, 'PSP/task_list.html', args)


def task_detail(request, number: int = 1):
    print(request)
    print(request.method)
    if request.method == "POST":
        data = json.loads(request.body)
        print(f'language: {data["language"]}')
        print(f'code: {data["code"]}')
        print(f'task_no: {number}')
        print(f'time: {datetime.now()}')  # 시간은 서버 시간 기준

    args = dict()
    args["task_index"] = number
    return render(request, 'PSP/task_detail.html', args)

    # response = {
    #     "score": 10,
    #     "time": "2023-01-11"
    # }
    #
    # return JsonResponse(response)


def lobby(request):
    return render(request, 'PSP/lobby.html')


def monitoring(request):
    return render(request, 'PSP/monitoring.html')


def end(request):
    return render(request, 'PSP/end.html')


def enroll(request):
    context = {}

    if request.method == "POST":
        prob_name = request.POST.get('prob_name')
        uploaded_file = request.FILES['input_grading_file']
        fs = FileSystemStorage(location='grading_file/')
        fs.save(prob_name, uploaded_file)
        context = {
            'success': "file was uploaded successfully.",
        }

    return render(request, 'PSP/enroll.html', context)
