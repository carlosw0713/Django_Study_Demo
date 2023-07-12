from django.contrib import messages
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class  M1(MiddlewareMixin):
    '''中间件1 每次进行http操作会先调用中间件 '''
    def process_request(self,request):

        # 如果没有返回值 也就是返回为 None
        # 如果有返回值 HttpResponse、rende、redirect  不会继续走下去
        print('M1.进来了')
        return  HttpResponse('M1 停止访问！！！')
    def process_response(self,request,response):
        print('M1.走了')
        return response

class  M2(MiddlewareMixin):
    '''中间件2'''
    def process_request(self,request):
        print('M2.进来了')
    def process_response(self,request,response):
        print('M2.走了')
        return response


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 0.排除那些不需要登录就能访问的页面
        #   request.path_info 获取当前用户请求的URL /login/ 和验证码 /image/code/
        if request.path_info in ["/login/", "/image/code/"]:
            return

        # 1.读取当前访问的用户的session信息，如果能读到，说明已登陆过，就可以继续向后走。
        info_dict = request.session.get("info")
        # print(info_dict)
        if info_dict:
            return

        # 2.没有登录过，重新回到登录页面
        messages.error(request, '登录权限过期,请重新登录')
        return redirect('/login/')


