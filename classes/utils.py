class Utils:
    
    DEFAULT_COLOR = 0x02e7e7
    async def is_connected(self, ctx):
        vc = ctx.voice_client
        if vc:
            return True
        return False