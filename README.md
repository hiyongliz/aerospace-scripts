# Aerospace Scripts
我在用的 Aerospace 脚本。

## pin_desktop.py

将指定关键词匹配的窗口移动到目标工作区。

### 使用方法

```bash
./pin_desktop.py <workspace>         # 移动窗口到指定工作区
./pin_desktop.py <workspace> -f      # 移动并跟随焦点
```

### 配置

可通过 `config.json` 自定义匹配关键词：

```json
{
  "keywords": ["WeChat", "钉在桌面上", "| 企业微信          | 企业微信", "图片查看器"]
}
```

若配置文件不存在，使用内置默认关键词。
