import io
import interactions
import helpers.standards

class Ping(interactions.Extension):
    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="ping",
        description="A ping command used to test if the bot is responsive.",
    )
    async def ping(self, ctx: interactions.CommandContext):
        # TODO: make helper class with embed setup (or public vars, or even a public embed, idc)
        # embed = interactions.Embed(title="Title", description="Desc", color=0xbb9ba5)
        file, embed = helpers.standards.genEmbed()
        embed.add_field(name="Field 1", value="hi", inline=False)
        await ctx.send(files=file, embeds=embed)
        # await ctx.send("pong motherfucker")



def setup(client):
    print("setup")
    Ping(client)