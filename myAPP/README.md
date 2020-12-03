# 病理信息化系统

## 项目介绍
本项目用于进行病理信息化系统的初步实现，包含了对数据库的增删改查操作，详情请查看[接口及开发文档](链接：https://easydoc.xyz/s/84839459) 。

## 后端框架

[Django REST framework](https://www.django-rest-framework.org/)

基于Python，建议使用anaconda配置运行环境。  

操作详情请查看手册`filesForProject/REST入门`  

环境备份文件为`filesForProject/env_for_demo`，请自行导入
## 文件结构

只标注出了需要更改的文件 

~~~
myAPP  
│
└───api
│   │  admin.py 【可视化的后端数据库管理界面设置】
│   │  models.py 【定义数据库模型】
│   │  serializers.py  【序列化模型字段，用于验证和展示】
│   │  urls.py  【路由，指定访问地址和调用的函数】
│   │  views.py  【具体的后端操作函数】
│   
└───myAPP
    │   settings.py  【后端的设置，包括插件、页面数目、数据库地址及密码等】
    │   urls.py  【全局路由】
~~~

## 代码结构讲解

### models 模型

后端首先要定义模型，如下为`用户详细信息表`。

作用：设置每个表的表名、表项、对表项的限制、外键等等

模型设置的相关字段用法，请查询[文档](https://docs.djangoproject.com/en/3.1/topics/db/models/)

~~~python
class Profile(models.Model):
    """
    用户详细信息表
    """
    Sex_Choice = (
        ('male', '男'),
        ('female', '女')
    )
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_info_of')
    name = models.CharField(max_length=80, blank=True, null=True, default='未命名')
    sex = models.CharField(choices=Sex_Choice, default='male', max_length=10)
    phoneNumber = models.CharField(max_length=80, blank=True, null=True, default='000')
    title = models.CharField(max_length=80, blank=True, null=True, default='主治医师')
    office = models.CharField(max_length=80, blank=True, null=True, default='未分配')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
~~~

### serializers 序列器

用于对前端返回的字段进行验证，然后存储到数据库中；

也用于指定在前端请求数据时，能够返回展示的字段

更多操作请查询文档

~~~python
class UserProfileDetailSerializer(serializers.ModelSerializer):
    """
    Profile序列器
    详细信息
    医生信息表，仅本人可查看
    """
    class Meta:
        model = Profile
        fields = ('id', 'name', 'sex', 'phoneNumber', 'title', 'office',)
        read_only_fields = ('created', 'updated',)
~~~

### views 视图

在此进行代码编写，包含了后端所要处理的绝大部分逻辑操作。

如下为：用户列表获取

​	附加：

​		OrderingFilter，排序功能

​		SearchFilter，搜索功能

​		DjangoFilterBackend，过滤功能

~~~python
class UserListView(generics.ListAPIView):
    """
    用户List获取
    """
    queryset = Profile.objects.all()
    serializer_class = UserProfileListSerializer
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    filter_fields = ('sex',)
    ordering_fields = ('name', 'sex', 'created', 'updated', 'title', 'office',)
    search_fields = ('name',)
    ordering = ('id',)
~~~

view中，规定了相应的获取方法：

`创建、列表、详情、更新`  

[CreateAPIView](https://www.django-rest-framework.org/api-guide/generic-views/#createapiview)
```
Used for **create-only** endpoints.

Provides a post method handler.
```
[ListAPIView](https://www.django-rest-framework.org/api-guide/generic-views/#listapiview)
```
Used for **read-only** endpoints to represent a **collection of model instances**.

Provides a get method handler.
```
[RetrieveAPIView](https://www.django-rest-framework.org/api-guide/generic-views/#retrieveapiview)
```
Used for **read-only** endpoints to represent a **single model instance**.

Provides a get method handler.
```
[DestroyAPIView](https://www.django-rest-framework.org/api-guide/generic-views/#destroyapiview)
```
Used for **delete-only** endpoints for a **single model instance**.

Provides a delete method handler.
```
[UpdateAPIView](https://www.django-rest-framework.org/api-guide/generic-views/#updateapiview)
```
Used for **update-only** endpoints for a **single model instance**.

Provides put and patch method handlers.
```
[ListCreateAPIView](https://www.django-rest-framework.org/api-guide/generic-views/#listcreateapiview)
```
Used for **read-write** endpoints to represent a **collection of model instances**.

Provides get and post method handlers.
```
[RetrieveUpdateAPIView](https://www.django-rest-framework.org/api-guide/generic-views/#retrieveupdateapiview)
```
Used for **read or update** endpoints to represent a **single model instance**.

Provides get, put and patch method handlers.
```
[RetrieveDestroyAPIView](https://www.django-rest-framework.org/api-guide/generic-views/#retrievedestroyapiview)
```
Used for **read or delete** endpoints to represent a **single model instance**.

Provides get and delete method handlers.
```
[RetrieveUpdateDestroyAPIView](https://www.django-rest-framework.org/api-guide/generic-views/#retrieveupdatedestroyapiview)
```
Used for **read-write-delete** endpoints to represent a **single model instance**.

Provides get, put, patch and delete method handlers.
```
### url 路由

规定了某一函数对应的执行地址

~~~python
path('userCreate/', views.UserCreatView.as_view(), name='userCreate'),
path('userList/', views.UserListView.as_view(), name='userList'),	
~~~