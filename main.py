import re
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.platform import AstrBotMessage
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.provider import LLMResponse
from openai.types.chat.chat_completion import ChatCompletion
import traceback

@register("error_notice_plus", "CSSZYF", "屏蔽机器人的错误信息回复，并发送给指定管理员。", "1.0.0")
class ErrorFilter(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        self.Iserror_notice = self.config.get('Iserror_notice', True)
        # 指定接收通知的管理员ID列表（从插件配置中获取）
        self.notify_admin_ids: list = self.config.get('notify_admin_ids', [])
        # 错误关键词列表（默认内置常见错误词汇）
        self.error_keywords: list = self.config.get('error_keywords', [
            '请求失败', '错误类型', '错误信息', '调用失败',
            '处理失败', '描述失败', '获取模型列表失败'
        ])

    @filter.on_decorating_result()
    async def on_decorating_result(self, event: AstrMessageEvent):
        result = event.get_result()
        if not result:  # 检查结果是否存在
            return

        message_str = result.get_plain_text()
        if self.Iserror_notice and message_str:  # 确保message_str不为空
            if any(keyword in message_str for keyword in self.error_keywords):
                # 获取事件信息
                chat_type = "未知类型"
                chat_id = "未知ID"
                user_name = "未知用户"
                platform_name = "未知平台"
                group_name = "未知群聊"  # 初始化群聊名称

                try:  # 捕获处理事件对象时的潜在异常
                    if event.message_obj:
                        if event.message_obj.group_id:
                            chat_type = "群聊"
                            chat_id = event.message_obj.group_id

                            # 尝试获取群聊名称
                            try:
                                group_info = await event.bot.get_group_info(group_id=chat_id)
                                group_name = group_info.get('group_name', "获取群名失败") if group_info else "获取群名失败"
                            except Exception as e:
                                logger.error(f"获取群名失败: {e}")
                                logger.error(traceback.format_exc())
                                group_name = "获取群名失败"
                        else:
                            chat_type = "私聊"
                            chat_id = event.message_obj.sender.user_id

                        user_name = event.get_sender_name()
                        platform_name = event.get_platform_name()
                    else:
                        logger.warning("event.message_obj is None. Could not get chat details")

                except Exception as e:
                    logger.error(f"Error while processing event information: {e}")
                    logger.error(traceback.format_exc())

                # 给指定管理员发通知（仅发送给插件配置中指定的管理员）
                if self.notify_admin_ids:
                    try:
                        for admin_id in self.notify_admin_ids:
                            admin_id_str = str(admin_id).strip()
                            if admin_id_str.isdigit():
                                # 构建通知消息
                                if chat_type == "群聊":
                                    notify_msg = f"主人，我在群聊 {group_name}（{chat_id}） 中和 [{user_name}] 聊天出现错误了: {message_str}"
                                else:
                                    notify_msg = f"主人，我在和 {user_name}（{chat_id}） 私聊时出现错误了: {message_str}"

                                await event.bot.send_private_msg(
                                    user_id=int(admin_id_str),
                                    message=notify_msg
                                )
                                logger.info(f"已向管理员 {admin_id_str} 发送错误通知")
                            else:
                                logger.warning(f"无效的管理员ID: {admin_id}，已跳过")
                    except Exception as e:
                        logger.error(f"Error while sending message to admin: {e}")
                        logger.error(traceback.format_exc())
                else:
                    logger.info("未配置指定管理员ID，跳过发送错误通知")

                logger.info(f"拦截错误消息: {message_str}")
                event.stop_event()  # 停止事件传播
                event.set_result(None)  # 清除结果
                return  # 确保后续处理不会执行
