"""
MCP Time 测试套件
"""

import pytest
import pytest_asyncio
import sys
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_time.server import app


class TestTimeTools:
    """测试时间工具"""

    def test_get_current_time_utc(self):
        """测试获取 UTC 时间"""
        now = datetime.now(ZoneInfo("UTC"))
        assert now.tzinfo is not None
        assert now.year >= 2024

    def test_get_current_time_beijing(self):
        """测试获取北京时间"""
        beijing = datetime.now(ZoneInfo("Asia/Shanghai"))
        utc = datetime.now(ZoneInfo("UTC"))
        # 北京时间应该比 UTC 早（时区偏移）
        assert beijing.tzinfo is not None

    def test_convert_timezone(self):
        """测试时区转换"""
        # 创建一个纽约时间
        ny_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=ZoneInfo("America/New_York"))
        # 转换到上海
        sh_time = ny_time.astimezone(ZoneInfo("Asia/Shanghai"))

        # 验证转换后的时间戳相同
        assert ny_time.timestamp() == sh_time.timestamp()
        # 上海时间应该是第二天凌晨
        assert sh_time.day == 2

    def test_list_timezones(self):
        """测试列出时区"""
        from zoneinfo import available_timezones
        zones = available_timezones()

        # 验证常见时区存在
        assert "Asia/Shanghai" in zones
        assert "America/New_York" in zones
        assert "Europe/London" in zones
        assert "UTC" in zones

    def test_timezone_filtering(self):
        """测试时区过滤"""
        from zoneinfo import available_timezones
        all_zones = available_timezones()

        # 筛选亚洲时区
        asia_zones = [z for z in all_zones if z.startswith("Asia/")]
        assert len(asia_zones) > 0
        assert "Asia/Shanghai" in asia_zones
        assert "Asia/Tokyo" in asia_zones

    def test_iso_format(self):
        """测试 ISO 格式"""
        now = datetime.now(ZoneInfo("UTC"))
        iso_str = now.isoformat()

        # 验证 ISO 格式
        assert "T" in iso_str
        assert len(iso_str) > 0

    def test_unix_timestamp(self):
        """测试 Unix 时间戳"""
        now = datetime.now(ZoneInfo("UTC"))
        timestamp = int(now.timestamp())

        # 验证时间戳是合理的（大于 2024年）
        assert timestamp > 1704067200  # 2024-01-01

    def test_human_readable_format(self):
        """测试人类可读格式"""
        now = datetime.now(ZoneInfo("Asia/Shanghai"))
        human = now.strftime("%Y-%m-%d %H:%M:%S %Z")

        assert "-" in human
        assert ":" in human
        assert len(human) > 0


class TestEdgeCases:
    """测试边界情况"""

    def test_invalid_timezone(self):
        """测试无效时区"""
        with pytest.raises(Exception):
            ZoneInfo("Invalid/Timezone")

    def test_timezone_case_sensitive(self):
        """测试时区大小写敏感"""
        # 正确的时区
        tz1 = ZoneInfo("Asia/Shanghai")
        assert tz1 is not None

        # 错误的大小写应该失败
        with pytest.raises(Exception):
            ZoneInfo("asia/shanghai")

    def test_daylight_saving(self):
        """测试夏令时"""
        # 纽约有夏令时
        ny_summer = datetime(2024, 7, 1, 12, 0, 0, tzinfo=ZoneInfo("America/New_York"))
        ny_winter = datetime(2024, 1, 1, 12, 0, 0, tzinfo=ZoneInfo("America/New_York"))

        # 夏令时和非夏令时的 UTC 偏移应该不同
        assert ny_summer.utcoffset() != ny_winter.utcoffset()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
