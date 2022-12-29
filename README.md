| 请求方法 | URL                         | 描述         | 参数                   |
| -------- | --------------------------- | ------------ | ---------------------- |
| POST     | register/                   | 注册         | 用户信息               |
| POST     | login/                      | 登入         | username、password     |
| POST     | logout/                     | 注销         | token.refresh          |
| POST     | token/refresh/              | 刷新token    | token.refresh          |
| DEL      | user/del/                   | 用户销户     | password               |
| PUT      | user/:username/new-password | 用户修改密码 | password、old_password |

------

- API文档链接：

https://console-docs.apipost.cn/preview/ed03170c2acf9472/e57b2ee73c8ec10a

