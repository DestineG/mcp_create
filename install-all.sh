#!/usr/bin/env bash
# MCP 批量安装脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 是否运行测试（默认开启）
RUN_TESTS=${RUN_TESTS:-true}

echo "🚀 开始批量安装 MCP 服务器..."
echo "目录: $SCRIPT_DIR"
if [ "$RUN_TESTS" = "true" ]; then
    echo "🧪 测试模式: 启用"
else
    echo "⚠️  测试模式: 跳过"
fi
echo ""

# 检查 uv 是否安装
if ! command -v uv &> /dev/null; then
    echo -e "${RED}❌ 错误: uv 未安装${NC}"
    echo "请先安装 uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 统计
total=0
success=0
failed=0
failed_list=()

# 遍历所有包含 pyproject.toml 的子目录
for dir in "$SCRIPT_DIR"/*/; do
    if [ -f "$dir/pyproject.toml" ]; then
        project_name=$(basename "$dir")
        total=$((total + 1))

        echo -e "${YELLOW}[${total}] 安装: $project_name${NC}"

        # 运行测试（如果启用）
        if [ "$RUN_TESTS" = "true" ] && [ -d "$dir/tests" ]; then
            echo -e "${BLUE}  🧪 运行测试...${NC}"
            cd "$dir"
            if uv run pytest -q 2>&1 | grep -q "passed\|PASSED"; then
                echo -e "${GREEN}  ✅ 测试通过${NC}"
            else
                echo -e "${RED}  ❌ 测试失败${NC}"
                failed=$((failed + 1))
                failed_list+=("$project_name (测试失败)")
                cd "$SCRIPT_DIR"
                continue
            fi
            cd "$SCRIPT_DIR"
        fi

        # 安装
        if uv tool install --force "$dir" 2>&1 | grep -q "Installed"; then
            echo -e "${GREEN}✅ $project_name 安装成功${NC}"
            success=$((success + 1))
        else
            echo -e "${RED}❌ $project_name 安装失败${NC}"
            failed=$((failed + 1))
            failed_list+=("$project_name")
        fi
        echo ""
    fi
done

# 显示统计信息
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✨ 安装完成！${NC}"
echo "总计: $total 个项目"
echo -e "${GREEN}成功: $success${NC}"
if [ $failed -gt 0 ]; then
    echo -e "${RED}失败: $failed${NC}"
    echo "失败的项目:"
    for name in "${failed_list[@]}"; do
        echo "  - $name"
    done
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 显示已安装的工具
echo ""
echo "已安装的 MCP 工具:"
uv tool list | grep -E "^[a-z]" || echo "无"

echo ""
echo -e "${BLUE}💡 提示：${NC}"
echo "  • 跳过测试: RUN_TESTS=false ./install-all.sh"
echo "  • 只运行测试: cd mcp-xxx && uv run pytest -v"

