## 基于django框架开发的小说分享网站

#### 简介
用户可以分享小说文件，或者分享资源链接。同时也可以创建一个小说页面，等待他人分享

### 文件说明

#### admintool/ 
管理员工具，用于批量创建小说页面

#### check/
验证码生成和验证模块

#### myUpload/
处理异步模块，用于处理小说上传，小说收藏等

#### shuchongwo/
主要模块，用于大部分的页面生成

#### nginx.conf、uwsgi_params
nginx配置文件

#### uwsgi.ini
uwsgi配置文件

#### books.json
起点捉取的一些小说基本资料，用于批量生成第一部分小说页面