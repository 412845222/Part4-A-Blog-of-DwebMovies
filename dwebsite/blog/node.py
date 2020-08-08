User模型和权限之间可以通过以下几种方式来进行管理：
1、user.user_permissions.set(permission_list)：直接给定一个权限的列表。
2、user.user_permissions.add(permission,permission,...)：一个个添加权限。
3、user.user_permissions.remover(permission,permission)：一个个删除权限。
4、user.user_permissions.clear()：清除权限
5、user.has_perm('<app_name>.<codename>')：判断是否拥有某个权限
6、user.get_all_permission()：获得所有权限。