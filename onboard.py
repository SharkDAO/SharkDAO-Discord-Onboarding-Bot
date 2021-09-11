import discord
import os, asyncio
from discord.ext.commands import Bot


# Loaded from .env file in repo root dir
token = os.getenv("TOKEN")
guild_id = int(os.getenv("GUILD_ID"))
role_id = int(os.getenv("ROLE_ID"))


intents = discord.Intents.all()
bot = Bot(command_prefix="!", intents=intents)


# Load Question/answers
questions = [
    {
        "question": "Question 1: What is SharkDAO? \nA: A 10k profile picture project \nB: An exclusive group for large NFT collectors \nC: A DAO that collects Nouns, partners with artists, and grows the nouns ecosystem \nD: A DAO that invests in pizza related NFT’s",
        "answer": "c",
    },
    {
        "question": "Question 2: Which of the following is NOT a risk of joining SharkDAO? \nA: 3 of our trusted signers go rogue and steal the DAO’s funds \nB: The DAO never owns any Nouns \nC: An NFT market collapse \nD: A smart contract hack or exploit",
        "answer": "b",
    },
    {
        "question": "Question 3: What is a SHARK token? \nA: A governance token \nB: A community access token \nC: Both of the above",
        "answer": "d",
    },
]


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="for new sharks"
        )
    )


@bot.command()
async def startOnBoardBot(ctx):
    await ctx.message.delete()

    # Send a message with embed
    embed = discord.Embed(
        title="Use !onboard to start the onboarding process",
        description="This quick process will allow you to participate in the rest of the general discord channels! \n\n User Settings > Privacy & Safety > 'Allow direct messages from server members' must be turned On. You can turn this setting off afterwards. \n\nWe recommend taking a look at #faq and #links before starting the onboarding process.",
        color=0xE91E63,
    )
    file = discord.File(
        "dm_setting.jpeg"
    )  # an image in the same folder as the main bot file
    embed.set_image(url="attachment://dm_setting.jpeg")
    await ctx.channel.send(embed=embed, file=file)


@bot.command()
async def onboard(ctx):

    await ctx.message.delete()
    guild = bot.get_guild(guild_id)
    role = guild.get_role(role_id)

    timeout = 120  # How long to wait for a CORRECT answer before aborting the dm

    # Main logic for Questiono & Answer onboarding process

    # DM User and state intent
    await ctx.author.send(
        "Hi I am SharkDao's Onboarding Bot! My job is to quickly get new members familiarized with SharkDao!"
    )
    await ctx.author.send("Lets start with some questions")

    # Cycle through questions
    for question in questions:
        # print(question["question"])
        # Send Question
        await ctx.author.send(question["question"])
        try:

            # Checks if answer is exact match to question
            # If no correct answer is provided in the timeouot period, asyncio.TimeoutError is returned
            def check(m):
                return m.content.lower() == question["answer"]

            msg = await bot.wait_for(
                "message",
                check=check,
                timeout=timeout,
            )
            await ctx.author.send("Right {.author.name}!".format(msg))

        except asyncio.TimeoutError:
            await ctx.author.send(
                "You took too long to respond correctly. You can try again later using the !onboard command again"
            )
            return True

    # Getting here means answering all above questions correctly, at which point bot can assign the relevant role
    await ctx.message.author.add_roles(role)
    await ctx.author.send(
        "You have completed the onboarding processs and have been assigned a new role in the server!"
    )
    print("Succesfully onboarded: ", ctx.author.name, "and assigned role:", role.name)


bot.run(token)