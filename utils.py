class Utils:
    async def is_connected(self, ctx):
        vc = ctx.voice_client
        if vc:
            return True
        return False