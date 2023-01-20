import interactions
import json

def main():
    # bot set up
    token = json.load(open("admin/private.json", 'r'))["token"]
    client = interactions.Client(token=token, intents=interactions.Intents.DEFAULT)

    # To use files in CommandContext send, you need to load it as an extension.
    client.load("interactions.ext.files")
    # Load custom extensions
    client.load("extension_commands.ping")
    # client.load("admin.terminal")

    client.start()

if __name__ == "__main__":
    main()
