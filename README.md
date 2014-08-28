CaptchaReader
=============

Identify the CAPTCHA of http://xk.fudan.edu.cn

现在对于复旦大学选课系统验证码的识别功能已经开发完成。

本程序处理图片采用了二值化和垂直像素直方图的统计方法分割（其实直接按像素分割效果也很好）进行图片预处理，采用SVM进行图像识别。因此你在测试本程序之前需要下载安装机器学习相关的第三方库[scikit-learn](http://scikit-learn.org/stable/index.html)与用于科学计算的第三方库[numpy](http://www.numpy.org)。

在两次大规模的登录测试（每次测试登录501次）中，程序对于复旦选课系统验证码的识别准确率都达到了100%。

由于本人开发该程序的动机纯粹是因为好玩，而且不想被教务处查水表，所以暂不提供刷课功能。但是识别图片接口已经写好，使用时只需调用

``` python
>>> from Identify import Identify
>>> i = Identify(captcha)
>>> captcha_content = i.captcha_reader()
```

即可得到识别好的验证码字符串。

Model文件夹
---

Model文件夹中存放着几个预处理脚本文件，以下是这些文件的用途：

- `download.py`下载指定数目的验证码到指定文件夹
- `binary.py`将`download.py`下载下来的验证码二值化并储存至指定文件夹
- `splite.py`将`binary.py`中的图片切割成四个字符用以识别
- `classfy.py`可识别`splite.py`处理过的图片并将图片文件名首添加改成识别后字符。例如图片上的字符是「2」，文件名是`0202.png`，那么处理过之后的文件名是`20202.png`
- `generate.py`处理训练集并生成.pkl文件。

Model文件夹下还有配置文件`config.py`，里面设置了预处理脚本文件中读取、写入文件夹的路径，批量下载验证码数目，验证码下载地址这些参数。

字模/训练集
---

字模/训练集我已经上传至`Model/trainset/`文件夹下。其中有2086个字模，每个字模对应的字母都是文件名首字母。

**注意：**程序里我没有做路径检测，如果随意更改路径却不创建相应路径的话程序会直接崩溃。

如果有问题请联系zqguo(at)zqguo.com
