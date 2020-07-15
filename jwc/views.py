from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from jwc import models

def login(request):
    if request.method == 'GET' :
        return render(request, 'login.html')
    else:
        number = request.POST.get('number')
        pswd = request.POST.get('pswd')
        p = 1
        if number and pswd:
            user = models.user.objects.filter(number=number).filter(pswd=pswd)
            if user:
                request.session['number'] = number
                request.session['islogin'] = True
                if user[0].usertype == '学生':
                    return redirect('/index_student/')
                elif user[0].usertype == '教师':
                    return redirect('/index_teacher/')
                else:
                    return redirect('/index_manager/')
            else:
                # 密码错误
                messages.success(request, "密码错误")
                return render(request, 'login.html')
        # 账号或密码不存在
        else:
            messages.success(request, "账号或密码不能为空")
            return render(request, 'login.html')


def logout(request):
    request.session['number'] = None
    request.session['islogin'] = False
    request.session['id'] = None
    return redirect('/login/')


def index(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        user = models.user.objects.filter(number=request.session.get('number'))
        if user[0].usertype == '学生':
            return redirect('/index_student/')
        elif user[0].usertype == '教师':
            return redirect('/index_teacher/')
        else:
            return redirect('/index_manager/')


def index_student(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.user.objects.filter(number=number)
        return render(request, 'index_student.html', context={'name': user[0].name, 'number': number,
                                                              'department': user[0].department, 'sex': user[0].sex,
                                                              'age': user[0].age})


def index_teacher(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.user.objects.filter(number=number)
        return render(request, 'index_teacher.html', context={'name': user[0].name, 'number': number,
                                                              'department': user[0].department, 'sex': user[0].sex,
                                                              'age': user[0].age})


def index_manager(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.user.objects.filter(number=number)
        return render(request, 'index_manager.html', context={'name': user[0].name, 'number': number,
                                                              'department': user[0].department, 'sex': user[0].sex,
                                                              'age': user[0].age})


def student_scores(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.user.objects.filter(number=number)
        scores_data = models.courseinfo.objects.filter(student_number=number).filter(course_status='past')
        return render(request, 'student_scores.html', context={'name': user[0].name, 'number': number,
                                                               'scores_data': scores_data})


def student_timetable(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.user.objects.filter(number=number)
        scores_data = models.courseinfo.objects.filter(student_number=number).filter(course_status='current')
        term_data = models.term.objects.filter(status='current')
        current_term = ' '
        for i in term_data:
            current_term = i.name + i.id
        return render(request, 'student_timetable.html', context={'name': user[0].name, 'number': number,
                                                                  'scores_data': scores_data,
                                                                  'current_term': current_term})


def course_selection(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.user.objects.filter(number=number)
        opened_course = models.opened_course.objects.all()
        selected_courses = models.courseinfo.objects.filter(student_number=number).filter(course_status='later')
        term_data = models.term.objects.filter(status='later')
        next_term = ' '
        for i in term_data:
            next_term = i.name + i.id
        if request.method == 'GET':
            return render(request, 'course_selection.html',
                          context={'name': user[0].name, 'number': number, 'opened_course': opened_course,
                                   'next_term': next_term, 'selected_courses': selected_courses})
        else:
            courseid_selected = request.POST.get('id')
            # 判断该课程是否已选
            for item in selected_courses:
                if item.course_id == courseid_selected:
                    messages.success(request, '已选此课程，不可重复选择')
                    return redirect('/course_selection/')
            # 判断输入课号是否存在
            course_existing = False
            for item in opened_course:
                if item.id == courseid_selected:
                    course_existing = True
            if course_existing:
                #   写入选课信息
                course_selected = models.opened_course.objects.filter(id=courseid_selected)
                course_id = courseid_selected
                course_name = course_selected[0].name
                course_credit = course_selected[0].credit
                teacher_number = course_selected[0].teacher_number
                teacher_name = course_selected[0].teacher_name
                student_number = number
                student_name = user[0].name
                models.courseinfo.objects.create(course_id=course_id, course_name=course_name,
                                                 course_credit=course_credit, course_status='later',
                                                 teacher_number=teacher_number, teacher_name=teacher_name,
                                                 student_number=student_number, student_name=student_name,
                                                 student_score=None)
                messages.success(request, '选课成功')
                return redirect('/course_selection/')
            else:
                messages.success(request, '无此门课程')
                return redirect('/course_selection/')


#   删除课程
def course_delete(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.user.objects.filter(number=number)
        selected_courses = models.courseinfo.objects.filter(student_number=number).filter(course_status='later')
        term_data = models.term.objects.filter(status='later')
        next_term = ' '
        for i in term_data:
            next_term = i.name + i.id
        if request.method == 'GET':
            return render(request, 'course_delete.html',
                          context={'name': user[0].name, 'number': number, 'next_term': next_term,
                                   'selected_courses': selected_courses})
        else:
            courseid_deleted = request.POST.get('id')
            # 判断该课程是否已选
            for item in selected_courses:
                if item.course_id == courseid_deleted:
                    models.courseinfo.objects.filter(student_number=number).filter(course_id=courseid_deleted).delete()
                    messages.success(request, '退课成功')
                    return redirect('/course_delete/')
            # 没有选择该课程
            messages.success(request, '没有选择编号为' + courseid_deleted + '的课程')
            return redirect('/course_delete/')


def teacher_coursetable(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.user.objects.filter(number=number)
        courses_data = models.courseinfo.objects.filter(teacher_number=number).filter(
            course_status='current').distinct()
        term_data = models.term.objects.filter(status='current')
        current_term = ' '
        for i in term_data:
            current_term = i.name + i.id
        return render(request, 'teacher_coursetable.html', context={'name': user[0].name, 'number': number,
                                                                    'courses_data': courses_data,
                                                                    'current_term': current_term})


def scores_edit(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:  # 下拉框未选课程
        cname = request.GET.get('course_name')
        number = request.session.get('number')
        user = models.user.objects.filter(number=number)
        term_data = models.term.objects.filter(status='current')
        current_term = ' '
        for i in term_data:
            current_term = i.name + i.id
        courses_data = models.courseinfo.objects.filter(teacher_number=number).filter(
            course_status='current').distinct()
        if cname:
            student_data = models.courseinfo.objects.filter(course_name=cname).filter(course_status='current').filter(
                teacher_number=number)
            return render(request, 'scores_edit.html', context={'name': user[0].name, 'number': number,
                                                                'current_term': current_term,
                                                                'courses_data': courses_data,
                                                                'student_data': student_data,
                                                                'course_name': cname})
        else:  # 下拉框已选课程
            cname = '未选择课程'
            student_data = courses_data
            return render(request, 'scores_edit.html', context={'name': user[0].name, 'number': number,
                                                                'current_term': current_term,
                                                                'courses_data': courses_data,
                                                                'student_data': student_data,
                                                                'course_name': cname})


def scores_submit(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.user.objects.filter(number=number)
        term_data = models.term.objects.filter(status='current')
        current_term = ' '
        for i in term_data:
            current_term = i.name + i.id
        if request.method == 'GET':
            course_id = request.GET.get('course_id')
            student_number = request.GET.get('student_number')
            student_name = models.user.objects.filter(number=student_number)
            student_name = student_name[0].name
            course_name = models.courseinfo.objects.filter(course_id=course_id)
            request.session['tempid'] = course_name[0].id
            course_name = course_name[0].course_name
            return render(request, 'scores_submit.html', context={'name': user[0].name, 'number': number,
                                                                  'current_term': current_term,
                                                                  'student_number': student_number,
                                                                  'student_name': student_name,
                                                                  'course_name': course_name})
        else:
            student_score = request.POST.get('id')
            if student_score:
                courseinfo_id = request.session['tempid']
                models.courseinfo.objects.filter(id=courseinfo_id).update(student_score=student_score)
                request.session['tempid'] = None
                messages.success(request, '成绩录入成功')
                return redirect('/scores_edit/')
            else:
                messages.success(request, '成绩不可为空')
                return redirect('/scores_edit/')


def user_edit(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        selected_department = request.GET.get('selected_department')
        number = request.session.get('number')
        user = models.user.objects.filter(number=number)
        term_data = models.term.objects.filter(status='current')
        current_term = ' '
        for i in term_data:
            current_term = i.name + i.id
        user_data = models.user.objects.all()  # 用户表
        department_data = []  # 院系的集合
        for i in user_data:  # 去重
            if i.department not in department_data:
                department_data.append(i.department)
        if request.method == 'POST':  # 新增用户
            number = request.POST.get('number')  # 不会与上文number冲突因为会重定向
            name = request.POST.get('name')
            department = request.POST.get('department')
            usertype = request.POST.get('usertype')
            sex = request.POST.get('sex')
            age = request.POST.get('age')
            pswd = request.POST.get('pswd')
            if number and name and department and usertype and sex and age and pswd:
                models.user.objects.create(number=number, name=name, department=department, usertype=usertype, sex=sex,
                                           age=age, pswd=pswd)
                return redirect('/user_edit/')
            else:
                # messages
                return redirect('/user_edit')
        if selected_department:  # 下拉框已选择院系
            user_data = models.user.objects.filter(department=selected_department)
            return render(request, 'user_edit.html', context={'name': user[0].name, 'number': number,
                                                              'current_term': current_term,
                                                              'department_data': department_data,
                                                              'user_data': user_data,
                                                              'selected_department': selected_department})
        else:  # 下拉框未选择院系
            selected_department = '未选择学院'
            return render(request, 'user_edit.html', context={'name': user[0].name, 'number': number,
                                                              'current_term': current_term,
                                                              'department_data': department_data,
                                                              'user_data': user_data,
                                                              'selected_department': selected_department})


def user_submit(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.user.objects.filter(number=number)
        if request.method == 'GET':  # 通过‘编辑’、‘删除’进入
            userid_selected = request.GET.get('userid')
            ope = request.GET.get('ope')
            request.session['tempid'] = userid_selected
            if ope == '1':  # 编辑用户信息
                user_selected = models.user.objects.filter(number=userid_selected)
                return render(request, 'user_submit.html', context={'name': user[0].name, 'number': number,
                                                                    'user_selected': user_selected})
            else:  # 删除用户
                models.user.objects.filter(number=userid_selected).delete()  # user表中删除
                models.courseinfo.objects.filter(student_number=userid_selected).delete()  # courseinfo表中删除
                return redirect('/user_edit/')
        else:  # 修改用户信息
            number = request.POST.get('number')
            name = request.POST.get('name')
            department = request.POST.get('department')
            usertype = request.POST.get('usertype')
            sex = request.POST.get('sex')
            age = request.POST.get('age')
            pswd = request.POST.get('pswd')
            if number and name and department and usertype and sex and age and pswd:
                userid_selected = request.session['tempid']
                models.user.objects.filter(number=userid_selected).update(number=number, name=name,
                                                                          department=department,
                                                                          usertype=usertype, sex=sex, age=age,
                                                                          pswd=pswd)
                request.session['tempid'] = None
                # messages.success(request, '信息修改成功')
                return redirect('/user_edit/')
            else:
                # messages.success(request, '所有信息不能为空')
                return redirect('/user_edit/')


def course_edit(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.user.objects.filter(number=number)
        term_data = models.term.objects.filter(status='later')
        next_term = ' '
        for i in term_data:
            next_term = i.name + i.id
        opened_course = models.opened_course.objects.all()  # 当前学期开课表
        if request.method == 'POST':  # 新增用户
            id = request.POST.get('id')  # 不会与上文number冲突因为会重定向
            credit = request.POST.get('credit')
            name = request.POST.get('name')
            teacher_number = request.POST.get('teacher_number')
            teacher_name = request.POST.get('teacher_name')
            if id and credit and name and teacher_number and teacher_name:
                models.opened_course.objects.create(id=id, credit=credit, name=name, teacher_number=teacher_number,
                                                    teacher_name=teacher_name)
                return redirect('/course_edit/')
            else:
                # messages
                return redirect('/course_edit')
        else:  # 刷新、进入页面等非post
            return render(request, 'course_edit.html', context={'name': user[0].name, 'number': number,
                                                                'next_term': next_term,
                                                                'opened_course': opened_course})


def course_submit(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.user.objects.filter(number=number)
        term_data = models.term.objects.filter(status='current')
        current_term = ' '
        for i in term_data:
            current_term = i.name + i.id
        if request.method == 'GET':  # 通过‘编辑’、‘删除’进入
            courseid_selected = request.GET.get('courseid')
            ope = request.GET.get('ope')
            # 管理员有可能修改id及其他基本信息，所以提交表单时找不到定位用户表数据的内容，此时记录修改的id
            request.session['tempid'] = courseid_selected
            if ope == '1':  # 编辑课程信息
                course_selected = models.opened_course.objects.filter(id=courseid_selected)
                return render(request, 'course_submit.html', context={'name': user[0].name, 'number': number,
                                                                      'current_term': current_term,
                                                                      'course_selected': course_selected})
            else:  # 删除课程
                models.opened_course.objects.filter(id=courseid_selected).delete()  # opened_course表中删除
                return redirect('/course_edit/')
        else:  # 修改课程信息
            id = request.POST.get('id')  # 不会与上文number冲突因为会重定向
            credit = request.POST.get('credit')
            name = request.POST.get('name')
            teacher_number = request.POST.get('teacher_number')
            teacher_name = request.POST.get('teacher_name')
            if id and credit and name and teacher_number and teacher_name:
                courseid_selected = request.session['tempid']
                models.opened_course.objects.filter(id=courseid_selected).update(id=id, credit=credit, name=name,
                                                                                 teacher_number=teacher_number,
                                                                                 teacher_name=teacher_name)
                # 以免后续引起bug
                request.session['tempid'] = None
                print('alter success!')
                return redirect('/course_edit/')
            else:
                # messages.success(request, '所有信息都不能为空')
                return redirect('/course_edit/')


def term_edit(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.user.objects.filter(number=number)
        term_data = models.term.objects.filter(status='current')
        current_term = ' '
        for i in term_data:
            current_term = i.name + i.id
        term_data = models.term.objects.all()  # 当前学期表
        if request.method == 'POST':  # 新增学期
            id = request.POST.get('id')  # 不会与上文number冲突因为会重定向
            name = request.POST.get('name')
            if id and name:
                # 新增学期修改数据库
                models.term.objects.filter(status='current').update(status='past')
                models.term.objects.filter(status='later').update(status='current')
                models.term.objects.create(id=id, name=name, status='later')
                models.opened_course.objects.all().delete()
                models.courseinfo.objects.filter(course_status='current').update(course_status='past')
                models.courseinfo.objects.filter(course_status='later').update(course_status='current')
                return redirect('/term_edit/')
            else:
                # messages
                return redirect('/term_edit')
        else:  # 刷新、进入页面等非post
            return render(request, 'term_edit.html', context={'name': user[0].name, 'number': number,
                                                              'current_term': current_term,
                                                              'term_data': term_data})
