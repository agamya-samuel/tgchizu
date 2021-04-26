from telegram.ext import CommandHandler
from tgchizu import dispatcher, status_reply_dict, DOWNLOAD_STATUS_UPDATE_INTERVAL, status_reply_dict_lock
from tgchizu.helper.telegram_helper.message_utils import *
from time import sleep
from tgchizu.helper.ext_utils.bot_utils import get_readable_message
from telegram.error import BadRequest
from tgchizu.helper.telegram_helper.filters import CustomFilters
from tgchizu.helper.telegram_helper.bot_commands import BotCommands
import threading


def mirror_status(update, context):
    message = get_readable_message()
    if len(message) == 0:
        message = "No active downloads"
        reply_message = sendMessage(message, context.bot, update)
        threading.Thread(target=auto_delete_message, args=(bot, update.message, reply_message)).start()
        return
    index = update.effective_chat.id
    with status_reply_dict_lock:
        if index in status_reply_dict.keys():
            deleteMessage(bot, status_reply_dict[index])
            del status_reply_dict[index]
    sendStatusMessage(update, context.bot)
    deleteMessage(context.bot, update.message)


mirror_status_handler = CommandHandler(BotCommands.StatusCommand, mirror_status,
                                       filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(mirror_status_handler)
