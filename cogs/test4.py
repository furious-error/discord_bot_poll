import asyncio
import datetime
import discord
from discord.ext import commands
from discord.ext.commands import Bot


class VoteBot(commands.Cog):

    bot:Bot

    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def poll(self, ctx, duration:int, question, *options):
        duration_minute = int(duration) * 60
        final_datetime = datetime.datetime.now() + datetime.timedelta(minutes=duration)
        end_datetime = final_datetime.strftime("%b %d, %Y, %I:%M %p")
        if len(options) <= 2:
            await ctx.send('You need more than two option to create a poll!')
            return
        if len(options) > 10:
            await ctx.send('You cannot create a poll with more than 10 options!')
            return
        if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
            reactions = ['✅', '❌']
        elif len(options) == 2 and options[0] == 'no' and options[1] == 'yes':
            reactions = ['❌', '✅']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        description = []
        for i, option in enumerate(options):
            description += '\n{} {}\n'.format(reactions[i], option)
        embed = discord.Embed(title=question, description=''.join(description))
        embed.add_field(name='Poll will end on {}'.format(end_datetime), value='', inline=True)
        react_message = await ctx.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)

        
        await asyncio.sleep(duration_minute)  # Wait for the duration of the poll

        # Get the poll results
        message = await ctx.channel.fetch_message(react_message.id)
        results = {}
        for reaction in message.reactions:
            if str(reaction.emoji) in reactions[:len(options)]:
                # Subtract the bot's own reaction
                results[reactions.index(str(reaction.emoji))] = reaction.count - 1
        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

        # Create the poll results message
        result_description = []
        for i, (option_index, count) in enumerate(sorted_results):
            result_description += '\n{}. {} - {} vote{}\n'.format(
                i+1, options[option_index], count, 's' if count != 1 else '')
        result_embed = discord.Embed(
            title='Poll Results: ' + question, description=''.join(result_description))
        await ctx.send(embed=result_embed)

        # Disable reactions on the poll message
        for reaction in message.reactions:
            await reaction.clear()

        
    # @poll_error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Duration must be a valid integer!')
        else:
            await ctx.send('An error occurred while processing the command!')



async def setup(bot):
    await bot.add_cog(VoteBot(bot))