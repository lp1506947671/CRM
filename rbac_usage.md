1.将rbac组件拷贝项目并在setting文件中添加如下配置

```python
#注册app
INSTALLED_APPS = [
            ...
            'rbac.apps.RbacConfig'
]
#中间件
MIDDLEWARE = [
        'rbac.middlewares.rbac.RbacMiddleware',
    ]

#添加自动发现URL时,所需要排除的URL
AUTO_DISCOVER_EXCLUDE = [
            '/admin/.*',
            '/login/',
            '/logout/',
            '/index/',
        ]
#需要登录但无需权限的URL
NO_PERMISSION_LIST = [
            '/index/',
            '/logout/',
        ]
#添加无需登录白名单VALID_URL_LIST
VALID_URL_LIST = [
        '/login/',
        '/admin/.*'
    ]

#添加权限和菜单的session key
PERMISSION_SESSION_KEY = "luffy_permission_url_list_key"
MENU_SESSION_KEY = "luffy_permission_menu_key"
```



2.修改所有的from XXX import setting的导入配置



3.业务系统中用户表结构的设计,业务表结构中的用户表需要**继承**rbac中的用户表

rbac/models.py

```python
class UserInfo(models.Model):
            # 用户表
            name = models.CharField(verbose_name='用户名', max_length=32)
            password = models.CharField(verbose_name='密码', max_length=64)
            email = models.CharField(verbose_name='邮箱', max_length=32)
            roles = models.ManyToManyField(verbose_name='拥有的所有角色', to=Role, blank=True) 严重提醒 Role 不要加引号

            def __str__(self):
                return self.name

            class Meta:
                # django以后再做数据库迁移时，不再为UserInfo类创建相关的表以及表结构了。
                # 此类可以当做"父类"，被其他Model类继承。
                abstract = True
```

业务/models.py

```python
class UserInfo(RbacUserInfo):
            phone = models.CharField(verbose_name='联系方式', max_length=32)
            level_choices = (
                (1, 'T1'),
                (2, 'T2'),
                (3, 'T3'),
            )
            level = models.IntegerField(verbose_name='级别', choices=level_choices)

            depart = models.ForeignKey(verbose_name='部门', to='Department')
```

 将业务系统中的用户表的路径写到配置文件setting.py

```python
#将用于在rbac分配权限时,读取业务表中的用户信息
RBAC_USER_MODLE_CLASS = "app01.models.UserInfo"
```



4.权限信息录入,在url中添加rbac的路由分发,注意:必须设置namespace

```python
urlpatterns = [
    url(r'^rbac/', include('rbac.urls', namespace='rbac')),
        ]
```

在url中将rbac用户表的增删改查和修改密码的功能删除

```python
# re_path(r'^user/list/$', user.user_list, name='user_list'),
    # re_path(r'^user/add/$', user.user_add, name="user_add"),
    # re_path(r'^user/edit/(?P<pk>\d+)/$', user.user_edit, name="user_edit"),
    # re_path(r'^user/del/(?P<pk>\d+)/$', user.user_del, name="user_del"),
    # re_path(r'^user/reset/password/(?P<pk>\d+)/$', user.user_reset_pwd, name="user_reset_pwd"),
```

业务逻辑开发,添加新的user的url ,并检查将所有的路由是否都设置一个name,如

```python
url(r'^login/$', account.login, name='login'),
url(r'^logout/$', account.logout, name='logout'),
url(r'^index/$', account.index, name='index'),

url(r'^user/list/$', user.user_list, name='user_list'),
url(r'^user/add/$', user.user_add, name='user_add'),
url(r'^user/edit/(?P<pk>\d+)/$', user.user_edit, name='user_edit'),
url(r'^user/del/(?P<pk>\d+)/$', user.user_del, name='user_del'),
url(r'^user/reset/password/(?P<pk>\d+)/$', user.user_reset_pwd, name='user_reset_pwd'),

url(r'^host/list/$', host.host_list, name='host_list'),
url(r'^host/add/$', host.host_add, name='host_add'),
url(r'^host/edit/(?P<pk>\d+)/$', host.host_edit, name='host_edit'),
url(r'^host/del/(?P<pk>\d+)/$', host.host_del, name='host_del'),
```



5.编写用户登录逻辑,进行权限初始化

```python
from django.shortcuts import render, redirect
from app01 import models
from rbac.service.init_permission import init_permission


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    user = request.POST.get('username')
    pwd = request.POST.get('password')

    user_object = models.UserInfo.objects.filter(name=user, password=pwd).first()
    if not user_object:
        return render(request, 'login.html', {'error': '用户名或密码错误'})

    # 用户权限信息的初始化
    init_permission(user_object, request)

    return redirect('/index/')
```



6.注释rbac的中间件,以及template中的权限校验组件



7.将rbac/migrations目录中的数据库迁移记录删除,包含user的其他app的数据库迁移记录也需要删除



8.连接数据库,导入数据

8.1在用户表中新建用户,例如用户名:唐三,密码:tangsan

```sql
INSERT INTO "main"."host_manage_userinfo"("id", "name", "password", "email", "phone", "level", "depart_id") VALUES (1, '唐三', 'tangsan', 'tangsan@163.com', '123456', 'T1', '1');
```

8.2为rbac_role添加root角色

8.3访问http://127.0.0.1:8000/rbac/multi/permissions/将所有的需要进行权限控制的**待新建的权限列表**,存入到数据库当中

8.4在rbac_menu表插入如下数据

```sql
INSERT INTO "main"."rbac_menu"("id", "title", "icon") VALUES (1, '信息管理', 'fa-envelope-open-o');
INSERT INTO "main"."rbac_menu"("id", "title", "icon") VALUES (2, '用户信息', 'fa-hand-spock-o');
INSERT INTO "main"."rbac_menu"("id", "title", "icon") VALUES (3, '账单管理', 'fa-hand-stop-o');
INSERT INTO "main"."rbac_menu"("id", "title", "icon") VALUES (4, '权限管理', 'fa-hourglass-2');
```

8.5访问rbac_permission添加menu_id,p_id

注意

> 如何使用Navicat设置null值



9.访问http://127.0.0.1:8000/rbac/distribute/permissions/,给root配置所有权限,并给刚新增用户分配root角色

注意 

> 如果存在pid设置不正确则会报错KEYERROR



10.放开rbac的中间件,以及template中的权限校验组件的注释,并进行登录



11.粒度到按钮级别的控制

1. 

```python
{% extends 'layout.html' %}
{% load rbac %}

{% block content %}
    <div class="luffy-container">
        <div class="btn-group" style="margin: 5px 0">

            {% if request|has_permission:'host_add' %}
                <a class="btn btn-default" href="{% memory_url request 'host_add' %}">
                    <i class="fa fa-plus-square" aria-hidden="true"></i> 添加主机
                </a>
            {% endif %}

        </div>
        <table class="table table-bordered table-hover">
            <thead>
            <tr>
                <th>主机名</th>
                <th>IP</th>
                <th>部门</th>
                {% if request|has_permission:'host_edit' or request|has_permission:'host_del' %}
                    <th>操作</th>
                {% endif %}

            </tr>
            </thead>
            <tbody>
            {% for row in host_queryset %}
                <tr>
                    <td>{{ row.hostname }}</td>
                    <td>{{ row.ip }}</td>
                    <td>{{ row.depart.title }}</td>
                    {% if request|has_permission:'host_edit' or request|has_permission:'host_del' %}
                        <td>
                            {% if request|has_permission:'host_edit' %}
                                <a style="color: #333333;" href="{% memory_url request 'host_edit' pk=row.id %}">
                                    <i class="fa fa-edit" aria-hidden="true"></i></a>
                            {% endif %}
                            {% if request|has_permission:'host_del' %}
                                <a style="color: #d9534f;" href="{% memory_url request 'host_del' pk=row.id %}"><i
                                        class="fa fa-trash-o"></i></a>
                            {% endif %}
                        </td>
                    {% endif %}
                </tr>
            {% endfor %}
            </tbody>
        </table>
    </div>

{% endblock %}
```



