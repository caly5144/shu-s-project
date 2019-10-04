import os


# 遍历文件夹
def walkFile(path):
    alist = []
    for root in os.walk(path):
        alist.append(root.split('\\')) # 遍历目录并分隔成列表
    return alist

def process(alist):
    path_len = len(alist[0])
    web_list = []
    for items in alist:
        web = items[path_len:len(items)]
        if len(web) == 0:
            continue
        webtemp = 'zy.ycyh.ink'+'/'+'/'.join(web) + '/'
        website = webtemp.replace(' ','%20')
        web_list.append([len(web),web[-1],website])  
        # 三个参数，分别为路径深度、最后一级目录名称，站点链接
    return web_list

def web2markdown(web_list):
    handler = open(r'README.md',"w+",encoding = "utf-8")
    for web in web_list:
        title_level = web[0]
        if title_level > 3:
            title_level = -1
        handler.write('#'*(title_level+1)+' '+'[' + web[1] + ']' + '(' + web[2] + ')' + '\n'*2)
    handler.close()

def main():
    web2markdown(process(walkFile(r"G:\我的云端硬盘\00分享文件")))
    

if __name__ == '__main__':
    main()