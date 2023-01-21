from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime
from .models import CustomUser
from django.db.utils import IntegrityError

from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.core.files.storage import FileSystemStorage
import json


def index(request):
    context = {
        'Authenticate_fail': False,
        'DoesNotExist': False
    }

    if request.method == "POST":
        id_ = request.POST.get('id_')
        pw = request.POST.get('password')

        try:
            user = CustomUser.objects.get(username=id_)

            if not check_password(pw, user.password):
                raise ValueError

            login(request, user)
            if user.is_staff:
                return redirect('PSP:monitoring')
            else:
                return redirect('PSP:lobby')

        except ValueError:
            context.update({'Authenticate_fail': True})

        except CustomUser.DoesNotExist:
            context.update({'DoesNotExist': True})

    return render(request, 'PSP/index.html', context)


def signup(request):
    context = {'id_duplicate': False}

    if request.method == "POST":
        new_name = request.POST.get('join_name')
        new_id = request.POST.get('join_id')
        new_pw = request.POST.get('join_pw')

        try:
            CustomUser.objects.create_user(
                username=new_id,
                password=new_pw,
                nickname=new_name
            )
            return redirect('PSP:index')

        except IntegrityError:
            context.update({'id_duplicate': True})

        # 렌더함수가 호출되면 페이지가 재로딩되기 때문에 지금까지 입력한 정보들이 날아가서 불편함 (해결방법.....)

    return render(request, 'PSP/signup.html', context)


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
    context = {}

    # 추가로 페이지 하단에 대회까지 남은 시간을 보여주고 있다.
    # 대회 시작시간을 DB에서 가져오려 했지만 contest 테이블이 사라졌기 때문에 여기서 대회 시간을 넘겨주었으면 함
    # 추가로 대회가 시작한 이후와 대회가 종료된 이후에는 이 페이지로 들어올 수 없다.
    # 대회 시작시간이 지났는지 확인하는 변수를 만들어서 넘겨줬으면 함

    return render(request, 'PSP/lobby.html', context)


def monitoring(request):
    context = {}

    # 추가로 페이지 하단에 대회 종료까지 남은 시간을 보여주고 있다.
    # 대회 종료시간을 DB에서 가져오려 했지만 contest 테이블이 사라졌기 때문에 여기서 대회 종료 시간을 넘겨주었으면 함

    # 대회 참가자 현황과 대회 실시간 랭킹을 보여주고 있는 화면이다.
    # 대회 참가자 현황은 현재 로그인 하고 있는 사람들의 정보를 가져와서 리스트로 전달해주었으면 함
    # 딕셔너리의 key 이름은 contest_participants value를 리스트로 전달해주면 됨
    # 대회 실시간 랭킹은 유저가 문제 별로 채점 요청을 하고 DB에 solution 안에 점수가 기록될 때 랭킹이 반영되어야한다.
    # 딕셔너리의 key 이름은 contest_ranking value를 리스트로 전달해주면 된다.
    # 아마 이것은 비동기 통신을 사용해야 할 듯

    return render(request, 'PSP/monitoring.html', context)


def end(request):
    context = {}

    # 대회가 종료되었을 때 보여지는 화면
    # lobby, task, task_detail에서 대회 시간이 종료된 즉시 이 페이지로 넘어가야한다.
    # 여기서는 대회 참가자 이름과 점수, 걸린 시간, 해결한 문제 개수를 보여줘야한다.
    # username, score, during_time, solving_problem 네 가지 키 값을 넣어서 렌더해주면 된다.
    # DB에서 점수, 해결한 문제 수를 가져오면 될 듯

    return render(request, 'PSP/end.html', context)


def enroll(request):

    # grading_file과 task_file을 저장하는 곳
    # grading_file은 py파일이 저장되며, task_file은 json으로 저장된다.
    # 여기서는 문제 이름이 중복됐는지만 확인해주면 될 것 같다.

    context = {}

    if request.method == "POST":
        task_info = {
            "문제 이름": request.POST.get('task_name'),
            "문제 내용": request.POST.get('task_desc'),
            "입력 예시": request.POST.get('input_example'),
            "출력 예시": request.POST.get('output_example')
        }

        task_file_num = '00001'
        task_file_path = f'task_file/{task_file_num}.json'

        with open(task_file_path, 'w', encoding='utf-8') as outfile:
            json.dump(task_info, outfile, indent="\t", ensure_ascii=False)

        task_name_py = task_file_num + ".py"
        uploaded_file = request.FILES['input_grading_file']
        fs = FileSystemStorage(location='grading_file/')
        fs.save(task_name_py, uploaded_file)

        context = {
            'success': 'file uploaded successfully.',
            'url': task_file_path,
        }

    return render(request, 'PSP/enroll.html', context)


def user_logout(request):
    logout(request)
    return redirect('PSP:index')
