import os


# 遍历文件夹
def walkFile(path):
    alist = []
    for root, dirs, files in os.walk(path):
        alist.append(root.split('\\')) # 遍历目录并分隔成列表
    return alist

def process(alist):
    path_len = len(alist[0])
    web_list = []
    for items in alist:
        web = items[path_len:len(items)]
        if len(web) == 0 or '【00】YH' in web:  # 排除根目录以及指定目录
            continue
        webtemp = 'zyk.ycyh.ink'+'/'+'/'.join(web) + '/'
        website = webtemp.replace(' ','%20')
        web_list.append([len(web),web[-1],website])  
        # 三个参数，分别为路径深度、最后一级目录名称，站点链接
    return web_list

def web2markdown(web_list):
    handler = open(r'README.md',"w+",encoding = "utf-8")  # 默认README生成在程序目录中
    for web in web_list:
        title_level = web[0]
        if title_level > 3:
            title_level = 0  # 从一级标题开始，三级标题结束，可自行修改
        handler.write('#'*(title_level)+' '+'[' + web[1] + ']' + '(' + web[2] + ')' + '\n'*2)
    handler.close()

def main():
    url = r"G:\我的云端硬盘\00分享文件"  # gd挂载目录
    web2markdown(process(walkFile(url)))
    

if __name__ == '__main__':
    main()