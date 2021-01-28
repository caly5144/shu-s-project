# shu-s-project

雁陎的各种小项目合集，一般用python编写

## [雁陎工具图形界面](https://github.com/caly5144/shu-s-project/tree/master/gui)

主要是下面项目的GUI图形界面，直接`python main.py`即可打开。目前只写了词云图生成

详细见：https://www.sitstars.com/archives/83/

## [词云图生成](https://github.com/caly5144/shu-s-project/tree/master/wordcloud)

可生成不同样式（方形、圆形、自定义），不同颜色、不同大小、不同字体、不同分词模式的词云图。

具体参数见/wordcloud/config.txt

详细见：https://www.sitstars.com/archives/33/

## [谷歌云盘目录markdown转换器](https://github.com/caly5144/shu-s-project/tree/master/gdindex)

一个用于生成gd指定目录下所有文件夹（不包括文件）的markdown格式文件，可传至gd网盘下，间接解决[goindex](https://github.com/donwa/goindex)搜索问题。

请提前挂载gd到你的电脑中（rclone，raidrive皆可，但推荐使用[官方filestream](https://dl.google.com/drive-file-stream/googledrivefilestream.exe)，对我来说唯一一个不卡而且无需全局代理的挂载工具）。

详细见：https://www.sitstars.com/archives/34/

## [markdown图片链接自动替换](https://github.com/caly5144/shu-s-project/tree/master/markdown%E5%9B%BE%E7%89%87%E9%93%BE%E6%8E%A5%E6%9B%BF%E6%8D%A2)

（仅适用于vnote笔记）自动读取指定文件夹下的md文件，上传md文件中的图片返回并替换链接。

说明见：https://www.sitstars.com/archives/35/

## [百度云ocr识别程序](https://github.com/caly5144/shu-s-project/tree/master/baidu_ocr)

利用百度云的接口，按下特定键后进行截图并识别文字的程序。

说明见：https://www.sitstars.com/archives/38/

## [新冠疫情分析](https://github.com/caly5144/shu-s-project/tree/master/covid)

pandas数据分析实战，具体使用方法参见博客https://www.sitstars.com/archives/79/

## [期权隐含波动率](https://github.com/caly5144/shu-s-project/tree/master/options)

利用tushare自动拉取数据，计算某日所有期权的隐含波动率，并生成波动率微笑图和波动率曲面图。

详细见：https://www.sitstars.com/archives/91/

## [API开发](https://github.com/caly5144/shu-s-project/tree/master/API)

使用fastapi开发，Demo地址：[https://api.yanshu.work](https://api.yanshu.work)，目前有以下几个API：

* 随机二次元图，参见：https://www.sitstars.com/archives/87/
* 检测网址状态
* 查询网址是否被百度收录，参见：https://www.sitstars.com/archives/110/
* 查询ip所在城市，数据源：https://github.com/out0fmemory/qqwry.dat
* 查询访客ip，参见：https://www.sitstars.com/archives/109/
* 查询访客UA

使用方法：

* windows：cd到API目录，输入`python main.py即可`
* Linux：cd到API目录，输入`uvicorn main:app --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips='*'`

## [文本相似度检测](https://github.com/caly5144/shu-s-project/tree/master/text)

给定两个txt文档，检测其相似度。

详见：https://www.sitstars.com/archives/112/



