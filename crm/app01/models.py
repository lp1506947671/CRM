from django.db import models


# Create your models here.
class Depart(models.Model):
    """部门表"""
    title = models.CharField(verbose_name='部门名称', max_length=32)

    def __str__(self):
        return self.title


class Host(models.Model):
    """主机表"""
    host = models.CharField(verbose_name='主机名', max_length=32)
    ip = models.GenericIPAddressField(verbose_name='IP')

    def __str__(self):
        return self.host


class Role(models.Model):
    """角色"""
    title = models.CharField(verbose_name='角色名称', max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """用户表"""
    my_choices = [(1, '男'), (2, "女")]
    name = models.CharField(verbose_name='姓名', max_length=32)
    age = models.CharField(verbose_name='年龄', max_length=32)
    sex = models.CharField(choices=my_choices, default=1, max_length=32 ,verbose_name='性别')
    email = models.CharField(verbose_name='邮箱', max_length=32)
    depart = models.ForeignKey(verbose_name='部门', to='Depart', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Project(models.Model):
    """项目表"""
    title = models.CharField(verbose_name='项目名称', max_length=32)
