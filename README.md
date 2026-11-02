# 奶系桌宠 / Milk Pets

一组为 ChatGPT / Codex Work 模式制作的精细 3D 奶黄色桌宠。当前包含奶蛙、奶鸡和奶鼠。

所有新角色由 ImageGen 2 生成动作素材，再经过逐帧拆分、透明抠图、统一缩放、基线校准、方向盲测和最终精灵表校验。仓库不包含原始视频或带水印的参考素材。

## 角色

### 奶蛙 · 原版大笑精修

保留捧肚大笑和笑后弯腰动作，并修正了闭眼笑的眼睛造型。

![奶蛙 8 帧动作长图](pets/naiwa/showcase-strip.png)

![奶蛙动作](pets/naiwa/previews/all-states.gif)

![奶蛙环视](pets/naiwa/previews/look-loop.gif)

### 奶鸡

红色鸡冠、大扇形尾羽、浅绿色眼睛。动作通过翅膀、鸡冠、尾羽与重心表达。

![奶鸡 8 帧动作长图](pets/naiji/showcase-strip.png)

![奶鸡动作](pets/naiji/previews/all-states.gif)

![奶鸡环视](pets/naiji/previews/look-loop.gif)

### 奶鼠

超大圆耳、橙色内耳、浅绿色眼睛和细长尾巴。动作通过耳朵、短手、尾巴与眼神表达。

![奶鼠 8 帧动作长图](pets/naishu/showcase-strip.png)

![奶鼠动作](pets/naishu/previews/all-states.gif)

![奶鼠环视](pets/naishu/previews/look-loop.gif)

## 精灵表规格

- v2：`1536 × 2288`
- 网格：8 列 × 11 行
- 单格：`192 × 208`
- 标准动作：待机、向右移动、向左移动、挥手、跳跃、失败、等待、工作、检查
- 鼠标环视：16 个顺时针方向
- 格式：透明 PNG

每个角色目录包含：

- `spritesheet.png`：可上传的最终精灵表
- `showcase-strip.png`：GitHub 首页展示用的 8 帧横向动作长图
- `pet.json`：角色元数据
- `previews/`：全动作、环视、跳跃和分状态 GIF，以及 MP4 总览
- `qa/`：结构校验、方向图、盲测和质量报告

## 质量检查

奶鸡和奶鼠均通过：

- 73 个必需帧与 15 个透明空格校验
- 跳跃离地与落地基线检查
- 16 向环视语义和连续性检查
- 三位独立审查者的随机 A/B 方向盲测
- ChatGPT Pets 上传前结构校验

## 重新导出预览

需要 Python 3 和 Pillow：

```bash
python tools/render_previews.py pets/naiji/spritesheet.png pets/naiji/previews
```

## 说明

本仓库没有附带开源许可证。角色与素材的使用请遵守相关平台规则和权利要求。
