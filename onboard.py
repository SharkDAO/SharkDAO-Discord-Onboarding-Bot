import discord
import os, asyncio
from discord.ext.commands import Bot


# Loaded from .env file in repo root dir
token = os.getenv("TOKEN")
guild_id = int(os.getenv("GUILD_ID"))
role_id = int(os.getenv("ROLE_ID"))
general_channel_id = "873484935342727241"
faq_channel_id = "873797683112976404"
join_sharkdao_channel_id = "874174777005326346"


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
        "answer": "c",
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
    # await ctx.message.delete()

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

    # await ctx.message.delete()
    guild = bot.get_guild(guild_id)
    role = guild.get_role(role_id)

    timeout = 120  # How long to wait for a CORRECT answer before aborting the dm

    # Main logic for Questiono & Answer onboarding process

    # DM User and state intent
    # print("DMing User", ctx.author.name)
    await ctx.author.send(
        "Hi I am SharkDao's Onboarding Bot! My job is to quickly get new members familiarized with SharkDao!"
    )
    await ctx.author.send(
        "Lets start with some questions - remember that all the answers are in the <#{faq_channel_id}>!".format(
            faq_channel_id=faq_channel_id
        )
    )

    # Cycle through questions
    question_index = 0
    while True:
        question = questions[question_index]
        # print(question["question"])
        # Send Question
        await ctx.author.send(question["question"])
        # print("Asking User", ctx.author.name, question["question"])
        try:

            # If no correct answer is provided in the timeouot period, asyncio.TimeoutError is returned
            def check(m):
                # print(
                #     m.author.id == ctx.author.id,
                #     m.guild is None,
                #     m.content.lower() == question["answer"],
                # )
                return m.author.id == ctx.author.id and m.guild is None

            msg = await bot.wait_for(
                "message",
                check=check,
                timeout=timeout,
            )
            # print(msg.content.lower(), msg.author.id, ctx.author.id)
            m = msg
            if (
                m.author.id == ctx.author.id
                and m.guild is None
                and m.content.lower() == question["answer"]
            ):
                await msg.author.send("Good job, {.author.name}!".format(msg))
                question_index = question_index + 1
                if question_index == 3:
                    break
            elif (
                m.author.id == ctx.author.id
                and m.guild is None
                and m.content.lower() != question["answer"]
            ):
                await msg.author.send(
                    "That's not quite right, {.author.name}!".format(msg)
                )
                continue

        except asyncio.TimeoutError:
            await ctx.author.send(
                "You took too long to respond correctly. You can try again later using the !onboard command again"
            )
            return True

    # Getting here means answering all above questions correctly, at which point bot can assign the relevant role
    if question_index > 2:
        user_id = msg.author.id
        author = guild.get_member(user_id)
        await author.add_roles(role)
        await msg.author.send(
            "Congratulations, you are now assigned the `@faq-master` role! You may now post in <#{general_channel_id}>. \nBecome a Shark to post in more channels and help us build fun Shark and Nouns projects! \nTo join, follow the instructions in <#{faq_channel_id}> to get SHARK tokens, and then verify in <#{join_sharkdao_channel_id}> to receive your `@sharks` role.".format(
                general_channel_id=general_channel_id,
                faq_channel_id=faq_channel_id,
                join_sharkdao_channel_id=join_sharkdao_channel_id,
            )
        )
        print(
            "Succesfully onboarded: ", msg.author.name, "and assigned role:", role.name
        )


bot.run(token)