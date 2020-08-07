from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from django.forms.models import model_to_dict
from Platform import models
from django.db.models import F
import datetime
from alipay import AliPay, DCAliPay, ISVAliPay

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
            print("fff")
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
        user = models.User.objects.filter(number=request.session.get('number'))
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
        meun = models.Menu.objects.filter(restaurantId=number)
        order = models.Order.objects.all()
        name1 = []
        name_list = []
        # name1_list = []
        # price_list = []
        result_list = []
        for item in meun:
            d = {'value': 0, 'name': item.mName, 'id': item.mId}
            name1.append(item.mName)
            name_list.append(d)
        for item in order:
            # name1_list.append(item.menuId.mName)
            # price_list.append(item.money)
            for name_id in name_list:
                if item.menuId.mId == name_id['id']:
                    name_id['value'] = name_id['value'] + 1
        for name_id in name_list:
            d = {'value': name_id['value'], 'name': name_id['name']}
            result_list.append(d)
        print(result_list)

        result_list1 = [{'value': 10, 'name': '烤全鸡'}, {'value': 4, 'name': '卤鸭架'}, {'value': 4, 'name': '麻辣鸭腿'}
                        ]
        return render(request, 'index_restaurant.html',
                      context={'id': restaurant[0].rId, 'name': restaurant[0].rName, 'addr': restaurant[0].rAddr,
                               'tel': restaurant[0].rTel, 'dysy': restaurant[0].dysy,
                               'name1': name1, 'result_list': result_list,
                               # 'name1_list': name1_list, 'price_list': price_list,
                               # 'result_list1': json.dumps(result_list1),
                               })


def index_administrator(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        admin = models.Administrator.objects.filter(aId=number)
        return render(request, 'index_administrator.html', context={'name': admin[0].aName, 'gender': admin[0].aGender,
                                                                    'id': admin[0].aId, 'age': admin[0].aAge})


def aitest(number):
    userId = number
    result = models.Order.objects.filter(status='已完成').order_by('userId')
    menus = models.Menu.objects.values_list('mId', flat=True)
    users = models.User.objects.values_list('uId', flat=True)
    menus_number = len(menus)
    users_number = len(users)
    matrixdata = [[0] * menus_number for i in range(users_number)]
    response = []
    for item in result:
        transferitem = model_to_dict(item)
        a = list(menus).index(transferitem['menuId'])
        b = list(users).index(transferitem['userId'])
        matrixdata[b][a] = int(transferitem['evaluation'])
        # matrixdata.append([transferitem['userId'],transferitem['menuId'],transferitem['evaluation']])

    def loadExData2():
        return matrixdata

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
    recomaandations = recommand(myMat, 1)
    for item in recomaandations:
        index = list(menus)[item[0]]
        element = models.Menu.objects.get(mId=index)
        response.append(model_to_dict(element))
    return response


def recommand(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.User.objects.filter(uId=number)
        recommandations = models.Order.objects.filter(userId=number, status='已完成').values('menuId').annotate(
            au=Count('menuId')).order_by('-au')
        recommandmenu1 = []
        recommandmenu2 = aitest(number)
        for item in recommandations:
            Object = model_to_dict(models.Menu.objects.get(mId=item['menuId']))
            recommandmenu1.append(Object)
        recommandmenu1 = recommandmenu1[0:6]
    return render(request, 'recommand.html',
                  context={'name': user[0].uName, 'number': number,
                           'recommandations': recommandmenu1, 'AIrecommandations': recommandmenu2})


def history(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.User.objects.filter(uId=number)
        order = models.Order.objects.filter(userId_id=number)
        return render(request, 'history.html', context={'name': user[0].uName, 'number': number,
                                                        'order': order})


def restaurant_entrance(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.User.objects.filter(uId=number)
        menu = models.Menu.objects.all()
        restaurant = models.Restaurant.objects.all()
        if request.method == 'GET':
            return render(request, 'restaurant_entrance.html',
                          context={'name': user[0].uName, 'number': number, 'menu': menu,
                                   'restaurant': restaurant})


app_private_key_string = open("Platform/keys/my_private_key.pem").read()
alipay_public_key_string = open("Platform/keys/alipay_public_key.pem").read()

alipay = AliPay(
    appid="2021000116687928",
    app_notify_url='http://127.0.0.1:8000/checkPay/',  # 默认回调url
    app_private_key_string=app_private_key_string,
    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    alipay_public_key_string=alipay_public_key_string,
    sign_type="RSA2",  # RSA 或者 RSA2
    debug=True  # 默认False
)


def reserve(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.User.objects.filter(uId=number)
        if request.method == 'GET':
            rId = request.GET.get('rId')
            rName = models.Restaurant.objects.filter(rId=rId)
            for i in rName:
                temp = i.rName
            rName = temp
            menu = models.Menu.objects.filter(restaurantId=rId)
            return render(request, 'reserve.html',
                          context={'name': user[0].uName, 'number': number, 'menu': menu, 'rName': rName})
        elif request.method == 'POST':
            amount = 0
            for i in models.Menu.objects.all():
                quan = request.POST.get(i.mId)
                if quan:
                    quan = int(quan)
                    if quan > 0:
                        print(i.mId, ':', quan)
                        amount += i.price * quan
                        # models.Menu.objects.create(oTime=datetime.datetime.now(),number=quan,money=quan*i.price,status='处理中',userId=number,menuId=i.mId)
            if amount > 0:
                import uuid
                subject = "饥肠辘辘订单支付"
                # 获取扫码支付请求参数
                order_string = alipay.api_alipay_trade_page_pay(
                    out_trade_no=str(uuid.uuid1()),
                    total_amount=amount,
                    subject=subject,
                    return_url='http://127.0.0.1:8000/checkPay/',
                    notify_url='http://127.0.0.1:8000/checkPay/'
                )
                # 获取扫码支付的请求地址
                url ='https://openapi.alipaydev.com/gateway.do?' + order_string
                return HttpResponseRedirect(url)


def checkPay(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        user = models.User.objects.filter(uId=number)
        print(request)
        data = request.dict()
        signature = data.pop("sign")
        # verification
        success = alipay.verify(data, signature)
        if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            return HttpResponse('支付成功！')
        return HttpResponse('支付失败！')


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
            order = models.Order.objects.filter(oId=courseid_deleted)
            money = order[0].money
            rid = order[0].menuId.restaurantId.rId
            models.Order.objects.filter(oId=courseid_deleted).update(status='已完成')
            models.Order.objects.filter(oId=courseid_deleted).update(status='已完成')
            models.Restaurant.objects.filter(rId=rid).update(dysy=F('dysy') + money)
            messages.success(request, '订单已发货！')
            return redirect('/handle_current/')


def new_activities(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        restaurant = models.Restaurant.objects.filter(rId=number)
        activities = models.Activity.objects.filter(restaurantId=number)
        if request.method == 'GET':
            return render(request, 'new_activities.html', context={'activities': activities})
        else:
            # discount = request.POST.get('discount')
            # d = int(discount)
            # print(d)
            # models.Menu.objects.filter(restaurantId=number).update(price=F('price') * d / 10)
            # messages.success(request, '新建成功！')

            # restaurantId = request.POST.get('restaurantId')
            return redirect('/activities_submit/')


def activities_submit(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        restaurant = models.Restaurant.objects.filter(rId=number)
        if request.method == 'GET':
            return render(request, 'activities_submit.html',
                          context={'restaurantId': number})
        else:
            restaurant_Id = number
            name = request.POST.get('name')
            start = request.POST.get('start')
            end = request.POST.get('end')
            discount = request.POST.get('discount')
            d = int(discount)

            new_Activity = models.Activity()
            new_Activity.name = name
            new_Activity.start = start
            new_Activity.end = end
            new_Activity.discount = discount
            new_Activity.restaurantId = restaurant[0]
            new_Activity.save()

            models.Menu.objects.filter(restaurantId=restaurant_Id).update(price=F('price') * d / 10)
            return redirect('/new_activities/')


def edit_menu(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        menu = models.Menu.objects.filter(restaurantId=number)

        if request.method == 'GET':
            return render(request, 'edit_menu.html', context={'menu': menu})
        else:
            if 'delete' in request.POST:
                temp_id = request.POST.get('delete')
                models.Menu.objects.filter(mId=temp_id).first().delete()
                return redirect('/edit_menu/')
            else:
                temp_id = request.POST.get('temp_id')
                temp = models.Menu.objects.filter(mId=temp_id)
                return redirect('/menu_submit/?temp_id=' + temp_id)


def menu_submit(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        restaurant = models.Restaurant.objects.filter(rId=number)

        if request.method == 'GET':
            temp_id = request.GET.get('temp_id')
            menu_id = temp_id
            temp = models.Menu.objects.filter(mId=temp_id)
            print(menu_id)
            return render(request, 'menu_submit.html',
                          context={'temp': temp})
        else:
            temp_id = request.POST.get('temp_id')
            name = request.POST.get('name')
            price = request.POST.get('price')
            image = request.FILES.get('image')
            infor = request.POST.get('infor')

            menu_id = request.POST.get('menu_id')
            models.Menu.objects.filter(mId=menu_id).first().delete()

            new_Menu = models.Menu()
            new_Menu.mId = temp_id
            new_Menu.mName = name
            new_Menu.price = price
            new_Menu.restaurantId = restaurant[0]
            new_Menu.image = image
            new_Menu.infor = infor
            new_Menu.save()

            return redirect('/edit_menu/')


def menu_add(request):
    if not request.session.get('islogin', None):
        return redirect('/login/')
    else:
        number = request.session.get('number')
        restaurant = models.Restaurant.objects.filter(rId=number)
        if request.method == 'GET':
            return render(request, 'menu_add.html',
                          context={})
        else:
            temp_id = request.POST.get('mid')
            name = request.POST.get('name')
            price = request.POST.get('price')
            image = request.FILES.get('image')
            infor = request.POST.get('infor')

            new_Menu = models.Menu()
            new_Menu.mId = temp_id
            new_Menu.mName = name
            new_Menu.price = price
            new_Menu.restaurantId = restaurant[0]
            new_Menu.image = image
            new_Menu.infor = infor
            new_Menu.save()

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
        image = request.FILES.get('image')
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
            new_tmp_res.image = image
            new_tmp_res.save()

            messages.success(request, '提交成功，管理员将在12小时内审核，请耐心等待！')
            return redirect('/login/')

        else:
            messages.error(request, '请正确填写注册信息！')
            return redirect('/restaurant_register/')
