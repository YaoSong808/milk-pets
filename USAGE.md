# 奶系桌宠安装说明

## 快速安装

### Codex：发给你的 Agent

把这段话发给能访问本地文件和 GitHub 的 Agent：

```text
帮我安装奶家生物桌宠：
https://github.com/YaoSong808/milk-pets
```

Agent 读取仓库内的 `AGENTS.md` 后，运行 `python3 tools/install.py`，会安装三只桌宠。只装一只时可指定 `--pet naiwa`、`--pet naiji` 或 `--pet naishu`。安装脚本只使用 Python 标准库，不需要额外依赖；会校验精灵表，并拒绝覆盖不同的已有版本。

安装完成后打开 Codex 的桌宠选择器并启用角色。若列表尚未刷新，可重新打开选择器或重启 Codex。

### ChatGPT Work：上传导入

1. 从 [GitHub Releases](https://github.com/YaoSong808/milk-pets/releases/latest) 下载想要的角色完整包。
2. 解压下载的 ZIP 文件。
3. 打开 ChatGPT / Codex 工作模式中的桌宠功能。
4. 选择创建或上传自定义桌宠。
5. 上传包内的 `spritesheet.png`。
6. 填写角色名称并保存，然后选择启用该桌宠。

## 文件说明

- `spritesheet.png`：可以直接上传的 v2 桌宠精灵表。
- `pet.json`：角色名称、说明和精灵表版本信息。
- `使用说明.md`：当前说明文件。

## 推荐名称

| 文件包 | 推荐名称 |
| --- | --- |
| `milk-frog-v2.zip` | 奶蛙 · 原版大笑精修 |
| `milk-chicken-v2.zip` | 奶鸡 |
| `milk-mouse-v2.zip` | 奶鼠 |

如果桌宠显示异常，请确认上传的是完整的 `1536 × 2288` 透明 PNG，且没有经过聊天软件压缩或重新保存。
