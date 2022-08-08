#-*- coding:utf-8 -*-

import os
import discord
from bot.helper import HelperBot
from bot.challenge import ChallengeAlertBot

class RoadBot:
    def __init__(self):
        self.prefix  = '!'
        self.token   = self.getToken()
        self.bot     = self.createBot()

    def createBot(self):
        bot = discord.ext.commands.Bot(command_prefix=self.prefix)
        bot.remove_command('help')

        # 봇 리스트
        bot.add_cog(ChallengeAlertBot(bot))

        # HelperBot은 가장 마지막에 추가
        bot.add_cog(HelperBot(bot))

        return bot

    def getToken(self):
        token = os.environ['DISCORD_BOT_TOKEN']
        assert len(token) > 0
        return token

    def run(self):
        self.bot.run(self.token)


if __name__ == "__main__":
    bot = RoadBot()
    bot.run()
