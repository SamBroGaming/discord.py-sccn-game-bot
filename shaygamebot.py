import discord, asyncio, mysql.connector, requests, time
from discord.ext import tasks, commands

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="pw",
  database="discordpy"
)

mycursor = mydb.cursor(buffered=True)

client = commands.Bot(command_prefix="pumpkin ")
client.remove_command('help')

global usd_value

url = 'http://api.shaycryptoco.in/price'

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    activity = discord.Game(name="Prefix pumpkin ")
    await client.change_presence(status=discord.Status.dnd, activity=activity)
    giving.start()
    getting_stats.start()

@tasks.loop(seconds=300.0)
async def giving():
    people = mycursor.execute("SELECT discord_id FROM discordpy.pumpkinvalues")
    people = mycursor.fetchall()
    people_list = []

    for i in people:
        people_list.append(i[0])

    for i in people_list:
        pumpkins = mycursor.execute(F"SELECT pumpkins FROM discordpy.pumpkinvalues WHERE discord_id = {i}")
        pumpkins = mycursor.fetchone()
        length = len(str(pumpkins)) - 2
        pumpkins = str(pumpkins)[1:length]
        if pumpkins == 'o':
            pumpkins = 0
        pumpkins = int(pumpkins)
        tractors = mycursor.execute(F"SELECT tractors FROM discordpy.pumpkinvalues WHERE discord_id = {i}")
        tractors = mycursor.fetchone()
        length = len(str(tractors)) - 2
        tractors = str(tractors)[1:length]
        if tractors == 'o':
            tractors = 0
        tractors = int(tractors) * 2
        pumpkin_scoopers = mycursor.execute(F"SELECT pumpkin_scoopers FROM discordpy.pumpkinvalues WHERE discord_id = {i}")
        pumpkin_scoopers = mycursor.fetchone()
        length = len(str(pumpkin_scoopers)) - 2
        pumpkin_scoopers = str(pumpkin_scoopers)[1:length]
        if pumpkin_scoopers == 'o':
            pumpkin_scoopers = 0
        pumpkin_scoopers = int(pumpkin_scoopers) * 3
        carving_machines = mycursor.execute(F"SELECT carving_machines FROM discordpy.pumpkinvalues WHERE discord_id = {i}")
        carving_machines = mycursor.fetchone()
        length = len(str(carving_machines)) - 2
        carving_machines = str(carving_machines)[1:length]
        if carving_machines == 'o':
            carving_machines = 0
        carving_machines = int(carving_machines) * 4
        pumpkins = pumpkins + 1 + tractors + pumpkin_scoopers + carving_machines
        insertion = mycursor.execute(F"UPDATE pumpkinvalues SET pumpkins = {pumpkins} WHERE discord_id = {i}")
        insert = mydb.commit()

@tasks.loop(seconds=60)
async def getting_stats():
    global usd_value
    response = requests.get(url)
    response_json = response.json()
    usd_value = response_json['usd']
    
@tasks.loop(count=1)
async def add_deposit(ctx):
    length = len(ctx.system_content)
    other_length = length - 20
    third_length = length - 2
    x = ctx.system_content[other_length:(length-2)]
    if ctx.system_content[other_length:(length-2)] == '753091466988879913' or ctx.system_content[(other_length - 1):(length-2)] == '753091466988879913':
        if ctx.system_content[22:33] == 'just tipped' or ctx.system_content[21:32] == 'just tipped':
            length = length - 31
            try:
                amount_to_add = float(ctx.system_content[34:length])
            except ValueError:
                amount_to_add = float(ctx.system_content[33:(length-1)])
            try:
                author_id = str(int(ctx.system_content[2:20]))
            except ValueError:
                author_id = str(int(ctx.system_content[2:19]))
            sccn = mycursor.execute(F"SELECT sccn FROM discordpy.pumpkinvalues WHERE discord_id = {author_id}")
            sccn = str(mycursor.fetchone())
            if sccn == "None":
                sccn = 0
            sccn += amount_to_add
            inserting = mycursor.execute(F"UPDATE pumpkinvalues SET sccn = {sccn} WHERE discord_id = {author_id}")
            mydb.commit()
            embed = discord.Embed(title="Success", description=F"You just deposited {amount_to_add} sccn successfully!", color=0xFFA500)
            embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
            ctx = await client.get_context(ctx)
            await ctx.send(embed=embed)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.author.bot == True:
        if message.author.id != 607942707620610087:
            return
        else:
            add_deposit.start(message)

    await client.process_commands(message)

@client.command(aliases = ['pumpkins', 'p'])
async def pumpkin(ctx):
    author_id = str(ctx.author.id)
    pumpkins = mycursor.execute(F"SELECT pumpkins FROM discordpy.pumpkinvalues WHERE discord_id = {author_id}")
    pumpkins = str(mycursor.fetchone())
    length = len(pumpkins) - 2
    pumpkins = pumpkins[1:length]
    try:
        pumpkins = int(pumpkins)
    except ValueError:
        pumpkins = 0

    if pumpkins == 1:
        embed=discord.Embed(title="Pumpkins: ", description=F"You have {pumpkins} pumpkin", color=0xFFA500)
        embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Pumpkins: ", description=F"You have {pumpkins} pumpkins", color=0xFFA500)
        embed.add_field(name="If you have 0 pumpkins:", value="If you have 0 pumpkins, try registering?")
        embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
        await ctx.send(embed=embed)

@client.command(aliases = ["tractors", "t", "ts"])
async def tractor(ctx):
    author_id = str(ctx.author.id)
    tractor = mycursor.execute(F"SELECT tractors FROM discordpy.pumpkinvalues WHERE discord_id = {author_id}")
    tractor = str(mycursor.fetchone())
    length = len(tractor) - 2
    tractor = tractor[1:length]
    tractor = int(tractor)

    if tractor == 1:
        embed=discord.Embed(title="Tractors: ", description=F"You have {tractor} tractor", color=0xFFA500)
        embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Tractors: ", description=F"You have {tractor} tractors", color=0xFFA500)
        embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
        await ctx.send(embed=embed)

@client.command(aliases = ["ps", "pumpkinscoopers"])
async def pumpkinscooper(ctx):
    author_id = str(ctx.author.id)
    pumpkin_scooper = mycursor.execute(F"SELECT pumpkin_scoopers FROM discordpy.pumpkinvalues WHERE discord_id = {author_id}")
    pumpkin_scooper = str(mycursor.fetchone())
    length = len(pumpkin_scooper) - 2
    pumpkin_scooper = pumpkin_scooper[1:length]
    pumpkin_scooper = int(pumpkin_scooper)

    if pumpkin_scooper == 1:
        embed=discord.Embed(title="Pumpkin Scoopers: ", description=F"You have {pumpkin_scooper} pumpkin scooper", color=0xFFA500)
        embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Pumpkin Scoopers: ", description=F"You have {pumpkin_scooper} pumpkin scoopers", color=0xFFA500)
        embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
        await ctx.send(embed=embed)

@client.command(aliases = ["cm", "carvingmachine", "cms"])
async def carvingmachines(ctx):
    author_id = str(ctx.author.id)
    carving_machines = mycursor.execute(F"SELECT carving_machines FROM discordpy.pumpkinvalues WHERE discord_id = {author_id}")
    carving_machines = str(mycursor.fetchone())
    length = len(carving_machines) - 2
    carving_machines = carving_machines[1:length]
    carving_machines = int(carving_machines)

    if carving_machines == 1:
        embed=discord.Embed(title="Carving Machines: ", description=F"You have {carving_machines} carving machine", color=0xFFA500)
        embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
        await ctx.send(embed=embed)
    else: 
        embed=discord.Embed(title="Carving Machines: ", description=F"You have {carving_machines} carving machines", color=0xFFA500)
        embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
        await ctx.send(embed=embed)

@client.command(aliases = ["bal", "bals", "balance", "balances", "b"])
async def sccn(ctx):
    author_id = str(ctx.author.id)
    sccn = mycursor.execute(F"SELECT sccn FROM discordpy.pumpkinvalues WHERE discord_id = {author_id}")
    sccn = str(mycursor.fetchone())
    if sccn == "None":
        sccn = 0
        embed=discord.Embed(title="Sccn: ", description=F"You have {sccn} sccn", color=0xFFA500)
        embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
        await ctx.send(embed=embed)
    else:
        length = len(sccn) - 4
        sccn = sccn[10:length]
        usd_price = usd_value * float(sccn)
        usd_price = round(usd_price, 2)
        embed=discord.Embed(title="Sccn: ", description=F"You have {sccn} sccn ≈ {usd_price} usd", color=0xFFA500)
        embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
        await ctx.send(embed=embed)

@client.command(aliases=["register"])
async def r(ctx):
    account = str(ctx.author.id)

    try:
        mycursor.execute(F"INSERT INTO pumpkinvalues (discord_id, pumpkins, tractors, pumpkin_scoopers, carving_machines, sccn) VALUES ('{account}', 0, 0, 0, 0, 0.0)")
        mydb.commit()
        embed=discord.Embed(title="Success:", description="Registered", color=0xFFA500)
        embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
        await ctx.send(embed=embed)

    except mysql.connector.IntegrityError:
        embed=discord.Embed(title="Error:", description="You are already registered", color=0xFFA500)
        embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
        await ctx.send(embed=embed)

@client.command()
async def buy(ctx, amount: int = 1, item: str = ''):
    items_list = ['tractor', 'tractors', 't', 'pumpkin_scooper', 'pumpkin_scoopers', 'p', 'carving_machine', 'carving_machines', 'c']
    items_price = {'tractor' : 3, 'tractors' : 3, 't' : 3, 'pumpkin_scooper' : 4, 'pumpkin_scoopers' : 4, 'p' : 4, 'carving_machine' : 5, 'carving_machines' : 5, 'c' : 5}
    if item in items_list:
        item_price = items_price[item] * amount
        usd_price = usd_value * float(item_price)
        usd_price = round(usd_price, 2)
        embed=discord.Embed(title="Are you Sure?", description=F"This will cost {item_price} sccn ≈ {usd_price} usd. Reply yes or no.", color=0xFFA500)
        embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
        await ctx.send(embed=embed)
        def check(m):
            return m.channel == ctx.channel
        try:
            msg = await client.wait_for('message', check=check, timeout=60.0)
            message_to_check = msg.system_content
            message_to_check = message_to_check.lower()
            
            if message_to_check == 'yes':
                if item in ['t', 'tractor']:
                    item = 'tractors'
                elif item in ['p', 'pumpkin_scooper']:
                    item = 'pumpkin_scoopers'
                elif item in ['c', 'carving_machine']:
                    item = 'carving_machines'

                values = mycursor.execute(F"SELECT sccn FROM discordpy.pumpkinvalues WHERE discord_id = {ctx.author.id}")
                values = str(mycursor.fetchone())
                if values == 'None':
                    embed=discord.Embed(title="Error:", description="You need to register. You can do this by typing pumpkin r.", color = 0xFFA500)
                    embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
                    await ctx.send(embed=embed)
                else:
                    length = len(values) - 4
                    values = values[10:length]
                    values = float(values)
                    item_values = mycursor.execute(F"SELECT {item} FROM discordpy.pumpkinvalues WHERE discord_id = {ctx.author.id}")
                    item_values = str(mycursor.fetchone())
                    length = len(item_values) - 2
                    item_values = item_values[1:length]
                    item_values = int(item_values)
                    new_item_values = item_values + amount
                    if values >= item_price:
                        new_balance = values - item_price
                        inserting = mycursor.execute(F"UPDATE pumpkinvalues SET sccn = {new_balance} WHERE discord_id = {ctx.author.id}")
                        mydb.commit()
                        inserting_2 = mycursor.execute(F"UPDATE pumpkinvalues SET {item} = {new_item_values} WHERE discord_id = {ctx.author.id}")
                        mydb.commit()
                        embed = discord.Embed(title = "Success!", description = F"You have successfully bought your items!", color = 0xFFA500)
                        embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(title = 'Error:', description = "You don't have the funds for this", color = 0xFFA500)
                        embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
                        await ctx.send(embed=embed)
            elif message_to_check == 'no':
                embed=discord.Embed(title="Command Cancelled", description="You have cancelled the command successfully", color=0xFFA500)
                embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="You didn't enter yes or no", description="Command cancelled", color=0xFFA500)
                embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
                await ctx.send(embed=embed)
        except asyncio.TimeoutError:
            embed = discord.Embed(title="Error:", description="The command timed out", color=0xFFA500)
            embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
            await ctx.send(embed=embed)
    else: 
        embed = discord.Embed(title = "Error:", description = F"You can't buy '{item}'", color = 0xFFa500)
        embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
        await ctx.send(embed=embed)

@client.command()
async def sell(ctx, amount: int = 1):
    message_author = str(ctx.author.id)
    pumpkins = mycursor.execute(F"SELECT pumpkins FROM discordpy.pumpkinvalues WHERE discord_id = {message_author}")
    pumpkins = mycursor.fetchone()
    length = len(str(pumpkins)) - 2
    pumpkins = int(str(pumpkins)[1:length])
    sccn_amount = amount/1000
    if pumpkins >= amount:
        embed=discord.Embed(title="Are you sure?", description=F"You want to sell {amount} pumpkins? That will give you {sccn_amount} sccn", color=0xFFA500)
        embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
        await ctx.send(embed=embed)
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        try:
            msg = await client.wait_for('message', check=check, timeout=60)
            message_to_check = msg.system_content
            message_to_check = message_to_check.lower()

            if message_to_check == 'yes':
                sccn = mycursor.execute(F"SELECT sccn FROM discordpy.pumpkinvalues WHERE discord_id = {message_author}")
                sccn = str(mycursor.fetchone())
                length = len(sccn) - 4
                sccn = sccn[10:length]
                sccn = float(sccn)
                new_sccn = sccn + sccn_amount
                sccn_insertion = mycursor.execute(F"UPDATE pumpkinvalues SET sccn = {new_sccn} WHERE discord_id = {message_author}")
                sccn_insertion = mydb.commit()
                if amount == 1:
                    embed=discord.Embed(title="Success!", description=F"You just sold {amount} pumpkin for {sccn_amount} to bring your total up to {new_sccn}!", color=0xFFA500)
                    await ctx.send(embed=embed)
                else:
                    embed=discord.Embed(title="Success!", description=F"You just sold {amount} pumpkins for {sccn_amount} to bring your total up to {new_sccn}!", color=0xFFA500)
                    await ctx.send(embed=embed)

            elif message_to_check == "no":
                embed=discord.Embed(title="Error:", description="Command cancelled.", color=0xFFA500)
                embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
                await ctx.send(embed=embed)

            else:
                embed=discord.Embed(title="Error:", description="Command cancelled", color=0xFFA500)
                embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
                await ctx.send(embed=embed)

        except asyncio.TimeoutError:
            embed=discord.Embed(title="Error:", description="The command timed out", color = 0xFFA500)
            embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Error:", description="You don't have enough pumpkins for this", color=0xFFA500)
        embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
        await ctx.send(embed=embed)

@client.command(aliases=['d'])
async def deposit(ctx):
    embed=discord.Embed(title="Send from SCCN Tipbot to Pumpkin Farm Bot", description="Send your desired amount from SCCN Tipbot. Important: **YOU MUST BE REGISTERED!**", color=0xFFA500)
    embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
    await ctx.send(embed=embed)

@client.command(aliases=['w'])
async def withdraw(ctx, amount: float):
    user_id = ctx.author.id
    await ctx.send(F'sccn!tip <@{user_id}> {amount}')

@client.command(aliases = ["c", "cmd", "cmds", "command", "commands"])
async def help(ctx):
    embed=discord.Embed(title="List of Commands:", color=0xFFA500)
    embed.add_field(name="pumpkins: ", value="How many Pumpkins you have.")
    embed.add_field(name="tractor: ", value="How many tractors you have.")
    embed.add_field(name="pumpkin Scoopers: ", value="How many Pumpkin Scoopers you have.")
    embed.add_field(name="carving Machines: ", value="How many Carving Machines you have.")
    embed.add_field(name="r, register", value="Registers you into the db and lets you earn.")
    embed.add_field(name="sccn, any variation of balance", value="Show's your balance in SCCN and USD.")
    embed.add_field(name="buy", value="Allows you to buy upgrades (Tractors : 3 SCCN, Pumpkin Scoopers : 4 SCCN, and Carving Machines : 5 SCCN).")
    embed.add_field(name="sell", value="Allows you to sell your pumpkins for sccn at 0.01 SCCN each.")
    embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
    await ctx.send(embed=embed)

@buy.error
async def buy_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed=discord.Embed(title="Error:", description="I did not recognize that command. You may be missing a parameter", color=0xFFA500)
        embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
        await ctx.send(embed=embed)

    if isinstance(error, commands.BadArgument):
        embed=discord.Embed(title="Error:", description="One (or more) of those parameters was entered incorrectly", color=0xFFA500)
        embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
        await ctx.send(embed=embed)

@sell.error
async def sell_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed=discord.Embed(title="Error:", description="I did not recognize that command. You may be missing a parameter", color=0xFFA500)
        embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
        await ctx.send(embed=embed)

    if isinstance(error, commands.BadArgument):
        embed=discord.Embed(title="Error:", description="One (or more) of those parameters was entered incorrectly", color=0xFFA500)
        embed.set_footer(text="This game is a community-led project, not funded nor endorsed by the SCCN team. Play at your own risk.")
        await ctx.send(embed=embed)

client.run('token')