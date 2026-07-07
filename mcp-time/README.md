# MCP Time

一个用于时间和时区工具的 MCP (Model Context Protocol) 服务器。

## 功能特性

- 🌍 **获取当前时间**: 支持任意时区
- 🔄 **时区转换**: 在不同时区之间转换时间
- 📋 **时区列表**: 查看所有可用时区
- ✅ **完整测试**: 包含 11 个单元测试，覆盖所有功能和边界情况

## 安装

```bash
cd mcp-time
uv tool install .
```

## 工具列表

### 1. get_current_time

获取指定时区的当前时间。

**参数**:
- `timezone`: 时区名称（如 'America/New_York', 'Asia/Shanghai'），默认 'UTC'
- `format`: 格式类型 ('iso', 'unix', 'human')，默认 'iso'

**示例**:
```json
{
  "timezone": "Asia/Shanghai",
  "format": "human"
}
```

### 2. convert_timezone

在不同时区之间转换时间。

**参数**:
- `time` (必需): ISO 格式时间
- `from_timezone`: 源时区，默认 'UTC'
- `to_timezone` (必需): 目标时区

**示例**:
```json
{
  "time": "2024-01-01T12:00:00",
  "from_timezone": "America/New_York",
  "to_timezone": "Asia/Shanghai"
}
```

### 3. list_timezones

列出所有可用时区。

**参数**:
- `region`: 按区域筛选（如 'America', 'Asia', 'Europe'）

## 配置

### Claude CLI (推荐)

```bash
claude mcp add time mcp-time
```

## 使用示例

在 Claude CLI 中使用自然语言：

```
"现在北京时间几点？"
"把纽约时间 2024-01-01 12:00 转换成上海时间"
"列出所有亚洲的时区"
```

## 开发

### 运行测试

```bash
# 运行所有测试
uv run pytest -v

# 运行特定测试
uv run pytest tests/test_time.py::TestTimeTools::test_convert_timezone -v
```

### 测试覆盖

项目包含 11 个单元测试：
- 时区操作（UTC、北京、时区转换）
- 时区列表和过滤
- 格式化（ISO、Unix、人类可读）
- 边界情况（无效时区、大小写敏感、夏令时）

## 许可证

MIT
