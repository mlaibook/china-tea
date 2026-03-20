# Collection Governance

本文件只描述 `china-tea` 当前正在使用的内容治理规则，不记录旧系统，不讨论迁移过程。

## 1. Canonical source 规则

### 1.1 文章 source
文章源文件只能位于各自 article collections：

- `_zh_tea`
- `_en_tea`
- `_zh_teaware`
- `_en_teaware`
- `_zh_drinks`
- `_en_drinks`
- `_zh_science`
- `_en_science`
- `_zh_history`
- `_en_history`

`zh/...` / `en/...` 发布路径不是文章 source-of-truth，不能回写文章源文件。

### 1.2 栏目页 source
栏目页源文件只能位于：

- `_zh_section_index`
- `_en_section_index`

这些 collection 当前承载：
- `tea`
- `teaware`
- `drinks`
- `science`
- `history`

`/zh/<section>/index.html` 与 `/en/<section>/index.html` 是 permalink 输出结果，不是栏目页源文件位置。

## 2. 严禁回写发布路径

禁止以下行为：

- 把文章直接写到 `zh/...` 或 `en/...`
- 把栏目页源文件直接写到 `zh/<section>/index.html` 或 `en/<section>/index.html`
- 把发布路径目录当成 source 目录使用

## 3. 首页与栏目页更新规则

如果新文章没有在首页或栏目页正确出现，应优先检查：

- article collection 是否正确
- section-index collection 是否正确
- front matter 是否正确
- `date` / `updated` / `featured` / `index_title` / `index_description` / `thumbnail_*` 是否正确
- include / layout / Liquid 查询是否正确

禁止用以下方式“刷新页面”：

- 手动 touch 多个 index 页面
- 批量重写多个 index 页面
- 手动复制文章链接进栏目页正文
- 把首页或栏目页当缓存文件强行刷新

首页、栏目页的内容变化必须来自：
- article collections
- section-index collections
- metadata
- includes
- layouts
- Liquid 查询逻辑

## 4. 双语内容规则

### 4.1 中文是源稿
中文稿是源稿。英文稿必须翻译、重写并对齐自中文稿。

### 4.2 英文不得脱离中文单独演化
英文稿可以为英语读者补解释，但不能：

- 脱离中文稿单独起题
- 脱离中文稿单独立意
- 脱离中文稿写成另一篇重点不同的文章
- 改变中文稿的核心事实、主线、论点或结论

### 4.3 中文未定稿，不先发英文
如果中文稿尚未定稿，不发布英文稿。

### 4.4 发布前双语对齐检查
发布前必须检查：

- 中英标题主旨对齐
- description 对齐
- section 对齐
- permalink 对齐
- `lang_switch_url` 对齐
- 核心事实与结论对齐
- 章节推进与内容重点对齐

## 5. Collection 文件格式规则

所有新增或批量生成的 collection 文件都必须抽查。

至少检查：
- front matter 正常
- `permalink` 正常
- `lang_switch_url` 正常
- 没有多余引号
- 没有错误转义
- 正文不是整页 HTML 壳
- 没有残留 `\\n` 等序列化垃圾

## 6. 图片规则

### 6.1 先验图，再用图
不能只看文件名、URL、alt 或上下文去猜图片内容，必须确认图片本身是否贴题。

### 6.2 先验类型，再上线
不能只信扩展名。下载后的图片必须确认真实文件类型，防止 HTML、错误页、跳转页或坏资源被误存成图片。

### 6.3 图文同步
换图后要同步检查：
- alt
- caption
- 缩略图 metadata
- 是否影响栏目卡片与首页显示

## 7. 旧脚本治理规则

禁止保留或重新启用会绕开 collections 的旧脚本。尤其禁止这类行为：

- 直接写 `zh/...` / `en/...` 文章源文件
- 直接覆盖 `zh/<section>/index.html` / `en/<section>/index.html`
- 批量刷新 index 页面
- 重新制造发布路径 source

发现此类脚本时，默认动作是：
- 删除
- 停用
- 或明确阻断运行

## 8. 提交与发布规则

站点更新的默认完成标准是：

1. 修改正确的 source 文件
2. 完成必要自检
3. `git add`
4. `git commit`
5. `git push`

只有本地 commit 不算发布完成。

## 9. 默认自检清单

每次发文或改站后，至少确认：

- 文章是否位于正确 article collection
- 栏目页是否位于正确 section-index collection
- 是否误写到 `zh/...` / `en/...`
- permalink 是否保持稳定
- 中英文是否对齐
- collection 文件格式是否正常
- 图片是否真实有效且贴题
- 首页/栏目页是否通过 collections 正常反映新内容
- 是否已完成 commit 与 push
