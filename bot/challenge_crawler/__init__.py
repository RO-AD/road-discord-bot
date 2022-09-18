
import discord
from discord.ext import commands
from bot.challenge_crawler import crawler


class ChallengeAlertBot(crawler.CrawlerDB, commands.Cog, name='대회 알림 봇'):
    def __init__(self, bot):
        self.bot = bot
        
        self.chall_list = [
            crawler.NhsukCrawler(),
            crawler.KookminUnivCrawler(),
            crawler.LgeRobotContestCrawler(),
            crawler.KiroCrawler(),
        ]

    @commands.command(name='challenge', aliases=['chall', '대회'], description ='대회 현황 명령')
    async def chall(self, ctx, *args):
        for chall in self.chall_list:
            embed = discord.Embed(
                title = "\"{}\" 새로운 소식 알림".format(chall.name),
                description = "(관련대회: {})".format(chall.sub_name),
                color = 0x00cf00
            )
            query = """
                SELECT
                    title, datetime
                FROM {}
                WHERE 
                    is_notice=0 AND target_name=?
            """.format(self.table_name)

            try:
                self.db.execute(query, (chall.name,))
            except:
                print("ERROR :: NO DATABASE!")
                return

            notice_title_list = []
            for row in self.db:
                embed.add_field(
                    name  = row[1],
                    value = row[0],
                    inline = False
                )
                notice_title_list.append(row[0])

            # Activate is_notice
            try:
                for title in notice_title_list:
                    query = """
                        UPDATE {}
                        SET is_notice = 1
                        WHERE
                            title = ? AND target_name = ?
                    """.format(self.table_name)
    
                    self.db.execute(query, (title, chall.name))
    
                self.connection.commit()
            except Exception as err:
                print(err)
                self.connection.rollback()

            # Publish
            if len(notice_title_list) > 0:
                await ctx.send(embed=embed)
        


