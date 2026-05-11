# Garmin CN MCP Server

让 Claude Code / AI 助手访问你的 Garmin Connect 中国区（garmin.cn）数据——活动、睡眠、心率、训练负荷等。

## 为什么需要这个项目

2026 年 3 月 Garmin 中国区加了一层 Cloudflare TLS 指纹验证 + Turnstile 挑战，所有 Python requests / curl / curl-cffi 请求全部返回 403。市面上的 Garmin MCP 方案对中国区全线失效。

**这个项目的解法：所有 API 请求都走真正的 Chromium 浏览器。**

```
Claude Code → MCP Server → Playwright Chromium → connect.garmin.cn
                                 ↑
                          真 Chrome TLS 指纹
                          Cloudflare 自动放行
```

## 快速开始

### 前置条件
- Node.js 18+
- Python 3.10+
- [Claude Code](https://claude.ai/code)

### 一键安装

```bash
# 1. 安装依赖 + patch + 注册 MCP
bash setup.sh

# 2. 设置环境变量
export GARMIN_EMAIL=you@example.com
export GARMIN_PASSWORD=your_password

# 3. 登录（会打开浏览器窗口）
python garmin_login.py

# 4. 验证
python check_session.py
```

### 手动安装

```bash
# 安装 MCP server
npm install -g @etweisberg/garmin-connect-mcp

# 安装浏览器
npx playwright install chromium

# Patch 中国区
python patch_cn.py

# 安装 Python 依赖
pip install playwright

# 注册 MCP
claude mcp add garmin-cn -- node "$(npm root -g)/@etweisberg/garmin-connect-mcp/dist/index.js"
```

## 项目文件

| 文件 | 用途 |
|------|------|
| `garmin_login.py` | Playwright 自动登录，生成 session |
| `patch_cn.py` | 把 MCP server 域名从 `.com` 改成 `.cn` |
| `check_session.py` | 检查 session 是否过期 |
| `setup.sh` | 一键安装所有依赖 |
| `CLAUDE.md` | Claude Code 项目记忆 |

## 使用

在 Claude Code 中直接用自然语言：

```
"查我最近 5 次跑步"
"昨晚睡眠怎么样"
"下载今天早上的 FIT 文件"
"对比我 5K PB 和 10K PB 的步频步幅"
```

Claude Code 会自动调用对应的 MCP 工具。

## Session 管理

- Session 保存于 `~/.garmin-connect-mcp/session.json`
- 有效期约 2-6 小时
- 过期后重新运行 `python garmin_login.py`

## 技术细节

### 为什么必须可见浏览器？

Garmin CN 的 Cloudflare Turnstile 会检测 WebGL、canvas 指纹等 浏览器特征。`headless=False` 打开的是真 Chromium，Turnstile 自动放行。Headless 模式会被拦截。

### Patches

`patch_cn.py` 做了三处替换：

```
connect.garmin.com  → connect.garmin.cn
sso.garmin.com      → sso.garmin.cn
connectapi.garmin.com → connectapi.garmin.cn
```

### 认证链路

1. SSO API 登录 → 获取 CASTGC ticket
2. 浏览器导航到 `connect.garmin.cn/app/activities`
3. Cloudflare Turnstile 自动完成
4. SSO 自动重定向（CASTGC 已有效）
5. 提取 CSRF token + JWT_WEB cookie
6. 写入 `session.json`

### API 代理

MCP server 启动时：

1. 启动 Headless Chromium
2. 注入已保存的 cookies
3. 导航到 `connect.garmin.cn/site-status/...` 建立会话
4. 所有后续 API 请求通过 `page.evaluate(fetch('/gc-api/...'))` 发出去

关键：API 请求使用浏览器的 `fetch()`，继承了 Chrome 的真实 TLS 指纹，Cloudflare 不会拦截。

## License

MIT
