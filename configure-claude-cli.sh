#!/usr/bin/env bash
# 自动配置 Claude CLI MCP 服务器

set -e

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "🔧 Claude CLI MCP 自动配置"
echo ""

# Claude CLI 配置文件路径
CLAUDE_DIR="$HOME/.claude"
CONFIG_FILE="$CLAUDE_DIR/settings.json"

echo -e "${BLUE}配置文件路径:${NC}"
echo "  $CONFIG_FILE"
echo ""

# 检查配置目录
if [ ! -d "$CLAUDE_DIR" ]; then
    echo -e "${RED}❌ 错误: Claude CLI 配置目录不存在${NC}"
    echo "请确保已安装 Claude CLI"
    exit 1
fi

# 获取已安装的 MCP 工具列表
echo -e "${BLUE}扫描已安装的 MCP 服务器...${NC}"
MCP_TOOLS=$(uv tool list 2>/dev/null | grep -E "^mcp-" | awk '{print $1}' || echo "")

if [ -z "$MCP_TOOLS" ]; then
    echo -e "${RED}❌ 错误: 没有找到已安装的 MCP 服务器${NC}"
    echo "请先运行: ./install-all.sh"
    exit 1
fi

echo -e "${GREEN}找到以下 MCP 服务器:${NC}"
echo "$MCP_TOOLS" | while read tool; do
    echo "  • $tool"
done
echo ""

# 备份现有配置
if [ -f "$CONFIG_FILE" ]; then
    BACKUP_FILE="${CONFIG_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$CONFIG_FILE" "$BACKUP_FILE"
    echo -e "${YELLOW}📦 已备份现有配置到:${NC}"
    echo "  $BACKUP_FILE"
    echo ""
fi

# 读取现有配置
if [ -f "$CONFIG_FILE" ]; then
    EXISTING_CONFIG=$(cat "$CONFIG_FILE")
else
    EXISTING_CONFIG="{}"
fi

# 生成 MCP 配置
echo -e "${BLUE}生成 MCP 配置...${NC}"

# 使用 Python 来处理 JSON
python3 - "$CONFIG_FILE" "$MCP_TOOLS" "$EXISTING_CONFIG" << 'PYTHON_SCRIPT'
import json
import sys
import os

config_file = sys.argv[1]
mcp_tools = sys.argv[2].strip().split('\n')
existing_config = sys.argv[3]

# 解析现有配置
try:
    config = json.loads(existing_config)
except:
    config = {}

# 确保 mcpServers 键存在
if "mcpServers" not in config:
    config["mcpServers"] = {}

# 为每个 MCP 工具生成配置
for tool in mcp_tools:
    if not tool:
        continue

    tool = tool.strip()
    server_name = tool.replace("mcp-", "")

    # 基本配置
    server_config = {
        "command": tool
    }

    # 针对特定 MCP 添加环境变量
    if tool == "mcp-scholar":
        env = {}
        if os.environ.get("OPENALEX_EMAIL"):
            env["OPENALEX_EMAIL"] = os.environ.get("OPENALEX_EMAIL")
        if os.environ.get("SEMANTIC_SCHOLAR_API_KEY"):
            env["SEMANTIC_SCHOLAR_API_KEY"] = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
        if env:
            server_config["env"] = env

    # 只在不存在时添加（不覆盖用户自定义配置）
    if server_name not in config["mcpServers"]:
        config["mcpServers"][server_name] = server_config

# 写入配置文件
with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print(json.dumps(config, indent=2))
PYTHON_SCRIPT

echo ""
echo -e "${GREEN}✅ 配置已写入:${NC}"
echo "  $CONFIG_FILE"
echo ""

# 显示配置内容
echo -e "${BLUE}当前配置:${NC}"
cat "$CONFIG_FILE" | python3 -m json.tool
echo ""

# 环境变量提示
echo -e "${YELLOW}💡 提示:${NC}"
echo ""
echo "某些 MCP 服务器需要环境变量。你可以："
echo ""
echo "1. 设置环境变量后重新运行此脚本:"
echo "   export OPENALEX_EMAIL='your@email.com'"
echo "   export SEMANTIC_SCHOLAR_API_KEY='your-key'"
echo "   ./configure-claude-cli.sh"
echo ""
echo "2. 或手动编辑配置文件:"
echo "   nano $CONFIG_FILE"
echo ""

# 完成提示
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✨ 配置完成！${NC}"
echo ""
echo -e "${YELLOW}📝 配置文件已更新，无需重启 Claude CLI${NC}"
echo ""
echo "配置的 MCP 服务器:"
echo "$MCP_TOOLS" | while read tool; do
    server_name=$(echo $tool | sed 's/mcp-//')
    echo "  ✅ $server_name ($tool)"
done
echo ""
echo "你现在可以在 Claude CLI 中使用这些 MCP 服务器了！"
echo ""
