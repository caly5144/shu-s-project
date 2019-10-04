# shu-s-project

雁陎的各种小项目合集，一般用python编写

## [词云图生成](https://yanshu.live/archives/33/)

可生成不同样式（方形、圆形、自定义），不同颜色、不同大小、不同字体、不同分词模式的词云图。

具体参数见/wordcloud/config.txt

## [谷歌云盘目录markdown转换器](https://yanshu.live/archives/34/)

一个用于生成gd指定目录下所有文件夹（不包括文件）的markdown格式文件，可传至gd网盘下，间接解决[goindex](https://github.com/donwa/goindex)搜索问题。

请提前挂载gd到你的电脑中（rclone，raidrive皆可，但推荐使用[官方filestream](https://dl.google.com/drive-file-stream/googledrivefilestream.exe)，对我来说唯一一个不卡而且无需全局代理的挂载工具）。