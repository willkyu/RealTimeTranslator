# RealTimeTranslator
实时翻译选中区域的文字，使用百度ocr与有道翻译api

## 使用说明
首先注册一个[百度智能云](https://ai.baidu.com)的账号，实名后在控制台中选择文字识别，点击创建应用。填写相关信息后得到一系列**APP_ID**等信息。

在**RealTimeTranslator.exe**文件同一目录下新建**account.ini**文件，填入如下内容：

```
[account]
APP_ID = 2******5
API_KEY = g*****************M
SECRECT_KEY = T*****************************Y
```

三项分别填入之前得到的信息即可。

最后双击**RealTimeTranslator.exe**，根据指示操作即可。