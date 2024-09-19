import discord
# from discord_slash import SlashCommand, SlashContext
import numpy as np
import random
import os
from discord.ext import commands
from discord import app_commands
# from discord_buttons_plugin import *
from datetime import datetime
import asyncio
import tkinter as tk
from dataclasses import dataclass
import string
#import openai_secret_manager
#from notion_client import Client
#from pprint import pprint

intents = discord.Intents.all()
TOKEN = 'MTA5MjQ3MzY4Njk5NDQ2MDY4Mg.GCJ7wF.F8h12j2yC-ZvvR4vPAuzGiagusjRjXwkfgC_QU'

bot = commands.Bot(command_prefix='&', intents=intents)

# buttons = ButtonsClient(client)

# slash = SlashCommand(client, sync_commands=True)

txt_game_started = False
players = []
scores = {}
score_cutline = 100
channel_fulllist = []
Gangjong = False
round_num = 0
# timezone_KST = pytz.timezone('Asia/Seoul')

# keep_alive()  #Server에 무한동작시키는 함수. server.py에 있어요!

# authenticate
'''secrets = openai_secret_manager.get_secret("notion")
notion = Client(auth=secrets["api_key"])


# retrieves the list of to do items from Notion
def get_todo_list():
  db_name = "My Todo List"
  results = notion.databases.query(
    **{
      "database_id": secrets["database_id"],
      "filter": {
        "property": "Name",
        "title": {
          "equals": db_name
        },
      },
    }).get("results")
  pprint(results)
  if len(results) > 0:
    result = results[0]
    to_do_items = result["properties"]["Todo"]["multi_select"]
    return [item["name"] for item in to_do_items]
  else:
    return []'''


#GUI APP을 만들었다. (MINUSIXBOT이 동작할 수 있게?) 그런데 힘들다..... html로 바꾸어야 할 수도?
class App:

  def __init__(self, master):
    self.master = master
    # 텍스트 상자와 버튼을 생성
    self.msg_entry = tk.Entry(master)
    self.msg_entry.pack()
    self.channel_entry = tk.Entry(master)
    self.channel_entry.pack()
    self.btn = tk.Button(master, text='전송', command=self.process_input)
    self.btn.pack()
    self.result_label = tk.Label(master, text='')
    self.result_label.pack()

  async def process_input(self):
    # 텍스트 상자에 입력된 메시지와 채널명을 가져옴
    message = self.msg_entry.get()
    channel_name = self.channel_entry.get()
    # process_input 함수 호출
    result = await process_input(message, channel_name)
    # 결과값을 라벨에 출력
    self.result_label.configure(text=result)


@bot.event
async def on_ready():
  print('봇이 로그인했습니다.')
  await client.tree.sync()
  global channel_fulllist
  channel_fulllist = [
    channel for guild in client.guilds for channel in guild.text_channels
  ]
  # GUI_Process() # 아직은 코드에 문제가 있다! 고치자 > html을 통해 접근 가능하게 하는 것이 편리할 듯 싶다.


@app_commands.command()
async def fruits(interaction: discord.Interaction, fruit: str):
  await interaction.response.send_message(
    f'Your favourite fruit seems to be {fruit}')


def GUI_Process():
  root = tk.Tk()
  app = App(root)
  root.mainloop()


async def process_input(message, channel_name):
  if not message:
    return '메시지를 입력해주세요'

  if not channel_name:
    return '채널을 입력해주세요'

  channel = None

  for guild in client.guilds:
    for channel in guild.text_channels:
      if channel.name == channel_name:
        break
    if channel:
      break

  if not channel:
    return f'Error: Could not find a channel named {channel_name}'

  try:
    await channel.send(message)
    return f'Success: Message sent to {channel.name}'
  except discord.errors.Forbidden:
    return f'Error: I do not have permission to send messages to {channel.name}'
  except:
    return 'Error : Have no Access, or no such channel'


'''
@client.slash_command()
async def ping(ctx):
  await ctx.send('Pong!')
'''
'''
@client.event
async def on_message(message):
    # 새로운 메시지가 작성되었을 때 최근 1개의 메시지를 출력합니다.
    channel = message.channel
    async for message in channel.history(limit=1):
        print(f'{message.channel}: {message.author}: {message.content}')
    
    await client.process_commands(message)
'''


@bot.command()
async def members(ctx):
  online_members = []
  online_bots = []
  for member in ctx.guild.members:
    if member.status == discord.Status.online:
      #online_members.append(member.name + member.status.name)
      if member.bot:
        online_bots.append(member.name)
      else:
        online_members.append(member.name)

  if len(online_members) == 0 and len(online_bots) == 0:
    await ctx.send('현재 온라인인 멤버가 없습니다.')
  else:
    if len(online_members) > 0:
      member_list = " ".join(online_members)
      member_embed = discord.Embed(title='현재 온라인인 멤버', description=member_list)
    else:
      member_embed = discord.Embed(title='현재 온라인인 멤버',
                                   description='현재 온라인인 멤버가 없습니다.')
    await ctx.send(embed=member_embed)
    '''
        if len(online_bots) > 0:
            bot_list = " ".join(online_bots)
            bot_embed = discord.Embed(title='현재 온라인인 봇', description=bot_list)
            bot_button = Button(style=ButtonStyle.green, label='Show Bots', id='show_bots', disabled=True)
        else:
            bot_embed = discord.Embed(title='현재 온라인인 봇', description='현재 온라인인 봇이 없습니다.')
            bot_button = Button(style=ButtonStyle.green, label='Show Bots', id='show_bots', disabled=True)
        '''


''' Discord.py에 스레드가 없나보네요. 좀더 찾아보자.
@client.command()
async def 스레드테스트(ctx):
'''


@bot.command(name='text맞추기')
async def start_game(ctx):
  global txt_game_started
  global players
  global scores
  global score_cutline

  if not ctx.channel.name == '마식봇':
    await ctx.send("마식봇 채널에서만 게임 진행이 가능합니다.")
    return

  if txt_game_started:
    await ctx.send("게임이 이미 시작되었습니다.")
    return

  txt_game_started = True
  players = []
  scores = {}
  score_cutline = 100

  await ctx.send("게임이 시작됩니다. 10초 안에 반응해주세요." + "<@&1096134050877554719>")
  bot_msg = await ctx.send("게임 참가자를 모아주세요.")
  await bot_msg.add_reaction("✅")

  players = await get_players(bot_msg, 10)
  if not players:
    await ctx.send("플레이어 목록이 없군요....")
    return

  tmpstr = ""
  for i in range(len(players)):
    tmpstr += str(players[i])
    tmpstr += ' '

  chamgaemb = discord.Embed(title='참가자',
                            description=tmpstr,
                            color=discord.Color.blurple())
  await ctx.send(embed=chamgaemb)

  thread_name = f"text맞추기 스레드 {datetime.now(timezone_KST)}"
  thread = await ctx.channel.create_thread(name=thread_name)
  await thread.send("게임 쓰레드를 생성했어요!")

  startemb = discord.Embed(title='게임시작',
                           description="게임 참가자가 모두 모였습니다. 이제부터 게임을 시작하겠습니다.",
                           color=discord.Color.green())
  startemb.add_field(name='참가링크',
                     value=f"여기에서 게임에 참가하세요! : {thread.mention}",
                     inline=False)
  await ctx.send(embed=startemb)
  await thread.send("게임을 시작할게요~")
  tmpemb = await start_rounds(thread, ctx)
  await ctx.send(embed=tmpemb)
  await thread.send("히히 이 스레드는 저장완료되었어요~")
  await thread.edit(archived=True)


async def get_players(bot_msg, time):

  def check(reaction, user):
    return user != client.user and str(reaction.emoji) == '✅'

  players = set()
  end_time = asyncio.get_event_loop().time() + time

  while asyncio.get_event_loop().time() < end_time:
    try:
      reaction, user = await client.wait_for('reaction_add',
                                             timeout=end_time -
                                             asyncio.get_event_loop().time(),
                                             check=check)
      if user not in players:
        players.add(user)
    except asyncio.TimeoutError:
      break

  await bot_msg.delete()

  if players:
    return list(players)
  else:
    await bot_msg.channel.send("시간이 종료되었습니다. 다음에 다시 시도해주십시오")
    return []


async def start_rounds(ctx, superior):
  global txt_game_started
  global players
  global scores
  global channel_fulllist
  global Gangjong
  global score_cutline
  # channel_list_str = ['general', '수수한-보현', '🕊', 'cant-tuna-music', '정신나간-보현', '영-앤-리치-보현', 'shitpost', '작고-귀여운-보현']
  # channel_list = [channel for channel in channel_fulllist if channel.name in channel_list_str]

  channel_list = channel_fulllist
  global round_num
  round_num = 1

  while True:
    ans = ""
    tmpchnl = random.choice(channel_list)
    await ctx.send(
      embed=discord.Embed(title='Round {}'.format(round_num),
                          description="Chose Channel : {}".format(tmpchnl),
                          color=discord.Color.green()))

    #random_int = random.randint(1, 100)
    # 선택한 정수값의 아이디를 가지는 메시지만 가져오기
    messages = []
    try:
      async for message in tmpchnl.history(limit=300):
        #if message.id % 100 == random_int:
        messages.append(message)
    except:
      await ctx.send("액세스 권한이 없군요. 재시작하겠습니다.")
      continue

    random.shuffle(messages)
    # print('shuffled')
    for msg in messages:
      if msg.author != client.user and not msg.content.startswith("&") and len(
          msg.content) < 2000 and len(msg.content) > 2:
        random_msg = msg
        ans = msg.author.name
        #await ctx.send(msg.author.name)
        break
    tmpembed = discord.Embed(title='문제{}'.format(round_num),
                             description=random_msg.content,
                             color=discord.Color.blue())
    # await ctx.send(random_msg.content)
    await ctx.send(embed=tmpembed)
    await asyncio.sleep(1)
    round_num += 1

    if not txt_game_started:
      return

    scores_this_round = {}
    for player in players:
      scores_this_round[player] = 0
    await ctx.send("10초 안에 누가 썼는지 맞춰주세요!")
    correct_players = await get_correct_players(ctx, 10, ans)
    try:
      if Gangjong == True:
        await ctx.send("강제종료되었습니다.")
        txt_game_started = False
        Gangjong = False
        round_num = 0
        gangjongemb = discord.Embed(title='결과',
                                    description="이번 게임은 강제종료되었습니다.... 아쉽군요",
                                    color=discord.Color.purple())
        return gangjongemb
    except:
      await ctx.send("다음 라운드로 가시죠!")

    for player in correct_players:
      scores_this_round[player] += 10

    for player in players:
      if player not in scores.keys():
        scores[player] = 0
      scores[player] += scores_this_round[player]
      if scores[player] >= score_cutline:
        txt_game_started = False
        scores_sorted = sorted(scores.items(),
                               key=lambda x: x[1],
                               reverse=True)
        tmptable = '\n'.join([
          f'{"👑 " if k == 0 else ""}{v[0]} : {v[1]}'
          for k, v in enumerate(scores_sorted)
        ])
        tmpemb = discord.Embed(title='결과발표',
                               description="{}님이 {}점으로 이번 게임을 우승하셨습니다!".format(
                                 player.name, scores[player]),
                               color=discord.Color.yellow())
        tmpemb.add_field(name='점수표',
                         value=f'```\n{tmptable}\n ```',
                         inline=False)
        await ctx.send(embed=tmpemb)
        players = []
        scores = {}
        round_num = 0
        return tmpemb


async def get_correct_players(channel, time, answer):

  def check(msg):
    return msg.author in players and msg.content != "" and not msg.content.startswith(
      "&") and msg.author not in correct_players

  global players
  global correct_players

  correct_players = []
  tmpcnt = 0
  while len(correct_players) < len(players):
    try:
      msg = await client.wait_for('message', timeout=time, check=check)
    except asyncio.TimeoutError:
      await channel.send("Timeout!")
      break
    else:
      if (answer == msg.content):
        correct_players.append(msg.author)
        await channel.send("{}님이 정답을 맞췄습니다!".format(msg.author.name))
        break
      else:
        if (tmpcnt > 10):
          await channel.send("정답은 {}님의 메시지였습니다! 아쉽군요...".format(answer))
          return []
        await msg.reply("땡!")
        tmpcnt += 1
        continue

  return correct_players


@bot.command(name="todo")
async def show_todo_list(ctx):
  to_do_items = get_todo_list()
  if len(to_do_items) > 0:
    items_str = "\n".join(to_do_items)
    await ctx.send(f"Your to-do list:\n{items_str}")
  else:
    await ctx.send("You have no items on your to-do list.")


@bot.command()
async def 개발진척사항(ctx):
  tmp = discord.Embed(title='개발진척사항',
                      description='현재 수행 중인 과제를 Trello로 표시합니다.',
                      color=discord.Color.blue())
  tmp.add_field(name='개발진척사항',
                value='https://trello.com/b/sOpE9eGu/kanban-template',
                inline=False)
  await ctx.reply(embed=tmp)


@dataclass
class songLyric:
  title: string = None
  artist: string = None
  lyric: string = None


@bot.command()
async def 가사(ctx):
  목록 = [
    songLyric("겨울잠", "아이유",
              "빼곡한 가을 한 장 접어다\n너의 우체통에 넣었어\n가장 좋았던 문장 아래 밑줄 그어\n나 만나면 읽어줄래?"),
    songLyric(
      "겨울잠", "아이유",
      "때 이른 봄 몇 송이 꺾어다\n너의 방 문 앞에 두었어\n긴 잠 실컷 자고 나오면\n그때쯤엔 예쁘게 피어 있겠다"),
    songLyric(
      "겨울잠", "아이유",
      "너 없이 보는 첫 봄이, 여름이\n괜히 왜 이렇게 예쁘니\n다 가기 전에 널 보여줘야 하는데\n음-음, 꼭 봐야 하는데"),
    songLyric(
      "겨울잠", "아이유",
      "내게 기대어 조각잠을 자던\n그 모습 그대로 잠들었구나\n무슨 꿈을 꾸니?\n깨어나면 이야기해 줄 거지?\n언제나의 아침처럼"),
    songLyric("겨울잠", "아이유",
              "새하얀 겨울 한숨 속에다\n나의 혼잣말을 담았어\n줄곧 잘 참아내다가도\n가끔은 철없이 보고 싶어"),
    songLyric("겨울잠", "아이유",
              "새삼 차가운 연말의 공기가\n뼈 틈 사이사이 시려와\n움츠려 있을 너의 그 마른 어깨를\n꼭 안아줘야 하는데"),
    songLyric(
      "1:03", "넬",
      "일초가 일분 처럼\n또 하루가 일년 처럼\n길게만 느껴지네요\n잊혀질 것 같았던 너의 기억은\n시간이 갈수록 선명해 져서\n이젠 손에 잡힐 듯 해"
    ),
    songLyric(
      "지구가 태양을 네 번", "넬",
      "지구가 태양을 네번 감싸 안는\n동안 나는 수 만번도 넘게\n너를 그리워했고\n또 지워가야 했어\n왜 그래야만 했어?"),
    songLyric("기억을 걷는 시간", "넬",
              "아직도 너의 소리를 듣고\n아직도 너의 손길을 느껴\n오늘도 난 너의 흔적 안에 살았죠"),
    songLyric("기억을 걷는 시간", "넬", "어떤가요 그댄 어떤가요 그댄\n당신도 나와 같나요\n어떤가요 그댄"),
    songLyric("Moonlight Punch Romance", "넬",
              "아련한 달빛의 노래\n서글퍼 울고 있는 내게\n작지만 큰 위로가 돼\n그 날의 우리를 기억해"),
    songLyric(
      "Fantasy", "넬",
      "Right when you think it’s over\nThat’s when it starts to hover\nIt won’t disappear\n그만 받아들여"
    ),
    songLyric("Fantasy", "넬",
              "돌려 놓을 수 있다해도\n이미 너무 많은걸\n알고 느껴버린 걸\n없던 일이 될 순 없어"),
    songLyric(
      "Day after day", "넬",
      "I’ll sail through the pouring rain\n물론 다 흠뻑 젖을 테지만\n그러면 어때\nI’ll dance in the rain"
    ),
    songLyric(
      "Day after day", "넬",
      "Just wait\nDon’t fade away\n늘 그랬듯 그 자리에서\n날 기다려줘\nDay after day"),
    songLyric("사건의 지평선", "윤하",
              "아낌없이 반짝인 시간은\n조금씩 옅어져 가더라도\n너와 내 맘에 살아 숨 쉴 테니"),
    songLyric("사건의 지평선", "윤하", "여긴 서로의 끝이 아닌\n새로운 길 모퉁이\n익숙함에 진심을 속이지 말자"),
    songLyric("사건의 지평선", "윤하",
              "하나 둘 추억이 떠오르면\n많이 많이 그리워할 거야\n고마웠어요 그래도 이제는\n사건의 지평선 너머로"),
    songLyric("26", "윤하", "천천히 숫자를 거꾸로 세고\n난 이제 떠나보려 해"),
    songLyric("26", "윤하", "좋았던 날들을 두고 갈 테니\n너는 늘 그렇게 예쁘길 바래"),
    songLyric(
      "좋은 꿈 꿔 0224.mp3", "볼빨간사춘기",
      "Have a good night\nIn your dream\n따스한 바람이 불길 바라\nI'll be there"),
    songLyric(
      "좋은 꿈 꿔 0224.mp3", "볼빨간사춘기",
      "I can't control myself\nAlways my eyes on you\n사랑이라 부를 수 있겠다 너를"),
    songLyric("좋은 꿈 꿔 0224.mp3", "볼빨간사춘기",
              "나는 이렇게 부족한 사람인데\n고작 내가 할 수 있는 건\n너의 밤이 평온하길 바라는 것 뿐이야"),
    songLyric("나의 사춘기에게", "볼빨간사춘기",
              "근데 가끔은 너무 행복하면 또 아파올까 봐\n내가 가진 이 행복들을 누군가가 가져갈까 봐"),
    songLyric("별 보러 갈래?", "볼빨간사춘기",
              "They called it milky way 쏟아져 머리 위로\n넌 나를 업고 모래사장을 뛰어다녀, yeah"),
    songLyric("나만 봄", "볼빨간사춘기", "봄이 지나갈 때까지\n다른 사람 다 사라져라\n나만 봄"),
    songLyric("26", "Lauv",
              "Can I tell you a story\n'Bout a boy who broke his own heart?"),
    songLyric(
      "Lucky Strike", "Troye Sivan",
      "'Cause you're safe like spring time\nShort days, long nights, boy"),
    songLyric("Lucky Strike", "Troye Sivan",
              "Tell me all the ways to love you"),
    songLyric(
      "Death By A Thousand Cuts", "Taylor Swift",
      "My heart my hips my body my love\nTryna find a part of me that you didn't touch\nGave up on me like I was a bad drug\nNow I'm searching for signs in a haunted club"
    ),
    songLyric(
      "Death By A Thousand Cuts", "Taylor Swift",
      "Our songs our films united we stand\nOur country guess it was a lawless land\nWhy are my fears at the touch of your hands?\nPaper cut stains from my paper thin plans"
    ),
    songLyric(
      "Death By A Thousand Cuts", "Taylor Swift",
      "My time my wine my spirit my trust\nTryna find a part of me you didn't take up\nGave you so much but it wasn't enough\nBut I'll be alright it's just a thousand cuts"
    ),
    songLyric(
      "前前前世(movie ver.)", "RADWIMPS",
      "너의 전, 전, 전생부터 나는 너를 찾기 시작했어\n그 멋쩍게 웃는 얼굴을 찾으려고 여기에 온 거야\n네가 전전전부 사라지고 산산이 흩어져도\n이제는 헤매지 않아 다시 하나부터 찾기 시작할 거야\n차라리 제로부터 다시 우주를 시작해 볼까"
    )
  ]
  x = np.random.choice(목록)
  tmp = discord.Embed(title=x.lyric)
  tmp.add_field(name=x.title, value=x.artist, inline=True)
  await ctx.reply(embed=tmp)


@bot.command()
async def 덕질(ctx, *, message):
  말 = [' 오늘도 좋은밤되렴 :)', '오늘도 고생 많았어 :)', '잘쟈']
  mslist = message.split(' ')
  if len(mslist) > 2:
    await ctx.reply('&덕질 (상대) (불리기 바라는 호칭(optional)) 형식으로 입력해주세요~')
  if len(mslist) == 1:
    await ctx.reply(f'{mslist[0]}: {ctx.author.name} {np.random.choice(말)}')
  if len(mslist) == 2:
    await ctx.reply(f'{mslist[0]}: {mslist[1]}{np.random.choice(말)}')


@bot.command()
async def 점수변경(ctx, message):
  global score_cutline

  if round_num:  #게임중이면 못바꾸게 합시다.
    tmp = discord.Embed(description='점수커트변경은 게임 시작 전에 요청한 사항에 대해서만 적용됩니다.',
                        color=discord.Color.red())
    await ctx.reply(embed=tmp)
  else:
    tmp = discord.Embed(description='점수커트변경이 적용되었습니다.',
                        color=discord.Color.brand_green())
    await ctx.reply(embed=tmp)

  try:
    intmes = int(message)
  except Exception as e:
    print('예외발생')
    await ctx.reply(f'예외발생 : {e}')
    return
  if intmes < 0:
    await ctx.send('때론 점수가 0보다 작아도...... 괜찮지 않답니다...')
    return
  elif intmes == 0:
    await ctx.reply('이러면 모두가 시작과 동시에 우승하게 됩니다. 이것이 {}의 \'평등\'입니까?'.format(
      message.author))
    return
  score_cutline = intmes
  tmpembed = discord.Embed(
    title="현재점수커트",
    description=f'현재점수커트 : {score_cutline}' +
    f'\n이 게임에서 이기려면 최소 {score_cutline / 10 if not score_cutline % 10 else int(score_cutline / 10) + 1}판을 이겨야겠군요. 다들 힘내세요!'
  )
  await ctx.send(embed=tmpembed)


@bot.command()
async def 강종(ctx):
  global Gangjong
  await ctx.send("현재 진행중인 명령을 중지합니다.")
  Gangjong = True


@bot.command()
async def echo(ctx, *, message):
  await ctx.send(message)


@bot.command()
async def usage(ctx):
  dirname = os.path.dirname(__file__)
  filepath = os.path.join(dirname, 'usage.txt')
  with open(filepath, 'r', encoding='utf-8') as f:
    usage = f.read()
  await ctx.author.send(usage)  # 사용법 문서를 DM으로 전송


@bot.command()
async def deride(ctx, *, message):
  print('Deride : ' + message)
  await ctx.reply('푸하하')


@bot.command()
async def alpha(ctx, *, message):
  print('Alpha : ' + message)
  await ctx.reply('알빠노???')


@bot.command()
async def real(ctx, *, message):
  print('Real : ' + message)
  await ctx.reply('ㄹㅇ')


@bot.command()
async def drum(ctx):
  print('Drum')
  await ctx.reply('두구둥탁')


@bot.command()
async def 수민혁(ctx):
  temp = np.random.randint(2)
  if temp == 1:
    mes = '이수민'
  else:
    mes = '권혁'
  await ctx.reply(mes)


@bot.command()
async def 혁수민(ctx):
  temp = np.random.randint(2)
  if temp == 1:
    mes = '이수민'
  else:
    mes = '권혁'
  await ctx.reply(mes)


@bot.command()
async def 맞추다(ctx):
  await ctx.reply("문제에 대한 답을 틀리지 않게 하다")


@bot.command()
async def 맞히다(ctx):
  await ctx.reply("둘 이상의 일정한 대상들을 나란히 놓고 비교하여 살피다")


@bot.command()
async def 호출(ctx, *, message):
  dding = ctx.guild.get_member(696321570167324672)
  zion = ctx.guild.get_member(541492834172403713)
  try:
    intmes = int(message)
  except Exception as e:
    print('예외발생')
    await ctx.reply(f'예외발생 : {e}')
    return

  if intmes > 20:
    await ctx.reply('너무 많은 호출을 요청했습니다. 자중하시죠?')
    return

  if intmes <= 0:
    await ctx.reply('무슨 생각이십니까?')
    return

  channel_list = []
  channel = None
  for guild in client.guilds:
    for channel in guild.text_channels:
      channel_list.append(channel)
    if channel:
      break

  shitpost = client.get_channel(820305690073497680)
  announcement = client.get_channel(819751872830504980)
  author = ctx.author
  member = ctx.guild.get_member(author.id)
  for _ in range(intmes):
    tmp = np.random.randint(intmes)
    try:
      # await channel_list[tmp].send(f'{zion.mention}' + '메롱')
      await shitpost.send(f'{member.mention}' + ' 멘션 테스트용')
    except Exception as e:
      print(str('''channel_list[tmp]''') + ' 채널에 대한 권한이 부족합니다')
      print(f'예외 발생: {e}')
      # await ctx.reply(str(channel_list[tmp]) + ' 채널에 대한 권한이 부족합니다'))
      await ctx.reply(str(announcement) + ' 채널에 대한 권한이 부족합니다')
    # await shitpost.send(f'{dding.mention}' + '메롱')


''' 추후 개발예정 : Button을 상호작용하기
@bot.command()
async def buttontest(ctx):
  await buttons.send(content='embed 안되는 걸까??',
                     channel=ctx.channel.id,
                     components=[
                       ActionRow([
                         Button(label="버튼이에용 ㅎㅎ",
                                style=ButtonType().Success,
                                custom_id="buttontag")
                       ])
                     ])


@buttons.click
async def buttontag(ctx):
  await ctx.reply('다람쥐는 너무나도 귀엽습니다')
'''

# bot.run(TOKEN)
