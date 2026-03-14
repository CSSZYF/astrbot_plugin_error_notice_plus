# error_notice_plus

> 基于 [error_notice](https://github.com/DragonEmpery/error_notice) 改进的 AstrBot 插件

屏蔽机器人在群聊或私聊中的错误信息，并将错误信息发送给**指定管理员**，而非所有管理员。

## ✨ 与原插件的区别

| 特性 | error_notice（原版） | error_notice_plus（本插件） |
|------|---------------------|---------------------------|
| 通知对象 | 所有全局管理员 | **仅发送给指定管理员** |
| 管理员配置 | 使用 AstrBot 全局管理员列表 | **插件内独立配置** |
| 自定义错误关键词 | ❌ 不支持 | ✅ 支持自定义扩展 |

## 📦 安装

在 AstrBot 插件管理中搜索 `error_notice_plus` 安装，或通过仓库地址安装：

```
https://github.com/CSSZYF/astrbot_plugin_error_notice_plus
```

## ⚙️ 配置说明

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `Iserror_notice` | bool | `true` | 是否启用错误信息屏蔽与通知 |
| `notify_admin_ids` | list | `[]` | 接收错误通知的指定管理员ID列表（QQ号） |
| `custom_error_keywords` | list | `[]` | 自定义错误关键词列表，用于额外匹配错误消息 |

### 配置示例

- **notify_admin_ids**: `["123456789", "987654321"]` — 仅这两个QQ号会收到错误通知
- **custom_error_keywords**: `["超时", "连接失败", "服务不可用"]` — 除默认关键词外额外匹配这些词

### 默认错误关键词

插件默认检测以下错误关键词（无需配置）：

- `请求失败`
- `错误类型`
- `错误信息`
- `调用失败`
- `处理失败`
- `描述失败`
- `获取模型列表失败`

## 📋 更新日志

### v1.0.0
- 🎉 基于 error_notice v1.0.3 改进
- ✅ 新增指定管理员通知功能，不再发送给所有管理员
- ✅ 新增自定义错误关键词配置
- ✅ 增强日志输出，可追踪通知发送情况

## 📄 致谢

感谢原作者 [DragonEmpery](https://github.com/DragonEmpery) 的 [error_notice](https://github.com/DragonEmpery/error_notice) 插件。
