# HR AI Assistant - Claude Code 项目指南

> 本文档为 Claude Code 提供项目上下文，帮助 AI 更好地理解和协助开发。

---

## 项目概述

| 属性 | 说明 |
|------|------|
| **项目名称** | HR AI Assistant（人事办公AI助手） |
| **核心功能** | 基于大模型的简历筛选与评分系统 |
| **团队规模** | 3人应届生小组 |
| **项目周期** | 6周青训项目 |
| **技术路线** | 国产开源大模型优先（DeepSeek/Qwen/GLM） |

---

## 目录结构

```
HR-ai-assistant/
├── backend/                      # 后端服务（FastAPI）
│   ├── app/
│   │   ├── main.py              # 应用入口
│   │   ├── api/v1/              # API 路由层
│   │   │   ├── router.py        # 路由注册
│   │   │   └── endpoints/       # 端点实现
│   │   │       ├── health.py    # 健康检查
│   │   │       ├── llm.py       # LLM 测试
│   │   │       ├── resume.py    # 简历上传（待实现）
│   │   │       ├── parse.py     # 简历解析（待实现）
│   │   │       └── score.py     # 评分打分（待实现）
│   │   ├── core/                # 核心模块
│   │   │   ├── config.py        # 配置管理
│   │   │   ├── exceptions.py    # 异常处理
│   │   │   └── logging.py       # 日志配置
│   │   ├── schemas/             # 数据模型（Pydantic）
│   │   │   ├── common.py        # 通用响应模型
│   │   │   └── resume.py        # 简历相关模型
│   │   └── services/            # 服务层（业务逻辑）
│   │       ├── llm_client.py    # LLM API 封装
│   │       └── file_parser.py   # PDF/Word 文本提取
│   ├── tests/                   # 单元测试
│   ├── uploads/                 # 上传文件存储（待创建）
│   ├── .env                     # 环境变量（不提交）
│   ├── .env.example             # 环境变量模板
│   └── requirements.txt         # Python 依赖
├── docs/                        # 项目文档
└── README.md
```

---

## 技术栈

### 后端
| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.11+ | 运行环境 |
| FastAPI | 0.115.8 | Web 框架 |
| Uvicorn | 0.34.0 | ASGI 服务器 |
| Pydantic | 2.x | 数据校验 |
| httpx | 0.28.1 | 异步 HTTP 客户端 |
| pdfplumber | 0.11.6 | PDF 文本提取 |
| python-docx | 1.1.2 | Word 文本提取 |

### 大模型
| 提供商 | 模型 | 说明 |
|--------|------|------|
| DeepSeek | deepseek-v3.2 | 主力模型 |
| 阿里云百炼 | qwen-turbo/plus | 备选方案 |
| NVIDIA | 免费 API | 备选方案 |

---

## 开发环境

### 启动后端服务

```bash
# 1. 进入后端目录
cd backend

# 2. 激活虚拟环境
source .venv/Scripts/activate    # Windows Git Bash
# 或
.venv\Scripts\activate           # Windows CMD

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 访问地址
- API 文档：http://127.0.0.1:8000/docs
- 健康检查：http://127.0.0.1:8000/api/v1/health

---

## API 端点

| 方法 | 路径 | 功能 | 状态 |
|------|------|------|------|
| GET | `/api/v1/health` | 健康检查 | ✅ 已实现 |
| POST | `/api/v1/llm/test` | LLM 连接测试 | ✅ 已实现 |
| POST | `/api/v1/resume/upload` | 简历上传 | ⏳ 待实现 |
| POST | `/api/v1/parse/extract` | 文本提取 | ⏳ 待实现 |
| POST | `/api/v1/score` | 简历评分 | ⏳ 待实现 |

---

## 核心模块说明

### 1. LLM Client (`services/llm_client.py`)

封装大模型 API 调用，兼容 OpenAI 格式。

**特性**：
- 支持 `system_prompt` + `user_prompt`
- 自动重试（3次，递增退避）
- 连接复用（httpx.AsyncClient）
- 完整异常处理

**使用示例**：
```python
from app.services.llm_client import LLMClient

client = LLMClient()
result = await client.chat(
    prompt="简历原文内容...",
    system_prompt="你是简历解析专家，请提取结构化JSON..."
)
await client.close()
```

### 2. File Parser (`services/file_parser.py`)

提取 PDF/Word 文件中的文本内容。

**使用示例**：
```python
from app.services.file_parser import parse_file

result = parse_file("path/to/resume.pdf", "pdf")
# 返回: {"total_pages": 2, "text": "提取的文本..."}
```

---

## 配置项

环境变量配置在 `.env` 文件中：

```env
# 应用配置
APP_NAME=HR AI Assistant Backend
APP_ENV=dev
APP_HOST=0.0.0.0
APP_PORT=8000

# LLM 配置
LLM_PROVIDER=deepseek
LLM_BASE_URL=https://api.deepseek.com
LLM_API_KEY=your_api_key_here
LLM_MODEL=deepseek-chat
LLM_TIMEOUT_SECONDS=30
```

---

## 项目规划（6周版）

### 模块划分（M0-M7）

| 模块 | 名称 | 功能 | 负责人 | 状态 |
|------|------|------|--------|------|
| M0 | 项目基建 | 前后端骨架、数据库设计、LLM API封装、Git规范 | A+B+C 共建 | ✅ 完成 |
| M1 | 简历接入 | 上传PDF/Word、文件校验、任务创建与状态管理 | C | 🔄 进行中 |
| M2 | 简历解析 | 文本抽取、字段结构化（姓名/学历/年限/技能/项目） | B | 🔄 进行中 |
| M3 | 岗位规则 | JD模板管理、硬性条件定义、权重配置、规则版本化 | A | ⏳ 待开始 |
| M4 | 匹配评分 | 硬筛过滤 + 软性打分 + 排序 | B | ⏳ 待开始 |
| M5 | 解释复核 | 命中/缺失/扣分原因生成，人工复核标记 | B | ⏳ 待开始 |
| M6 | 结果展示 | 候选人列表、筛选条件、导出CSV/Excel | C | ⏳ 待开始 |
| M7 | 评估日志 | 准确率/一致率统计、处理日志、错误追踪 | A | ⏳ 待开始 |

### 六周推进计划

| 周次 | 目标 | 交付物 |
|------|------|--------|
| **第1周** | M0 + M1/M2/M3 起步 | 项目基建、上传链路、解析v0.1、规则v1，打通单份简历最小流程 |
| **第2周** | M2/M3 深化 + M4 初版 | 提升解析准确率，完善规则配置，硬筛+软评分v0.1，支持批量评分 |
| **第3周** | M4 完善 + M5 上线 | 排序和解释能力（命中/缺失/扣分），人工复核标记，可评审结果页 |
| **第4周** | M6 交付 + 端到端联调 | 列表、筛选、导出，全链路联调，MVP演示版 |
| **第5周** | M7 评估与稳定性 | 准确率/一致率指标，日志与错误追踪，规则与算法迭代 |
| **第6周** | 试运行与发布准备 | 试运行验收、性能与异常回归、文档收口，可汇报版本 |

### 成员B（后端）第一周计划

| 日期 | 工作任务 | 状态 |
|------|----------|------|
| 3/2 周一 | 搭建后端基础框架 | ✅ 已完成 |
| 3/3 周二 | 封装大模型API统一调用接口，验证API连通性 | ✅ 已完成 |
| 3/4 周三 | 实现PDF/Word简历文本抽取功能 | 🔄 进行中 |
| 3/5 周四 | 开发AI简历解析功能（结构化数据提取）— 50% | ⏳ 待开始 |
| 3/6 周五 | 完成AI简历解析功能，样本验证与Prompt调优 — 100% | ⏳ 待开始 |
| 3/7 周六 | 开发简历硬性条件过滤与加权打分逻辑 — 50% | ⏳ 待开始 |

---

## 编码规范

### Python 风格
- 遵循 PEP 8 规范
- 类型注解：所有函数参数和返回值
- 文档字符串：公共函数必须有 docstring
- 异步优先：IO 操作使用 async/await

### 命名约定
| 类型 | 规范 | 示例 |
|------|------|------|
| 文件名 | snake_case | `llm_client.py` |
| 类名 | PascalCase | `LLMClient` |
| 函数名 | snake_case | `parse_file()` |
| 常量 | UPPER_SNAKE | `MAX_RETRIES` |
| 私有属性 | _前缀 | `self._client` |

### Git 提交规范
```
<type>: <subject>

类型：
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- refactor: 重构
- test: 测试相关
- chore: 构建/工具
```

---

## 团队分工

| 成员 | 角色 | 主要职责 |
|------|------|----------|
| A | M3 岗位规则 | JD模板、筛选规则、数据库设计 |
| B | M2 简历解析 | 后端核心、LLM封装、文本提取 |
| C | M1/M6 前端 | 前端开发、简历上传、结果展示 |

---

## 注意事项

1. **敏感信息**：`.env` 文件包含 API Key，不要提交到 Git
2. **虚拟环境**：始终在 `.venv` 中安装依赖，避免污染全局
3. **异步编程**：FastAPI 端点使用 `async def`，服务层配合使用
4. **错误处理**：使用 `AppException` 抛出业务异常，统一格式返回

---

## 常用命令

```bash
# 运行测试
pytest

# 格式化代码（推荐安装 black）
black app/

# 查看 API 文档
# 启动服务后访问 http://127.0.0.1:8000/docs
```

---

*最后更新：2026-03-04*
