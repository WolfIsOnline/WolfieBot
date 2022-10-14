import discord

from classes.utils import Utils
from discord.ext import commands
from discord.commands import slash_command
from discord.ui import Button, View, Modal, InputText

class SimpleEmbed(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils()
        self.children = None
        
    async def simple_embed(self, ctx, channel: discord.TextChannel):
        embed = discord.Embed(title="This is the title of the embed", description="This is the description of the embed", color=self.utils.DEFAULT_COLOR)
        embed.set_author(name="Author name will go here")
        embed.set_footer(text="This is the footer")
           
        edit_body = EmbedButton("Edit Body")
        edit_author = EmbedButton("Edit Author")
        edit_footer = EmbedButton("Edit Footer")
        
        confirm = EmbedButton("Confirm")
            
        view = View()
        view.add_item(edit_body)
        view.add_item(edit_author)
        view.add_item(edit_footer)
        view.add_item(confirm)
        await ctx.respond("Embed Preview:", view=view, embed=embed, ephemeral=True)
        
        # Modal Callbacks
        async def edit_body_modal_callback(interaction):
            if self.children[0].value != "":
                embed.title = self.children[0].value
                
            if self.children[1].value != "":
                embed.description = self.children[1].value
            await interaction.response.edit_message(embed=embed)

        async def edit_author_modal_callback(interaction):
            if self.children[0].value != "":
                embed.set_author(name=self.children[0].value)
            await interaction.response.edit_message(embed=embed)
            
        async def edit_footer_modal_callback(interaction):
            if self.children[0].value != "":
                embed.set_footer(text=self.children[0].value)
            await interaction.response.edit_message(embed=embed)            
            
        # Button Callbacks
        async def edit_body_callback(interaction: discord.Interaction):
            modal = EmbedModal("Edit Body", ["Edit Title", "Edit Description"], [embed.title, ""], [discord.InputTextStyle.short, discord.InputTextStyle.long])
            await interaction.response.send_modal(modal)
            modal.callback = edit_body_modal_callback
            self.children = modal.children
            
        async def edit_author_callback(interaction: discord.Interaction):
            modal = EmbedModal("Edit Author", ["Edit Author"], [embed.author.name], [discord.InputTextStyle.short])
            await interaction.response.send_modal(modal)
            modal.callback = edit_author_modal_callback
            self.children = modal.children
            
        async def edit_footer_callback(interaction: discord.Interaction):
            modal = EmbedModal("Edit Footer", ["Edit Footer"], [embed.footer.text], [discord.InputTextStyle.short])
            await interaction.response.send_modal(modal)
            modal.callback = edit_footer_modal_callback
            self.children = modal.children
            
        async def confirm_callback(interaction: discord.Interaction):
            await channel.send(embed=embed)
            
        edit_body.callback = edit_body_callback
        edit_author.callback = edit_author_callback
        edit_footer.callback = edit_footer_callback
        confirm.callback = confirm_callback
        
class EmbedModal(Modal):
    def __init__(self, title, a_labels, a_placeholders, a_style):
        super().__init__(title=title)
        
        
        self.value = None
        for c, label in enumerate(a_labels):
                self.add_item(InputText(label=label, placeholder=a_placeholders[c], required=False, style=a_style[c]))
            
        
class EmbedButton(Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.blurple)
        
        
def setup(bot):
    bot.add_cog(SimpleEmbed(bot))
