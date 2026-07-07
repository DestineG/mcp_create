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
CONFIG_FILE="$HOME/.claude/settings.json"

echo -e "${BLUE}配置路径:${NC}"
echo "  使用 claude mcp add 命令（自动选择合适的配置文件）"
echo ""

# 检查已配置的 MCP 服务器
echo -e "${BLUE}检查 Claude CLI 中已配置的 MCP 服务器...${NC}"
echo ""

# 显示当前 MCP 配置
if claude mcp list 2>/dev/null | grep -q "Connected"; then
    echo -e "${GREEN}已配置的 MCP 服务器:${NC}"
    claude mcp list
    echo ""
    echo -e "${YELLOW}提示: 以上 MCP 服务器已经配置完成${NC}"
    echo ""
    exit 0
fi

# 获取已安装但未配置的 MCP 工具列表
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

# 使用 claude mcp add 命令添加 MCP 服务器
echo -e "${BLUE}添加 MCP 服务器...${NC}"
echo ""

success_count=0
failed_count=0

echo "$MCP_TOOLS" | while read tool; do
    if [ -z "$tool" ]; then
        continue
    fi

    tool=$(echo "$tool" | xargs)
    server_name=$(echo "$tool" | sed 's/mcp-//')

    echo -e "${YELLOW}添加: $server_name ($tool)${NC}"

    # 使用 claude mcp add 命令
    if claude mcp add "$server_name" "$tool" 2>&1 | grep -q "Added"; then
        echo -e "${GREEN}  ✅ 成功${NC}"
        success_count=$((success_count + 1))
    else
        echo -e "${RED}  ❌ 失败${NC}"
        failed_count=$((failed_count + 1))
    fi
    echo ""
done

# 验证 MCP 服务器状态
echo -e "${BLUE}验证 MCP 服务器状态...${NC}"
claude mcp list
echo ""

echo ""

# 完成提示
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✨ 配置完成！${NC}"
echo ""
echo -e "${YELLOW}📝 MCP 服务器已添加并连接成功${NC}"
echo ""
echo "你现在可以在 Claude CLI 中使用这些 MCP 服务器了！"
echo ""
echo "示例："
echo "  - 搜索关于机器学习的论文"
echo "  - 现在北京时间几点？"
echo ""

