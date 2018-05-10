# 用户模块

---

## 用户

### 1. django自定义用户
用户表增加 `通知属性` 字段，因为公司的主要通讯工具用的是skype，所以这个项目我加的是`skype`，你也可以把它定义成其他字段。

### 2. 账号与AD域控结合(ldap)
使用的是 `django-python3-ldap` 模块，集中用户管理，但是这个模块原本是不能同步用户组数据到oms系统，而这个系统所使用的权限管理是基于用户组做的， 所以必须对其稍作修改，文件 [lday.py](https://github.com/itimor/django-oms/blob/master/ldap.py), 替换 `/to/path/site-packages/django_python3_ldap/ldap.py`, 这样就可以同步用户组信息了， 甚至你还可增加其他字段， 改改脚本一样能同步。


![首页](/images/base/base1.png)

---

## 用户组

这个只是定义了表，数据是从 `ldap` 同步过来的，oms系统的菜单、按钮、部分数据等权限都是围绕它做的。

## 角色

保留字段没有使用，用得着的人可以启用它。


