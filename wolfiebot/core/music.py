

@plugin.listener(hikari.ShardReadyEvent)
async def shard_ready(event: hikari.ShardReadyEvent):
    builder = (
        # TOKEN can be an empty string if you don't want to use lavasnek's discord gateway.
        lavasnek_rs.LavalinkBuilder(event.my_user.id, TOKEN)
        # This is the default value, so this is redundant, but it's here to show how to set a custom one.
        .set_host("127.0.0.1").set_password(LAVALINK_PASSWORD)
    )

    builder.set_start_gateway(False)

    lava_client = await builder.build(EventHandler())

    plugin.bot.d.lavalink = lava_client