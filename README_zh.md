# FastAPI Leads Service

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-green.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一个基于FastAPI开发的现代化Leads（潜在客户）管理系统，支持简历文件上传、邮件通知和状态跟踪。采用异步架构，专为高性能和高并发场景设计。

## ✨ 特性

- 🚀 **高性能异步API** - 基于FastAPI和asyncio，支持高并发请求
- 📁 **文件上传支持** - 安全处理简历PDF文件上传和存储
- 📧 **智能邮件通知** - 自动发送确认邮件和内部通知
- 🗄️ **灵活数据存储** - 支持SQLite和PostgreSQL等数据库
- 🔒 **安全设计** - 内置输入验证和错误处理
- 📊 **状态管理** - 完整的lead状态跟踪系统
- 🏗️ **模块化架构** - 清晰的分层设计，便于维护和扩展
- 🛠️ **开发友好** - 自动API文档生成和热重载支持

## 🏗️ 技术栈

- **框架**: FastAPI - 现代异步Web框架
- **数据库ORM**: SQLAlchemy 2.0 - 强大的数据库抽象层
- **数据验证**: Pydantic - 数据模型和验证
- **异步文件处理**: aiofiles - 异步文件操作
- **邮件服务**: aiosmtplib - 异步SMTP客户端
- **服务器**: Uvicorn - ASGI服务器
- **配置管理**: Pydantic Settings - 环境变量管理

## 📋 系统要求

- Python 3.8+
- SQLite 3.0+ (默认) 或 PostgreSQL (可选)

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/Rikiz/alma-backend-project.git
cd fastapi-leads
```

### 2. 创建conda环境

```bash
conda create -n fastapi-leads python=3.8
conda activate fastapi-leads
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量 (可选)

创建 `.env` 文件：

```env
# 数据库配置
DATABASE_URL=sqlite:///leads.db

# 文件上传配置
UPLOAD_DIR=./uploads

# SMTP邮件配置 (可选)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@yourdomain.com
ATTORNEY_EMAIL=attorney@yourdomain.com

# 日志配置
LOG_LEVEL=INFO
```

### 5. 启动服务

```bash
# 开发模式 (带热重载)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 或使用便捷脚本
./run.sh
```

访问 http://localhost:8000/docs 查看自动生成的API文档。

## 📚 API 文档

### 健康检查

- **GET** `/health` - 服务健康检查

### 公开接口 (Public APIs)

#### 创建Lead
- **POST** `/public/create_leads`
- **描述**: 提交新的潜在客户信息
- **请求体**: `multipart/form-data`
  - `first_name` (string, required): 名
  - `last_name` (string, required): 姓
  - `email` (string, required): 邮箱地址
  - `resume` (file, optional): 简历文件 (PDF)

**cURL 示例**:
```bash
curl -X POST "http://localhost:8000/public/create_leads" \
  -F "first_name=John" \
  -F "last_name=Doe" \
  -F "email=john.doe@example.com" \
  -F "resume=@resume.pdf"
```

**响应**:
```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "resume_path": "/uploads/abc123.pdf",
  "state": "PENDING",
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T10:00:00"
}
```

#### 更新Lead
- **PUT** `/public/update_leads/{lead_id}`
- **描述**: 更新现有lead的信息
- **参数**: `lead_id` (integer, path)
- **请求体**: `multipart/form-data`
  - `first_name` (string, optional): 名
  - `last_name` (string, optional): 姓
  - `resume` (file, optional): 新简历文件

### 内部接口 (Internal APIs)

#### 获取所有Leads
- **GET** `/internal/leads`
- **参数**:
  - `skip` (integer, query, default=0): 跳过的记录数
  - `limit` (integer, query, default=100): 返回的最大记录数

#### 获取单个Lead
- **GET** `/internal/leads/{lead_id}`
- **参数**: `lead_id` (integer, path)

#### 更新Lead状态
- **PATCH** `/internal/leads/{lead_id}/state`
- **描述**: 更新lead的跟进状态
- **请求体**:
```json
{
  "state": "REACHED_OUT"
}
```

**可用状态**: `PENDING`, `REACHED_OUT`

#### 删除Lead
- **DELETE** `/internal/leads/{lead_id}`
- **描述**: 删除指定的lead记录

## 🗂️ 项目结构

```
fastapi-leads/
├── app/
│   ├── api/           # API路由定义
│   │   ├── public.py  # 公开接口
│   │   └── internal.py # 内部接口
│   ├── core/          # 核心配置
│   │   └── config.py  # 应用配置
│   ├── models/        # 数据模型
│   │   ├── models.py  # SQLAlchemy模型
│   │   ├── schemas.py # Pydantic模式
│   │   └── enums.py   # 枚举定义
│   ├── services/      # 业务服务层
│   │   ├── email_service.py    # 邮件服务
│   │   └── storage_service.py  # 文件存储服务
│   ├── server/        # 数据访问层
│   │   └── lead_dao.py # Lead数据访问对象
│   └── database/      # 数据库配置
│       └── db.py
├── uploads/           # 文件上传目录
├── alembic/           # 数据库迁移 (可选)
├── .env              # 环境变量配置
├── .gitignore        # Git忽略文件
├── main.py           # 应用入口
├── requirements.txt  # Python依赖
├── run.sh           # 启动脚本
└── README.md        # 项目文档
```

## ⚙️ 配置选项

### 必需配置

| 变量 | 默认值 | 描述 |
|------|--------|------|
| `DATABASE_URL` | `sqlite:///leads.db` | 数据库连接URL |
| `UPLOAD_DIR` | `./uploads` | 文件上传目录 |

### 可选配置

| 变量 | 默认值 | 描述 |
|------|--------|------|
| `SMTP_HOST` | - | SMTP服务器主机 |
| `SMTP_PORT` | - | SMTP服务器端口 |
| `SMTP_USER` | - | SMTP用户名 |
| `SMTP_PASSWORD` | - | SMTP密码 |
| `FROM_EMAIL` | - | 发件人邮箱 |
| `ATTORNEY_EMAIL` | - | 律师邮箱 (接收内部通知) |
| `LOG_LEVEL` | `INFO` | 日志级别 |

## 📧 邮件通知系统

当创建新lead时，系统会自动发送两封邮件：

1. **客户确认邮件**: 发送给lead本人，确认收到申请
2. **内部通知邮件**: 发送给配置的律师邮箱，包含lead详细信息

邮件功能需要完整的SMTP配置才会启用。

## 🔧 开发指南

### 运行测试

```bash
# 安装测试依赖
pip install pytest

# 运行测试
pytest
```

### 数据库迁移 (使用Alembic)

```bash
# 初始化迁移
alembic init alembic

# 创建迁移
alembic revision --autogenerate -m "Initial migration"

# 应用迁移
alembic upgrade head
```

### 代码格式化

```bash
# 安装开发依赖
pip install black isort flake8

# 格式化代码
black .
isort .

# 检查代码质量
flake8 .
```

## 🚀 部署

### 使用Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 生产环境配置

```bash
# 使用生产WSGI服务器
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🔍 故障排除

### 常见问题

1. **数据库连接错误**
   - 检查 `DATABASE_URL` 配置
   - 确保数据库文件存在且有写权限

2. **文件上传失败**
   - 检查 `UPLOAD_DIR` 目录存在且有写权限
   - 验证文件大小限制

3. **邮件发送失败**
   - 检查SMTP配置完整性
   - 验证邮箱凭据和服务器设置

4. **端口占用**
   ```bash
   # 查找占用8000端口的进程
   lsof -i :8000
   # 或使用不同端口
   uvicorn app.main:app --port 8001
   ```

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 代码规范

- 使用 `black` 进行代码格式化
- 使用 `isort` 整理导入语句
- 遵循PEP 8 规范
- 为新功能添加适当的测试

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持

如有问题或建议，请：

- 提交 [GitHub Issue](https://github.com/Rikiz/alma-backend-project/issues)
- 查看 [API 文档](http://localhost:8000/docs) (运行服务后)
- 查看 [交互式API文档](http://localhost:8000/redoc) (运行服务后)

---

**Happy coding! 🚀**
