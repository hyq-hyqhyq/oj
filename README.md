# H.L.L.X SQL - Online -Judge项目

本项目是一个面向数据库课程的在线判题与考试系统，支持题目管理、自动判题、考试管理、社区交流等功能。采用前后端分离架构，便于扩展和维护。

---

## 目录结构

```
oj/
├── front/                  # 前端 Vue 项目目录
│   ├── src/                # 前端源码
│   └── ...                 # 其他前端相关文件
├── imgs/                   # 图片资源文件目录
├── server/                 # 后端 Flask 项目目录
│   ├── models.py           # 数据库模型定义
│   ├── resources.py        # 主要代码，实现各功能
│   ├── config.py           # 配置文件（数据库连接等）
│   ├── app.py              # 主函数，定义API接口
│   ├── permissions.py      # 实现后端接口的权限控制和用户身份校验
│   ├── create_sql.sql      # 数据库定义
│   └── requirements.txt    # 后端依赖包列表
├── README.md               # 项目说明文档
└── Test.md                 # 测试用例文档
```

---

## 快速上手指南

### 1. 后端环境配置与启动

1. **安装依赖**
   ```bash
   cd server
   pip install -r requirements.txt
   ```

2. **启动数据库**
   ```bash
   net start mysql
   ```

3. **配置数据库**
   - 默认使用 SQLite（如需更换请修改 `config.py`）
   - 在你的MySQL中建立数据库`OJ`：
        ```sql
        CREATE DATABASE OJ;
        ```
   - 需要在以下两处地方，填入你的数据库密码：
      - `config.py : Line 19`
      - `resources.py : Line 481 - 482`

4. **启动后端服务**
   ```bash
   python app.py
   ```

### 2. 前端环境配置与启动

1. **安装依赖**
   需安装 Node.js 和 npm/yarn：
   ```bash
   cd ../front
   npm install
   ```
2. **启动前端开发服务器**
   ```bash
   npm run serve
   ```
   前端服务默认运行在 `http://localhost:8080/`

### 3. 访问系统

打开浏览器访问 [http://localhost:8080/](http://localhost:8080/)即可体验全部功能
