

import discord
from discord.ext import commands

HELP_MSG_FORMAT = """
**운영중인 봇 리스트입니다**
```
{bot_list}
```
*각 봇의 세부 도움말은 다음 명령으로 확인하세요*
```
!help <봇 이름>
```
"""

class HelperBot(commands.Cog, name='도움말 봇'):
    def __init__(self, bot):
        self.bot = bot
        self.cogs = bot.cogs
        self.set_basic_message()

    @commands.command(name='help', aliases=['도움말', '사용법'], description ='Help Message')
    async def helper(self, ctx, *args):
        response_msg = ""
        argv = len(args)
        
        if argv == 0:
            response_msg = self.basic_msg
        else:
            bot_name = ' '.join(args)
            response_msg = self.get_bot_detail_message(bot_name)
        
        await ctx.send(response_msg)

    def set_basic_message(self):
        bot_list_description = ''
        for no, bot_name in enumerate(self.bot.cogs.keys()):
            bot_list_description = "{}. {}".format(no + 1, bot_name)

        self.basic_msg = HELP_MSG_FORMAT.format(
                bot_list=bot_list_description)

        return self.basic_msg


    def get_bot_detail_message(self, name):
        msg = ""
        if name in self.cogs.keys():
            msg = "**`{}` 사용법**\n".format(name)
            msg += "```\n"
            subbot = self.cogs[name]
            cmds = subbot.get_commands()
            for cmd in cmds:
                msg += "{0:20s}: {1}\n".format(cmd.name, cmd.description)
            
            msg += "```"
            return msg
        else:
            msg = "요청하신 봇 이름을 찾을 수 없습니다"
            suggest = self.suggest_bot_name(name)
            if len(suggest) > 0:
                msg += "\n*`{}`을 잘못 입력하셨나요?*\n".format('`, `'.join(suggest))

        return msg

    def suggest_bot_name(self, name):
        ''' 비슷한 봇 이름 제안 '''
        similar_bot_list = []
        for bot_name in self.cogs:
            for word in name.split(' '):
                if len(word) > 1 and word in bot_name:
                    similar_bot_list.append(bot_name)
                    break

        return similar_bot_list
            
