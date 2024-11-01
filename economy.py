import discord, json, os, random
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix="Mr!", intents=discord.Intents.all())

filename = "economy.json"

if not os.path.exists(filename):
    with open(filename, "w") as f:
        json.dump({}, f)
    print(f"Created new file: {filename}")

def load_data():
    with open(filename, "r") as f:
        return json.load(f)

def save_data(data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

@bot.event
async def on_ready():
    print(f"{bot.user} is on")
    await bot.tree.sync()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("That command does not exist")
    elif isinstance(error, commands.errors.MissingPermissions):
        await ctx.send("You do not have permissions to use this command")
    elif isinstance(error, commands.errors.MemberNotFound):
        await ctx.send("That member does not exist")
    elif isinstance(error, commands.errors.CommandOnCooldown):
        await ctx.send(f"This command is on cooldown. Please try again in {error.retry_after:.2f} seconds")

@commands.cooldown(1, 900, commands.BucketType.user)
@bot.hybrid_command(name="work", description="Work for me!")
async def work(ctx):
    user_id = str(ctx.author.id)
    data = load_data()

    phrases = [
    f"{ctx.author.mention} has worked as a cashier and earned",
    f"{ctx.author.mention} delivered pizzas and made",
    f"{ctx.author.mention} mowed lawns in the neighborhood and collected",
    f"{ctx.author.mention} walked dogs for busy pet owners and received",
    f"{ctx.author.mention} worked a shift at the local factory and earned",
    f"{ctx.author.mention} sold handmade crafts online and pocketed",
    f"{ctx.author.mention} did some freelance writing and got paid",
    f"{ctx.author.mention} helped out at a car wash and made",
    f"{ctx.author.mention} worked as a street performer and collected",
    f"{ctx.author.mention} completed online surveys and earned",
    f"{ctx.author.mention} worked overtime at the office and received",
    f"{ctx.author.mention} offered tech support and was paid",
    f"{ctx.author.mention} taught an online class and made",
    f"{ctx.author.mention} worked as a virtual assistant and earned",
    f"{ctx.author.mention} did some gardening work and collected"
    ]


    if not user_id in data:
        data[user_id] = {"money": 0}
    
    randphrase = random.choice(phrases)
    added_money = random.randint(120, 450)
    data[user_id]["money"] += added_money

    embed = discord.Embed(
        title="You worked!",
        description=f"{randphrase} ${added_money}",
        colour=discord.Colour.dark_green()
    )
    save_data(data)
    await ctx.send(embed=embed)

@commands.cooldown(1, 1200, commands.BucketType.user)
@bot.hybrid_command(name="crime", description="Commit a crime for money!")
async def crime(ctx):
    user_id = str(ctx.author.id)
    data = load_data()

    success_phrases = [
    f"{ctx.author.mention} pulled off a daring heist and got away with",
    f"{ctx.author.mention} hacked into a digital vault and transferred",
    f"{ctx.author.mention} organized a complex scheme and pocketed",
    f"{ctx.author.mention} snuck into a high-security area and snagged",
    f"{ctx.author.mention} conducted a risky operation and secured",
    f"{ctx.author.mention} executed a cunning plan and acquired",
    f"{ctx.author.mention} orchestrated a clever con and walked away with",
    f"{ctx.author.mention} infiltrated a secret facility and escaped with",
    f"{ctx.author.mention} cracked a supposedly unbreakable safe and obtained",
    f"{ctx.author.mention} conducted some shady business and earned",
    f"{ctx.author.mention} engaged in some questionable activities and gained",
    f"{ctx.author.mention} took a walk on the wild side and came back with",
    f"{ctx.author.mention} bent the rules of society and profited",
    f"{ctx.author.mention} lived dangerously for a day and collected",
    f"{ctx.author.mention} took a big risk and it paid off with"
    ]

    caught_phrases = [
    f"{ctx.author.mention} got caught red-handed and had to pay a fine of",
    f"{ctx.author.mention}'s plan backfired, resulting in a penalty of",
    f"{ctx.author.mention} tripped the alarm and lost",
    f"{ctx.author.mention}'s scheme unraveled, costing them",
    f"{ctx.author.mention} was outsmarted by security and fined",
    f"{ctx.author.mention}'s luck ran out, and they had to forfeit",
    f"{ctx.author.mention} got busted and had to cough up",
    f"{ctx.author.mention}'s criminal career hit a snag, losing them",
    f"{ctx.author.mention} faced the consequences and paid",
    f"{ctx.author.mention}'s risky venture failed, costing them",
    f"{ctx.author.mention} couldn't talk their way out and lost",
    f"{ctx.author.mention}'s master plan fell apart, resulting in a loss of",
    f"{ctx.author.mention} got a taste of justice and had to pay",
    f"{ctx.author.mention}'s crime spree came to an abrupt end, costing",
    f"{ctx.author.mention} learned crime doesn't pay and lost"
    ]

    if not user_id in data:
        data[user_id] = {"money": 0}

    if random.randint(1, 100) <= 65:
        amount = random.randint(120, 450) * 3
        data[user_id]["money"] += amount
        phrase = random.choice(success_phrases)
        colour = discord.Colour.brand_red()
    else:
        amount = random.randint(120, 450) * 4
        data[user_id]["money"] -= amount
        phrase = random.choice(caught_phrases)
        colour = discord.Colour.dark_red()
    
    embed = discord.Embed(
        title="You committed a crime!",
        description=f"{phrase} ${amount}",
        colour=colour
    )

    save_data(data)
    await ctx.send(embed=embed)
@commands.cooldown(1, 60, commands.BucketType.user)
@bot.hybrid_command(name="balance", description="Check your balance!")
async def balance(ctx):
    user_id = str(ctx.author.id)
    data = load_data()

    if not user_id in data:
        data[user_id] = {"money": 0}

    embed = discord.Embed(
        title="Your balance",
        description=f"You have ${data[user_id]['money']}",
        colour=discord.Colour.dark_green()
    )
    await ctx.send(embed=embed)

bot.run(os.getenv("API_KEY"))