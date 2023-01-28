import subprocess

from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime
from .models import CustomUser
from django.db.utils import IntegrityError

from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.core.files.storage import FileSystemStorage
import json
import time
import os
import threading
import sys

# path management
# solution_file/{user_id}/{task_number}/ : 사용자가 제출한 솔루션 파일
# grading_file/{task_number}.py          : 채점용 데이터 파일
# task_file/{task_file_num}.json         : 문제 파일f
# log/compile                            : 컴파일 결과 출력/예외 로그
# log/execute                            : 실행 결과 출력/예외 로그

contest_start_time = datetime(2023, 1, 26, 15, 30, 00)
contest_end_time = datetime(2025, 1, 26, 16, 35, 00)
# contest_end_time = datetime(2023, 1, 26, 16, 35, 00)


# reference code
def test(request):
    return render(request, 'PSP/test.html')


# reference code
def test_back(request):
    # fetch는 이렇게 받아야 하는갑다
    req = json.loads(request.body)

    if request.method == "POST":
        print(f"title : {req['title']}")
        print(f"body  : {req['body']}")
        print(f"userid: {req['userid']}")
    response = {
        "score": 10,
        "date_string": "2023-01-11",
        "current_time": time.ctime(),
    }

    return JsonResponse(response)


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
    # 문제 목록을 보여주는 화면
    # 현재 Task의 제목, 작성자 및 번호를 목록으로 표현합니다.
    
    # 현재 Task에 존재하는 레코드를 전부 가져와서 tasks라는 변수에 저장해주세요.
    # 일단 임시로 Task라는 클래스를 만들어두었는데, DB에 맞게 편하게 수정하면 됩니다.
    # 인출까지 완료했다면 그 뒤는 제가 인계받아 작업하겠습니다. 
    args = dict()
    task_list = [
        Task(1, "test_problem 1", "me"),
        Task(2, "test_problem 2", "you"),
        Task(3, "test_problem 3", "he"),
    ]
    args["task_list"] = task_list
    args["contest_end_time"] = int(time.mktime(contest_end_time.timetuple())) * 1000
    return render(request, 'PSP/task_list.html', args)


def task_detail(request, number: int = 1):
    # 문제 상세 정보를 보여주는 화면
    # 현재 문제의 제목, 작성자, 상세 정보, 예제 입력 및 출력 등 상세 정보를 표현합니다.

    # index가 number에 해당하는 Task 레코드를 가져와서 current_task라는 변수로 저장해주세요.
    # 역시 Task는 편한 대로 수정하시면 됩니다.
    print(request)
    print(request.method)

    number_str = str(number).zfill(5)

    if request.method == "POST":
        # 1. 파싱 및 데이터, 경로 정리
        data = json.loads(request.body)

        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        extension = ".cpp" if data["language"] == "cpp" else ".py"
        user_id = "test_user"  # user_name을 로그인 세션으로부터 가져와야 함
        solution_file_path = f'solution_file/{user_id}/{number_str}/' \
                         f'{current_time}{extension}'
        print(solution_file_path)

        # 2. 없는 디렉터리 생성
        solution_dir = os.path.dirname(solution_file_path)
        os.makedirs(solution_dir, exist_ok=True)

        # 3. 파일 작성
        with open(solution_file_path, 'w', encoding='utf-8') as outfile:
            outfile.write(data["code"])

        # 4. thread로 분리
        def run_solution(number_str):
            # 0. path check
            # log_compile_dir = f"log/compile/{user_id}/{number_str}"  # user_id/datetime.extension
            # log_execute_dir = f"log/execute/{user_id}/{number_str}"
            # log_judge_dir = f"log/judge/{user_id}/{number_str}"
            log_base_dir = f"log/{user_id}/{number_str}/{current_time}"
            log_compile_dir = os.path.join(log_base_dir, "compile")  # user_id/datetime.extension
            log_execute_dir = os.path.join(log_base_dir, "execute")
            log_judge_dir = os.path.join(log_base_dir, "judge")

            program_path = os.path.abspath(f"temp/program/program")

            os.makedirs(f"temp/program", exist_ok=True)
            os.makedirs(log_compile_dir, exist_ok=True)
            os.makedirs(log_execute_dir, exist_ok=True)
            os.makedirs(log_judge_dir, exist_ok=True)

            score = 0
            result_summary = ""
            result_detail = ""
            args = []

            # =================================
            # 컴파일
            # =================================
            if extension == ".cpp":
                # 0. setup path environment
                compiler_path = os.path.abspath("Resource/Compiler/w64devkit")
                compiler_bin_path = os.path.join(compiler_path, 'bin')
                os.environ["W64DEVKIT"] = "1.17.0"
                os.environ["W64DEVKIT_HOME"] = compiler_path
                os.environ["PATH"] = compiler_bin_path + ';' + os.environ["PATH"]

                # 1. 파일 컴파일
                if os.path.exists(program_path + ".exe"):
                    os.remove(program_path + ".exe")

                args = ["g++.exe", "-o", program_path, os.path.abspath(solution_file_path)]
                print(f'args: {args}')

                compile_stdout = (os.path.join(log_compile_dir, "stdout.txt"))
                compile_stderr = (os.path.join(log_compile_dir, "stderr.txt"))

                with open(compile_stdout, 'w') as stdout:
                    with open(compile_stderr, 'w') as stderr:
                        subprocess.run(args, shell=True, stdout=stdout, stderr=stderr)

                # 1.2 에러 있는지 확인

                args = [program_path]

            elif extension == ".py":
                # 0. setup path environment

                args = ["python", solution_file_path]

            # =================================
            # 실행
            # =================================

            # 3. 실행(프로그램 실행)
            execute_stdout = os.path.join(log_execute_dir, "stdout.txt")
            execute_stderr = os.path.join(log_execute_dir, "stderr.txt")
            execute_stdin = os.path.join("input_file", f"{number_str}.txt")

            with open(execute_stdin, 'r') as stdin:
                with open(execute_stdout, 'w') as stdout:
                    with open(execute_stderr, 'w') as stderr:
                        subprocess.run(args, shell=True, stdin=stdin, stdout=stdout, stderr=stderr)

            # =================================
            # 채점
            # =================================

            judge_stdin = execute_stdout
            judge_stdout = os.path.join(log_judge_dir, "stdout.txt")
            judge_stderr = os.path.join(log_judge_dir, "stderr.txt")
            judge_file_path = os.path.join('grading_file', f"{number_str}.py")

            args = ["python", judge_file_path]

            # 2. 테스트 및 채점(프로세스 실행)
            with open(judge_stdin, 'r') as stdin:
                with open(judge_stdout, 'w') as stdout:
                    with open(judge_stderr, 'w') as stderr:
                        subprocess.run(args, shell=True, stdin=stdin, stdout=stdout, stderr=stderr)

            with open(judge_stdout, 'r') as result_file:
                score = int(result_file.readline().strip())

            print("final score: " + str(score))

            # 4. DB 저장

        t = threading.Thread(target=run_solution, args=tuple([number_str]))
        t.start()

    task_file = f'task_file/{number_str}.json'

    args = dict()
    args["task_index"] = number
    args["contest_end_time"] = int(time.mktime(contest_end_time.timetuple())) * 1000

    if os.path.exists(task_file):
        json_data = dict()
        with open(task_file, 'r', encoding='utf-8') as json_fp:
            json_data = json.load(json_fp)
            args["task_title"] = json_data["문제 이름"]
            args["task_article"] = json_data["문제 내용"]
            args["example_input"] = json_data["입력 예시"]
            args["example_output"] = json_data["출력 예시"]

    return render(request, 'PSP/task_detail.html', args)


def lobby(request):
    context = {}
    contest_start_time_ = int(time.mktime(contest_start_time.timetuple())) * 1000
    context = {'time': contest_start_time_}

    if request.method == "POST":
        current_time = datetime.now()
        response = {'contest': " "}

        if contest_start_time > current_time:
            response.update({'contest': "before"})

        if contest_start_time < current_time < contest_end_time:
            response.update({'contest': "in_process"})

        if contest_end_time < current_time:
            response.update({'contest': "end"})

        return JsonResponse(response)

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

        task_score = request.POST.get('task_score')
        # task_file_num과 task_name, task_score 및 업로드 사용자 이름(추가 예정으로 보이네요)을 기반으로 DB에 등록해주세요.

        context = {
            'success': 'file uploaded successfully.',
            'url': task_file_path,
        }

    return render(request, 'PSP/enroll.html', context)


def user_logout(request):
    logout(request)
    return redirect('PSP:index')


def task_timecheck(request):
    if request.method == "POST":
        current_time = datetime.now()
        response = {'contest': " "}

        if contest_start_time < current_time < contest_end_time:
            response.update({'contest': "in_process"})

        if contest_end_time < current_time:
            response.update({'contest': "end"})

        return JsonResponse(response)
