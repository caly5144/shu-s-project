'''
Author: Dong Xing
Date: 2021-01-15 18:09:15
LastEditors: Dong Xing
LastEditTime: 2021-01-16 01:44:21
Description: 网络状态码字典
'''
HTTP_CODE = {
    200: 'OK',  # 请求处理成功，返回相关信息
    204: 'No Content',  # 请求处理成功，但响应报文没有主题返回
    206: 'Partial Content',  # 客户端进行了范围请求，服务器成功执行请求并返回指定范围的实体内容
    301: 'Moved Permanently',  # 永久性重定向。请求的资源已经被分配到新的url
    302: 'Found',  # 临时性重定向
    304: 'Not Modified',  # 客户端发送附带条件的请求后，服务器允许请求，但内容并没修改，返回304。即客户端可以使用缓存的内容
    400: 'Bad Request',  # 请求报文存在语法错误。需要修正请求报文后再次发送请求
    403: 'Forbidden',  # 请求资源的访问被服务器拒绝。服务器没必要给出拒绝的理由。
    404: 'Not Found',  # 服务器上无法找到被请求的资源
    500: 'Internet Server Error',  # 服务器在执行请求时发生了错误。可能是Web应用存在的 bug 或者临时的障碍
    503: 'Service Unavailable'
}

BAIDU_DICT = {
    200:'该网址已被百度收录！',
    403:'该网址暂未被百度收录！',
    500:'Internet Server Error'
}