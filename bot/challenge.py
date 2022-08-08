
import discord
from discord.ext import commands

class ChallengeAlertBot(commands.Cog, name='대회 알림 봇'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='challenge', aliases=['chall', '대회'], description ='대회 현황 명령')
    async def chall(self, ctx, *args):
        await ctx.send("대회 알림 봇 테스트~")

