from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.db.models import Count
from django.forms.models import model_to_dict
from Platform import models
import datetime

from numpy import *
from numpy import linalg as la

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

def aitest(request):
    userId = request.POST.get('useid')
    result = models.Order.objects.filter(status = '已完成').order_by('userId')
    matrixdata = []
    for item in result:
        transferitem = model_to_dict(item)
        matrixdata.append([transferitem['userId'],transferitem['menuId'],transferitem['evaluation']])

    def loadExData2():
        return [[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
                [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],
                [0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],
                [3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],
                [5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],
                [0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],
                [4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],
                [0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],
                [0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],
                [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
                [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]]

    # 计算两个评分的欧氏距离
    def esclidSim(inA, inB):
        if len(inA) < 3:
            return 1.0
        return 1.0 / (1.0 + la.norm(inA - inB))

    # 计算两个评分的 皮尔逊相关系数 (Pearson Correlation)
    def pearsSim(inA, inB):
        if len(inA) < 3:
            return 1.0
        return 0.5 + 0.5 * corrcoef(inA.inB)[0][1]

    # 计算两个评分的余弦相似度 (Cosine similarity)
    def cosSim(inA, inB):
        num = float(inA.T * inB)
        denom = la.norm(inA) * la.norm(inB)
        return 0.5 + 0.5 * (num / denom)

    # 基于物品的相似度推荐
    def standEst(dataMat, user, sinMeas, item):
        n = shape(dataMat)[1]
        simTotal = 0.0;
        ratsimTotal = 0.0
        for j in range(n):
            userRating = dataMat[user, j]
            if userRating == 0:
                continue
            overLap = nonzero(logical_and(dataMat[:, item].A > 0, dataMat[:, j].A > 0))[0]
            if len(overLap) == 0:
                simility = 0
            else:
                simility = sinMeas(dataMat[overLap, item], dataMat[overLap, j])
                print("the %d and %d similit is :%f" % (item, j, simility))
            simTotal += simility
            ratsimTotal += simility * userRating
        if simTotal == 0:
            return 0
        else:
            return ratsimTotal / simTotal

    def recommand(dataMat, user, n=3, simMeans=cosSim, estMethod=standEst):
        unratedItems = nonzero(dataMat[user, :].A == 0)[1]
        if len(unratedItems) == 0:
            return "you rated everything"
        itemScores = []
        for item in unratedItems:
            estimatscore = estMethod(dataMat, user, simMeans, item)
            itemScores.append((item, estimatscore))
        return sorted(itemScores, key=lambda jj: jj[1], reverse=True)[:n]

    myMat = mat(loadExData2())
    print(recommand(myMat, 1))
    return HttpResponse(matrixdata)

def recommand(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.User.objects.filter(uId=number)
        recommandations = models.Order.objects.filter(userId = number,status = '已完成').values('menuId').annotate(au=Count('menuId')).order_by('-au')
        recommandmenu1 = []
        recommandmenu2 = []
        for item in recommandations:
            Object = model_to_dict(models.Menu.objects.get(mId = item['menuId']))
            recommandmenu1.append(Object)
        recommandmenu1 = recommandmenu1[0:6]
    return render(request, 'recommand.html',
                  context={'name': user[0].uName, 'number': number,
                            'recommandations': recommandmenu1 ,'AIrecommandations': recommandmenu2})

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


def edit_menu(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        cname = request.GET.get('course_name')
        number = request.session.get('number')
        user = models.Restaurant.objects.filter(rId=number)

        courses_data = models.Menu.objects.filter(restaurantId_id=number)
        if cname:
            student_data = models.Menu.objects.filter(mName=cname)
            return render(request, 'edit_menu.html', context={'name': user[0].rName, 'number': number,

                                                                'courses_data': courses_data,
                                                                'student_data': student_data,
                                                                'course_name': cname})
        else:
            cname = '未选中菜'
            student_data = courses_data
            return render(request, 'edit_menu.html', context={'name': user[0].rName, 'number': number,

                                                                'courses_data': courses_data,
                                                                'student_data': student_data,
                                                                'course_name': cname})


def menu_submit(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.Restaurant.objects.filter(rId=number)

        if request.method == 'GET':
            mid = request.GET.get('mid')
            mName = request.GET.get('mName')
            price = request.GET.get('price')

            return render(request, 'menu_submit.html',
                          context={'number': number, 'mName': mName, 'price': price, 'mid': mid})
        else:
            mid = request.POST.get('mid')
            food_name = request.POST.get('food_name')
            food_price = request.POST.get('food_price')

            models.Menu.objects.filter(restaurantId_id=number).filter(mId=mid).update(mName=food_name)
            models.Menu.objects.filter(restaurantId_id=number).filter(mId=mid).update(price=food_price)

            return redirect('/edit_menu/')


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
        useless = models.TmpRestaurant.objects.filter(t_status=0).all()
        if useless:
            useless.delete()
        number = request.session.get('number')
        admin = models.Administrator.objects.filter(aId=number)
        temp_res = models.TmpRestaurant.objects.all()
        checked = 0

        if temp_res:
            if request.method == 'GET':
                return render(request, 'audit_restaurant.html',
                              context={'name': admin[0].aName, 'temp_res': temp_res})

            else:
                temp_id = request.POST.get('temp_id')
                temp = temp_res.filter(t_id=temp_id).get()
                checked = request.POST.get('check')
                if checked == '1':
                    new_restaurant = models.Restaurant()
                    new_restaurant.rName = temp.t_name
                    new_restaurant.rAddr = temp.t_addr
                    new_restaurant.rTel = temp.t_tel
                    new_restaurant.rEmail = temp.t_email

                    last_id = models.Restaurant.objects.order_by('-rId')[0].rId
                    new_id = "000" + str(int(last_id) + 1)
                    rpwd = new_id
                    new_restaurant.rId = new_id
                    new_restaurant.rPwd = rpwd
                    new_restaurant.save()
                    temp.t_status = 0
                    temp.save()

                    # messages.success(request, '审核通过！')
                    return redirect('/audit_restaurant/')
                else:
                    temp.t_status = 0
                    temp.save()
                    return redirect('/audit_restaurant/')
        else:
            return render(request, 'audit_restaurant.html',
                          context={'name': admin[0].aName})


def delete_restaurant(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        admin = models.Administrator.objects.filter(aId=number)
        all_res = models.Restaurant.objects.all()
        print("check")
        if request.method == 'GET':
            return render(request, 'delete_restaurant.html', context={'name': admin[0].aName, 'all_res': all_res})
        else:
            temp_id = request.POST.get('temp_id')
            temp = all_res.filter(rId=temp_id).get()
            if temp:
                temp.delete()
            return redirect('/delete_restaurant/')




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

            new_tmp_res = models.TmpRestaurant()
            new_tmp_res.t_name = rname
            new_tmp_res.t_addr = raddr
            new_tmp_res.t_tel = rtel
            new_tmp_res.t_email = remail
            new_tmp_res.save()

            messages.success(request, '提交成功，管理员将在12小时内审核，请耐心等待！')
            return redirect('/login/')

        else:
            messages.error(request, '请正确填写注册信息！')
            return redirect('/restaurant_register/')
