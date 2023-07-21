# youdao_note_migration

- 导出有道笔记为markdown到本地
- 导出有道笔记元数据
- 根据元数据修改markdown的创建和更新时间以方便排序

## 功能

- 可将所有笔记（文件）按原格式下载到本地保存为markdown格式
- 更新所有markdown的文件时间

## 使用步骤

### 一、环境准备
### 参考以下链接准备环境以及配置参数
https://github.com/DeppWang/youdaonote-pull#%E4%BD%BF%E7%94%A8%E6%AD%A5%E9%AA%A4

#### 设置脚本参数配置文件 `config.json`

建议使用 [Sublime](https://www.sublimetext.com/3) 等三方编辑器编辑 `config.json`，避免编码格式错误

```json
{
    "local_dir": "",
    "local_dir_meta": "",
    "ydnote_dir": "",
    "smms_secret_token": "",
    "is_relative_path": true
}
```

* `local_dir`：选填，本地存放导出文件的文件夹，不填则默认为当前文件夹
* `local_dir_meta`: 保存xml和json文件提供相关元数据的路径
* `ydnote_dir`：选填，有道云笔记指定导出文件夹名，不填则导出所有文件
* `smms_secret_token`：选填， [SM.MS](https://sm.ms) 的 `Secret Token`（注册后 -> Dashboard -> API Token），用于上传笔记中有道云图床图片到 SM.MS 图床，不填则只下载到本地（`youdaonote-images` 文件夹），`Markdown` 中使用本地链接
* `is_relative_path`：选填，在 MD 文件中图片 / 附件是否采用相对路径展示，不填或 false 为绝对路径，true 为相对路径    


###  二、运行导出脚本

```shell
python pullMD.py # 导出markdown
python pullMeta.py   # 导出元数据
python changeTs.py   # 修改创建和修改时间
```

## 注意事项

1. 如果你自己修改脚本，注意不要将 `cookies.json` 文件 `push` 到 GitHub
2. 如果你不是开发者，可能对上面的命令行操作有所陌生，建议按步骤慢慢操作一遍
3. 请确认代码是否为最新，有问题请先看 [issue](https://github.com/DeppWang/youdaonote-pull/issues?q=is%3Aissue+is%3Aclosed) 是否存在，不存在再提 issue
   ```bash
   git pull origin main  # 更新代码
   ```

## 原理

https://github.com/DeppWang/youdaonote-pull#%E5%8E%9F%E7%90%86

## 感谢（参考）

- [youdaonote-pull](https://github.com/DeppWang/youdaonote-pull)
- [YoudaoNoteExport](https://github.com/wesley2012/YoudaoNoteExport)

## 出发点 

https://github.com/DeppWang/youdaonote-pull#%E5%87%BA%E5%8F%91%E7%82%B9

使用[Obsidian](https://obsidian.md/) + GitHub做笔记和同步数据。手机端，官方教程的Working Copy需要收费，于是用iSH通过手机端shell免费在iOS设备上进行同步。具体可以参考https://forum.obsidian.md/t/mobile-sync-with-git-on-ios-for-free-using-ish/20861

注意：如果在iSH上不想使用SSH（安全隐患？），可以使用GitHub的personal access token进行认证，然后使用https来pull和push笔记到GitHub

## 贡献

欢迎贡献代码，但有几个注意事项：

1. commit 请使用英文；一次 commit 只改一个点；一个 commit 一个 PR
2. 代码注释需要有[中英文空格](https://github.com/sparanoid/chinese-copywriting-guidelines)

