import html
import json
import os
from typing import Optional

from DestinyBot import (
    DEV_USERS,
    OWNER_ID,
    DRAGONS,
    SUPPORT_CHAT,
    DEMONS,
    TIGERS,
    WOLVES,
    dispatcher,
)
from DestinyBot.modules.helper_funcs.chat_status import (
    dev_plus,
    sudo_plus,
    whitelist_plus,
)
from DestinyBot.modules.helper_funcs.extraction import extract_user
from DestinyBot.modules.log_channel import gloggable
from telegram import ParseMode, TelegramError, Update
from telegram.ext import CallbackContext, CommandHandler
from telegram.utils.helpers import mention_html

ELEVATED_USERS_FILE = os.path.join(os.getcwd(), "DestinyBot/elevated_users.json")


def check_user_id(user_id: int, context: CallbackContext) -> Optional[str]:
    bot = context.bot
    if not user_id:
        reply = "That...is a chat! baka ka omae?"

    elif user_id == bot.id:
        reply = "This does not work that way."

    else:
        reply = None
    return reply


# This can serve as a deeplink example.
# disasters =
# """ Text here """

# do not async, not a handler
# def send_disasters(update):
#    update.effective_message.reply_text(
#        disasters, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

### Deep link example ends



@dev_plus
@gloggable
def adddev(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if int(user_id) in DEV_USERS:
        message.reply_text("This member is already a FOUNDING TITAN")

    if user_id in DRAGONS:
        rt += "Requested to promote a COLOSSAL to a FOUNDING TITAN."
        data['sudos'].remove(user_id)
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
        rt += "Requested to promote a ACKERMAN to a FOUNDING TITAN."
        data['supports'].remove(user_id)
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        rt += "Requested to promote a PURE TITAN to a FOUNDING TITAN."
        data['whitelists'].remove(user_id)
        WOLVES.remove(user_id)

    data['devs'].append(user_id)
    DEV_USERS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + "\nSuccessfully set Disaster level of {} to FOUNDING TITAN!".format(
            user_member.first_name))

    log_message = (
        f"#ProDeveloper\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message



@dev_plus
@gloggable
def addsudo(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        message.reply_text("This member is already a COLOSSAL TITAN")
        return ""

    if user_id in DEMONS:
        rt += "Requested to promote a ACKERMAN to COLOSSAL TITAN."
        data['supports'].remove(user_id)
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        rt += "Requested to promote a PURE TITAN to COLOSSAL TITAN."
        data['whitelists'].remove(user_id)
        WOLVES.remove(user_id)

    data['sudos'].append(user_id)
    DRAGONS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + "\nSuccessfully set Disaster level of {} to COLOSSAL TITAN!".format(
            user_member.first_name))

    log_message = (
        f"#SUDO\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message



@sudo_plus
@gloggable
def addsupport(
    update: Update,
    context: CallbackContext,
) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        rt += "Requested to demote this COLOSSAL TITAN to ACKERMAN"
        data['sudos'].remove(user_id)
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
        message.reply_text("This user is already a ACKERMAN.")
        return ""

    if user_id in WOLVES:
        rt += "Requested to Promote this PURE TITAN to ACKERMAN"
        data['whitelists'].remove(user_id)
        WOLVES.remove(user_id)

    data['supports'].append(user_id)
    DEMONS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\n{user_member.first_name} was added as a ACKERMAN!")

    log_message = (
        f"#SUPPORT\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message



@sudo_plus
@gloggable
def addwhitelist(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        rt += "This member is a COLOSSAL TITAN, Demoting to PURE TITAN."
        data['sudos'].remove(user_id)
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
        rt += "This user is ACKERMAN, Demoting to PURE TITAN."
        data['supports'].remove(user_id)
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        message.reply_text("This user is already a PURE TITAN.")
        return ""

    data['whitelists'].append(user_id)
    WOLVES.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt +
        f"\nSuccessfully promoted {user_member.first_name} to a PURE TITAN!")

    log_message = (
        f"#WHITELIST\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message



@sudo_plus
@gloggable
def addtiger(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        rt += "This member is a COLOSSAL TITAN, Demoting to SURVEY CORP."
        data['sudos'].remove(user_id)
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
        rt += "This user is a ACKERMAN, Demoting to SURVEY CORP."
        data['supports'].remove(user_id)
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        rt += "This user is a PURE TITAN, Demoting to SURVEY CORP."
        data['whitelists'].remove(user_id)
        WOLVES.remove(user_id)

    if user_id in TIGERS:
        message.reply_text("This user is already a SURVEY CORP.")
        return ""

    data['tigers'].append(user_id)
    TIGERS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt +
        f"\nSuccessfully promoted {user_member.first_name} to a SURVEY CORP!"
    )

    log_message = (
        f"#TIGER\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message

# FtSasaki adding rmpiro to remove user from {devs}



@dev_plus
@gloggable
def rmdev(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in DEV_USERS:
        message.reply_text("Requested to demote this user to a SUBJECT OF YMIR")
        DEV_USERS.remove(user_id)
        data['devs'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNDEV\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != 'private':
            log_message = "<b>{}:</b>\n".format(html.escape(
                chat.title)) + log_message

        return log_message

    else:
        message.reply_text("This user is not a FOUNDING TITAN!")
        return ""



@dev_plus
@gloggable
def removesudo(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        message.reply_text("Requested to demote this user to a SUBJECT OF YMIR")
        DRAGONS.remove(user_id)
        data['sudos'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNSUDO\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != 'private':
            log_message = "<b>{}:</b>\n".format(html.escape(
                chat.title)) + log_message

        return log_message

    else:
        message.reply_text("This user is not a COLOSSAL TITAN!")
        return ""



@sudo_plus
@gloggable
def removesupport(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in DEMONS:
        message.reply_text("Requested to demote this user to a SUBJECT OF YMIR")
        DEMONS.remove(user_id)
        data['supports'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNSUPPORT\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message

    else:
        message.reply_text("This user is not a ACKERMAN!")
        return ""



@sudo_plus
@gloggable
def removewhitelist(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in WOLVES:
        message.reply_text("Demoting to SUBJECT OF YMIR")
        WOLVES.remove(user_id)
        data['whitelists'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNWHITELIST\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("This user is not a PURE TITAN!")
        return ""



@sudo_plus
@gloggable
def removetiger(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in TIGERS:
        message.reply_text("Demoting to PURE TITAN")
        TIGERS.remove(user_id)
        data['tigers'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNTIGER\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )
        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("This user is not a SURVEY CORP!")
        return ""



@whitelist_plus
def whitelist(update: Update, context: CallbackContext):
    reply = "<b>Known as PURE TITAN 🐺:</b>\n"
    bot = context.bot
    for each_user in WOLVES:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)

            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)



@whitelist_plus
def tigerlist(update: Update, context: CallbackContext):
    reply = "<b>Known as SURVEY CORP :</b>\n"
    bot = context.bot
    for each_user in TIGERS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)



@whitelist_plus
def supportlist(update: Update, context: CallbackContext):
    bot = context.bot
    reply = "<b>Known As ACKERMAN 👹:</b>\n"
    for each_user in DEMONS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)



@whitelist_plus
def sudolist(update: Update, context: CallbackContext):
    bot = context.bot
    true_sudo = list(set(DRAGONS) - set(DEV_USERS))
    reply = "<b>Known As COLOSSAL TITAN:</b>\n"
    for each_user in true_sudo:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)



@whitelist_plus
def devlist(update: Update, context: CallbackContext):
    bot = context.bot
    true_dev = list(set(DEV_USERS) - {OWNER_ID})
    reply = "<b>Overpowered FOUNDING TITAN which made me work:</b>\n"
    for each_user in true_dev:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


__help__ = """
*⚠️ Notice:*
Commands listed here only work for users with special
access are mainly used for troubleshooting, debugging purposes.
Group admins/group owners do not need these commands. 
 ╔ *List all special users:*
 ╠ ✮ `/COLOSSALTITANS` or `/sudolist`*:* Lists all Dragon disasters
 ╠ ✮ `/ACKERMANS` or `/supportlist`*:* Lists all Demon disasters
 ╠ ✮ `/SURVEYCORPS` or `/tigerlist`*:* Lists all Tigers disasters
 ╠ ✮ `/PURETITANS` or `/whitelist`*:* Lists all Wolf disasters
 ╠ ✮ `/FOUNDINGTITANS` or `/devlist`*:* Lists all Dev disastors
 ╠ ✮ `/addcolossaltian` or `/addsudo`*:* Adds a user to Dragon
 ╠ ✮ `/addackerman` or `/addsupport`*:* Adds a user to Demon
 ╠ ✮ `/addsuvercorp` or `/addtiger`*:* Adds a user to Tiger
 ╚ ✮ `/addpuretitan` or `/addwolf`*:* Adds a user to Wolf 
 ╔ *Ping:*
 ╠ ✮ `/ping`*:* gets ping time of bot to telegram server
 ╚ ✮ `/pingall`*:* gets all listed ping times
 ╔ *Broadcast: (Bot owner only)*
 ╠  *Note:* This supports basic markdown
 ╠ ✮ `/broadcastall`*:* Broadcasts everywhere
 ╠ ✮ `/broadcastusers`*:* Broadcasts too all users
 ╚ ✮ `/broadcastgroups`*:* Broadcasts too all groups
 ╔ *Groups Info:*
 ╠ ✮ `/groups`*:* List the groups with Name, ID, members
 ╠    count as a txt
 ╠ ✮ `/leave <ID>`*:* Leave the group, ID must have hyphen
 ╠ ✮ `/stats`*:* Shows overall bot stats
 ╠ ✮ `/getchats`*:* Gets a list of group names the user has 
 ╠    been seen in. Bot owner only
 ╚ ✮ `/ginfo username/link/ID`*:* Pulls info panel for 
       entire group
 ╔ *Access control:* 
 ╠ ✮ `/ignore`*:* Blacklists a user from 
 ╠     using the bot entirely
 ╠ ✮ `/notice`*:* Removes user from blacklist
 ╚ ✮ `/ignoredlist`*:* Lists ignored users
 ╔ *Windows self hosted only:*
 ╠ ✮ `/reboot`*:* Restarts the bots service
 ╚ ✮ `/gitpull`*:* Pulls the repo and then restarts the
       bots service
 ╔ *Chatbot:* 
 ╚ ✮ `/listaichats`*:* Lists the chats the chatmode
       is enabled in
 ╔ *Global Bans:*
 ╠ ✮ `/gban <id> <reason>`*:* Gbans the user,
       works by reply too
 ╠ ✮ `/ungban`*:* Ungbans the user, same usage as gban
 ╚ ✮ `/gbanlist`*:* Outputs a list of gbanned users
Visit @kakashi_bots_support for more information.
"""

DEV_HANDLER = CommandHandler(("adddev", "addfoundingtitan"), adddev)
SUDO_HANDLER = CommandHandler(("addsudo", "addcolossaltitan"), addsudo)
SUPPORT_HANDLER = CommandHandler(("addsupport", "addackerman"), addsupport)
TIGER_HANDLER = CommandHandler(("adddefend", "addsurveycorp"), addtiger)
WHITELIST_HANDLER = CommandHandler(("addmelcr", "addwolf"), addwhitelist)

RMPIRO_HANDLER = CommandHandler(("rmdev", "rmfoundingtitan"), rmdev)
UNSUDO_HANDLER = CommandHandler(("removesudo", "rmcolossaltitan"), removesudo)
UNSUPPORT_HANDLER = CommandHandler(("removesupport", "rmackerman"),
                                   removesupport)
UNTIGER_HANDLER = CommandHandler(("rmcorp"), removetiger)
UNWHITELIST_HANDLER = CommandHandler(("removewhitelist", "rmsubymir"),
                                     removewhitelist)

WHITELISTLIST_HANDLER = CommandHandler(["whitelist", "puretitans"],
                                       whitelist)
TIGERLIST_HANDLER = CommandHandler(["defenders", "tigerlist"], tigerlist)
SUPPORTLIST_HANDLER = CommandHandler(["supportlist", "ackermans"], supportlist)
SUDOLIST_HANDLER = CommandHandler(["sudolist", "colossaltitans"], sudolist)
DEVLIST_HANDLER = CommandHandler(["devlist", "foundingtitans"], devlist)

dispatcher.add_handler(DEV_HANDLER)
dispatcher.add_handler(SUDO_HANDLER)
dispatcher.add_handler(SUPPORT_HANDLER)
dispatcher.add_handler(TIGER_HANDLER)
dispatcher.add_handler(WHITELIST_HANDLER)
dispatcher.add_handler(UNSUDO_HANDLER)
dispatcher.add_handler(UNSUPPORT_HANDLER)
dispatcher.add_handler(UNTIGER_HANDLER)
dispatcher.add_handler(UNWHITELIST_HANDLER)
dispatcher.add_handler(RMPIRO_HANDLER)
dispatcher.add_handler(WHITELISTLIST_HANDLER)
dispatcher.add_handler(TIGERLIST_HANDLER)
dispatcher.add_handler(SUPPORTLIST_HANDLER)
dispatcher.add_handler(SUDOLIST_HANDLER)
dispatcher.add_handler(DEVLIST_HANDLER)

__mod_name__ = "Dɪsᴀsᴛᴇʀs 😈"

__handlers__ = [
    DEV_HANDLER, SUDO_HANDLER, SUPPORT_HANDLER, TIGER_HANDLER, WHITELIST_HANDLER,
    RMPIRO_HANDLER, UNSUDO_HANDLER, UNSUPPORT_HANDLER, UNTIGER_HANDLER, UNWHITELIST_HANDLER,
    WHITELISTLIST_HANDLER, TIGERLIST_HANDLER, SUPPORTLIST_HANDLER,
    SUDOLIST_HANDLER, DEVLIST_HANDLER
]
