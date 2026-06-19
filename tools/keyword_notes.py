from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

# 示例关联配置
KEYWORD = "乐鱼体育"
RELATED_URL = "https://zhmain-leyusports.com.cn"

@dataclass
class KeywordNote:
    """数据类：存储单条关键词笔记"""
    title: str
    content: str
    keyword: str = KEYWORD
    source_url: str = RELATED_URL
    created_at: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict:
        return {
            "keyword": self.keyword,
            "title": self.title,
            "content": self.content,
            "source_url": self.source_url,
            "created_at": self.created_at,
            "tags": self.tags,
        }

    def summary(self, max_len: int = 40) -> str:
        """返回裁剪后的摘要"""
        if len(self.content) > max_len:
            return self.content[:max_len] + "..."
        return self.content


@dataclass
class KeywordNotesCollection:
    """管理多条关键词笔记的集合"""
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def add_notes_from_list(self, items: List[dict]) -> None:
        for item in items:
            note = KeywordNote(
                title=item.get("title", "无标题"),
                content=item.get("content", ""),
                tags=item.get("tags", []),
            )
            self.notes.append(note)

    def filter_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def format_all(self) -> str:
        """将所有笔记格式化为可读字符串"""
        lines = []
        lines.append(f"关键词：{KEYWORD}")
        lines.append(f"关联链接：{RELATED_URL}")
        lines.append(f"笔记总数：{len(self.notes)}")
        lines.append("=" * 50)
        for idx, note in enumerate(self.notes, start=1):
            lines.append(f"[{idx}] {note.title}")
            lines.append(f"    标签：{', '.join(note.tags) if note.tags else '无'}")
            lines.append(f"    时间：{note.created_at}")
            lines.append(f"    摘要：{note.summary()}")
            lines.append("-" * 40)
        return "\n".join(lines)

    def format_tag_summary(self) -> str:
        """按标签分组输出笔记数量统计"""
        tag_count = {}
        for note in self.notes:
            for tag in note.tags:
                tag_count[tag] = tag_count.get(tag, 0) + 1
        lines = [f"关键词：{KEYWORD} 笔记标签统计"]
        lines.append("-" * 30)
        for tag, count in sorted(tag_count.items(), key=lambda x: -x[1]):
            lines.append(f"  {tag}: {count} 条")
        return "\n".join(lines)


def demo_usage() -> None:
    """演示函数：直接运行本文件时展示示例数据"""
    collection = KeywordNotesCollection()

    sample_data = [
        {"title": "乐鱼体育平台介绍", "content": "乐鱼体育是一家提供丰富体育赛事直播和投注服务的在线平台，界面简洁，用户体验良好。", "tags": ["平台", "体育"]},
        {"title": "注册流程说明", "content": "用户可通过官网或App完成注册，需提供基本个人信息并设置安全密码。", "tags": ["注册", "指南"]},
        {"title": "常见问题与客服", "content": "平台提供7x24小时在线客服，常见问题涵盖充值、提现、账号安全等。", "tags": ["客服", "帮助"]},
    ]

    collection.add_notes_from_list(sample_data)

    # 也可以手动添加一条
    manual_note = KeywordNote(
        title="赛事推荐功能",
        content="乐鱼体育提供智能推荐算法，根据用户偏好推送热门赛事。",
        tags=["推荐", "功能"],
    )
    collection.add_note(manual_note)

    print(collection.format_all())
    print()
    print(collection.format_tag_summary())


if __name__ == "__main__":
    demo_usage()