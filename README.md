1.第三方包的版本
```requirements.txt
Django==3.2
PyMySQL==0.10.0
```


2.数据库
```sql
127.0.0.1/crm
root:666666
```
3.数据库迁移
```shell script
python manage.py makemigrations
python manage.py migrate
```
**注意**
> 在CRM\crm\crm\__init__.py中添加
```python
import pymysql
pymysql.version_info = (1, 4, 13, "final", 0)
pymysql.install_as_MySQLdb()
```
4.创建超级用户
```shell script
# 设置密码
python manage.py createsuperuser 
# 修改密码
python manage.py changepassword 用户名
```
用户名:jason 邮件:jason@163.com 密码:yyds666666
