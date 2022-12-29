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

  [登录注册 (apipost.cn)](https://console-docs.apipost.cn/preview/1380d4ac60e1c6ff/bd28db2c76532b88?target_id=9a531ed1-69f6-45e0-9145-cb4ac310389f#fcc8514b-84fe-4b35-9f35-395555598c00)

