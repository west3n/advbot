from decouple import config

admin_id = int(config("ADMIN_ID"))
bot_token = config("TOKEN")
group_ids = [int(x) for x in config("GROUP_IDS").split(",")]
