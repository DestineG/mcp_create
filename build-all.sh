#!/usr/bin/env bash
# MCP 批量构建脚本 - 生成 wheel 文件用于分发

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST_DIR="$SCRIPT_DIR/dist-all"

# 颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "📦 开始批量构建 MCP 服务器..."
echo "目录: $SCRIPT_DIR"
echo ""

# 检查 uv 是否安装
if ! command -v uv &> /dev/null; then
    echo -e "${RED}❌ 错误: uv 未安装${NC}"
    exit 1
fi

# 创建统一的 dist 目录
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

# 统计
total=0
success=0
failed=0

# 遍历所有包含 pyproject.toml 的子目录
for dir in "$SCRIPT_DIR"/*/; do
    if [ -f "$dir/pyproject.toml" ]; then
        project_name=$(basename "$dir")
        total=$((total + 1))

        echo -e "${YELLOW}[${total}] 构建: $project_name${NC}"

        cd "$dir"
        if uv build --quiet 2>&1; then
            # 复制生成的文件到统一目录
            if [ -d "$dir/dist" ]; then
                cp "$dir/dist"/*.whl "$DIST_DIR/" 2>/dev/null || true
                cp "$dir/dist"/*.tar.gz "$DIST_DIR/" 2>/dev/null || true
                echo -e "${GREEN}✅ $project_name 构建成功${NC}"
                success=$((success + 1))
            fi
        else
            echo -e "${RED}❌ $project_name 构建失败${NC}"
            failed=$((failed + 1))
        fi
        cd "$SCRIPT_DIR"
        echo ""
    fi
done

# 显示统计信息
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✨ 构建完成！${NC}"
echo "总计: $total 个项目"
echo -e "${GREEN}成功: $success${NC}"
[ $failed -gt 0 ] && echo -e "${RED}失败: $failed${NC}"
echo ""
echo -e "${BLUE}📦 所有构建文件位于: $DIST_DIR${NC}"
echo ""
ls -lh "$DIST_DIR"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 创建安装说明
cat > "$DIST_DIR/INSTALL.md" << 'EOF'
# 批量安装 MCP 服务器

## 方法 1: 逐个安装
```bash
uv tool install mcp_scholar-0.1.0-py3-none-any.whl
# ... 其他包
```

## 方法 2: 批量安装
```bash
for wheel in *.whl; do
    uv tool install "$wheel"
done
```

## 验证安装
```bash
uv tool list
```
EOF

echo ""
echo -e "${GREEN}📝 安装说明已保存到: $DIST_DIR/INSTALL.md${NC}"
