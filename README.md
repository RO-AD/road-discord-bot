# road-discord-bot
ROAD 디스코드 봇

# 봇 개발 방법
메인으로 돌아가는 코드는 `app.py` 입니다. 봇을 추가하기 위해서는 Cog 객체로 개발한 뒤에 메인 코드에 해당 Cog 객체를 추가하는 코드를 작성하시면 됩니다.
1. [봇 코드 작성 방법](#봇-코드-작성-방법)
    1. 클래스 생성
    2. 명령 추가
    3. 예시 코드
2. [봇 추가 방법](#봇-추가-방법)


## 봇 코드 작성 방법
봇 코드를 작성하는 방법을 소개합니다. 더욱 다양하고 자세한 내용은 [discordpy 공식문서](!https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html)를 확인하세요.

### 클래스 생성
`discord.ext.commands.Cog`를 상속받는 클래스를 하나 생성합니다.
```python
import discord
from discord.ext import commands

class ChallengeAlertBot(commands.Cog, name='대회 알림 봇'):
    # ...
```
여기서 name 인자는 help 명령 입력 시 봇의 이름으로 사용됩니다.

### 명령 추가
명령은 `discord.ext.commands.command` 데코레이션 함수를 이용하여 세팅할 수 있습니다.
```
@commands.command(name='challenge', aliases=['chall', '대회'], description ='대회 현황 명령')
```
- `name` 인자는 어떤 명령이 들어오면 본 코드를 실행할지에 대한 명시입니다. 위의 경우 `!challenge` 명령 입력 시 함수가 실행됩니다.
- `aliases` 인자는 `name` 외에 추가로 비슷한 명령을 정의하고 싶은 경우 사용하면 됩니다. 위의 경우 `!chall` 및 `!대회` 명령이 같은 함수를 수행합니다.
- `description`은 해당 명령을 나타내는 간단한 한줄 소개를 작성하면 됩니다. HelperBot이 이를 이용해 사용자에게 봇 및 명령 사용법을 소개합니다.

### 예시 코드
```python
import discord
from discord.ext import commands

class ChallengeAlertBot(commands.Cog, name='대회 알림 봇'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='challenge', aliases=['chall', '대회'], description ='대회 현황 명령')
    async def chall(self, ctx, *args):
        await ctx.send("테스트~")
```

## 봇 추가 방법
메인으로 구동되는 클래스는 `app.py` 파일의 `RoadBot` 클래스입니다. 작성한 봇을 import 하셨다면 `RoadBot` 클래스의 `createBot` 메소드 내에 다음과 같이 추가하시면 됩니다.
```python
# /bot/challenge.py 파일에 ChallengeAlertBot Cog 객체를 만든 경우

from bot.challenge import ChallengeAlertBot

class RoadBot:

    # ...

    def createBot(self):

        # ...

        bot.add_cog(ChallengeAlertBot(bot))
```
만약 봇의 도움말에 뜨지 않길 원하신다면(백그라운드 전용) HelperBot보다 아래에서 `add_cog`를 진행해주시면 됩니다.


