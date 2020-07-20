from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from Platform import models
import datetime


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        number = request.POST.get('number')
        pwd = request.POST.get('pswd')
        if number and pwd:
            user = models.User.objects.filter(uId=number).filter(uPwd=pwd)
            restaurant = models.Restaurant.objects.filter(rId=number).filter(rPwd=pwd)
            administrator = models.Administrator.objects.filter(aId=number).filter(aPwd=pwd)
            if user:
                request.session['number'] = number
                request.session['islogin'] = True
                return redirect('/index_user/')
            elif restaurant:
                request.session['number'] = number
                request.session['islogin'] = True
                return redirect('/index_restaurant/')
            elif administrator:
                request.session['number'] = number
                request.session['islogin'] = True
                return redirect('/index_administrator/')
            else:
                # 密码错误或账号不存在
                messages.success(request, "密码错误或账号不存在")
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


def index_user(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.User.objects.filter(uId=number)
        return render(request, 'index_user.html', context={'name': user[0].uName, 'addr': user[0].uAddr,
                                                           'id': user[0].uId, 'tel': user[0].uPhone})


def index_restaurant(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        restaurant = models.Restaurant.objects.filter(rId=number)
        return render(request, 'index_restaurant.html',
                      context={'id': restaurant[0].rId, 'name': restaurant[0].rName, 'addr': restaurant[0].rAddr,
                               'tel': restaurant[0].rTel, 'dysy': restaurant[0].dysy})


def index_administrator(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        admin = models.Administrator.objects.filter(aId=number)
        return render(request, 'index_administrator.html', context={'name': admin[0].aName, 'gender': admin[0].aGender,
                                                                    'id': admin[0].aId, 'age': admin[0].aAge})


def history(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.User.objects.filter(uId=number)
        order = models.Order.objects.filter(userId_id=number)
        return render(request, 'history.html', context={'name': user[0].uName, 'number': number,
                                                        'order': order})


def reserve(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.User.objects.filter(uId=number)
        menu = models.Menu.objects.all()
        restaurant = models.Restaurant.objects.all()

        if request.method == 'GET':
            return render(request, 'reserve.html',
                          context={'name': user[0].uName, 'number': number, 'menu': menu,
                                   'restaurant': restaurant})
        else:
            mid = request.POST.get('mId')
            count = request.POST.get('count')
            menu = models.Menu.objects.filter(mId=mid)
            price = int(menu[0].price) * int(count)
            str = '%d' % price
            messages.success(request, "应付款" + str)
            time = datetime.datetime.now()
            models.Order.objects.create(oTime=time, number=count, money=price,
                                        menuId_id=mid, userId_id=number, status='处理中')
            messages.success(request, '下单成功')
            return redirect('/reserve/')


def current(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.User.objects.filter(uId=number)
        order = models.Order.objects.filter(status='处理中')

        if request.method == 'GET':
            return render(request, 'current.html', context={'name': user[0].uName, 'number': number,
                                                            'order': order})
        else:
            courseid_deleted = request.POST.get('id')
            models.Order.objects.filter(oId=courseid_deleted).update(status='已退订')
            messages.success(request, '退单成功')
            return redirect('/current/')


def handle_current(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.Restaurant.objects.filter(rId=number)
        order = models.Order.objects.filter(status='处理中')

        if request.method == 'GET':
            return render(request, 'restaurant_handle.html', context={'name': user[0].rName, 'number': number,
                                                                      'order': order})
        else:
            courseid_deleted = request.POST.get('id')
            models.Order.objects.filter(oId=courseid_deleted).update(status='已完成')
            messages.success(request, '订单已发货！')
            return redirect('/handle_current/')


def scores_edit(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        cname = request.GET.get('course_name')
        number = request.session.get('number')
        user = models.Restaurant.objects.filter(rId=number)

        courses_data = models.Menu.objects.filter(restaurantId_id=number)
        if cname:
            student_data = models.Menu.objects.filter(mName=cname)
            return render(request, 'scores_edit.html', context={'name': user[0].rName, 'number': number,

                                                                'courses_data': courses_data,
                                                                'student_data': student_data,
                                                                'course_name': cname})
        else:
            cname = '未选中菜'
            student_data = courses_data
            return render(request, 'scores_edit.html', context={'name': user[0].rName, 'number': number,

                                                                'courses_data': courses_data,
                                                                'student_data': student_data,
                                                                'course_name': cname})


def scores_submit(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.Restaurant.objects.filter(rId=number)

        if request.method == 'GET':
            mid = request.GET.get('mid')
            mName = request.GET.get('mName')
            price = request.GET.get('price')

            return render(request, 'scores_submit.html',
                          context={'number': number, 'mName': mName, 'price': price, 'mid': mid})
        else:
            mid = request.POST.get('mid')
            food_name = request.POST.get('food_name')
            food_price = request.POST.get('food_price')

            models.Menu.objects.filter(restaurantId_id=number).filter(mId=mid).update(mName=food_name)
            models.Menu.objects.filter(restaurantId_id=number).filter(mId=mid).update(price=food_price)

            return redirect('/scores_edit/')


def restaurant_history(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        restaurant = models.Restaurant.objects.filter(rId=number)
        order = models.Order.objects.filter()

        return render(request, 'restaurant_history.html', context={'name': restaurant[0].rName, 'number': number,
                                                                   'order': order})


def audit_restaurant(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        selected_department = request.GET.get('selected_department')
        rname = request.session['temp_name']
        raddr = request.session['temp_addr']
        rtel = request.session['temp_tel']
        rmail = request.session['temp_email']
        if rname and raddr and rtel and rmail:
            return render(request, 'audit_restaurant.html', context={'name':rname,})


        if selected_department:  # 下拉框已选择院系
            user_data = models.user.objects.filter(department=selected_department)
            return render(request, 'audit_restaurant.html', context={'name': user[0].name, 'number': number,
                                                              'current_term': current_term,
                                                              'department_data': department_data,
                                                              'user_data': user_data,
                                                              'selected_department': selected_department})
        else:  # 下拉框未选择院系
            selected_department = '未选择学院'
            return render(request, 'audit_restaurant.html', context={'name': user[0].name, 'number': number,
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


def user_register(request):
    if request.method == 'GET':
        return render(request, 'user_register.html')
    else:
        uname = request.POST.get('name')
        upwd1 = request.POST.get('pwd1')
        upwd2 = request.POST.get('pwd2')
        uaddr = request.POST.get('addr')
        uphone = request.POST.get('phone')
        if uname and upwd1 and upwd2 and uaddr and uphone:
            if upwd1 != upwd2:
                messages.error(request, '两次输入的密码不一致，请重新输入!')
                return redirect('/user_register/')
            else:
                same_name = models.User.objects.filter(uName=uname)
                if same_name:
                    messages.error(request, '该用户名已被注册!')
                    return redirect('/user_register/')

                last_id = models.User.objects.order_by('-uId')[0].uId
                new_id = str(int(last_id) + 1)

                new_user = models.User()
                new_user.uId = new_id
                new_user.uName = uname
                new_user.uPwd = upwd2
                new_user.uAddr = uaddr
                new_user.uPhone = uphone
                new_user.save()
                messages.success(request, '注册成功！')
                return redirect('/login/')

        else:
            messages.error(request, '请完整填写注册信息！')
            return redirect('/user_register/')


def restaurant_register(request):
    if request.method == 'GET':
        return render(request, 'restaurant_register.html')
    else:
        rname = request.POST.get('name')
        raddr = request.POST.get('addr')
        rtel = request.POST.get('tel')
        remail = request.POST.get('email')
        if rname and raddr and rtel and remail:
            same_name = models.User.objects.filter(uName=rname)
            if same_name:
                messages.error(request, '该餐厅名已被注册!')
                return redirect('/restaurant_register/')

            # last_id = models.Restaurant.objects.order_by('-rId')[0].rId
            # new_id = str(int(last_id) + 1)

            request.session['temp_name'] = rname
            request.session['temp_addr'] = raddr
            request.session['temp_tel'] = rtel
            request.session['temp_email'] = remail

            messages.success(request, '提交成功，管理员将在12小时内审核，请耐心等待！')
            return redirect('/login/')

        else:
            messages.error(request, '请正确填写注册信息！')
            return redirect('/restaurant_register/')
