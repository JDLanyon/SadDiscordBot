# TODO: Refactor the file name
import interactions

# def genEmbed(string: command_name, bool: can_disable=False):
def genEmbed():
    # TODO: Attachments just don't FUCKING work, use imgur or something instead I guess.
    embed = interactions.Embed(color=0xbb9ba5)
    file = interactions.File(fp="assets/Pixel Lotus.png", filename="Logo.png")
    embed.set_author(name="ur worst nitemar >:)", icon_url="attachment://Logo.png")
    embed.set_image(url="attachment://Logo.png")
    embed.set_footer(text="Wanna disable commands? I haven't added that yet so suck shit.")
    return file, embed