"""
bot/services/level/leaderboard_view.py
© by hassanpacary

class for display leaderboard view containing embed and buttons
"""

# --- Third party imports ---
import discord
from discord.ui import View, button

# --- Bot modules ---
from bot.core.config_loader import BOT, STRINGS
from bot.utils.discord_utils import create_discord_embed


# ██╗     ███████╗ █████╗ ██████╗ ███████╗██████╗ ██████╗  ██████╗  █████╗ ██████╗ ██████╗     ██╗   ██╗██╗███████╗██╗    ██╗
# ██║     ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗    ██║   ██║██║██╔════╝██║    ██║
# ██║     █████╗  ███████║██║  ██║█████╗  ██████╔╝██████╔╝██║   ██║███████║██████╔╝██║  ██║    ██║   ██║██║█████╗  ██║ █╗ ██║
# ██║     ██╔══╝  ██╔══██║██║  ██║██╔══╝  ██╔══██╗██╔══██╗██║   ██║██╔══██║██╔══██╗██║  ██║    ╚██╗ ██╔╝██║██╔══╝  ██║███╗██║
# ███████╗███████╗██║  ██║██████╔╝███████╗██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝     ╚████╔╝ ██║███████╗╚███╔███╔╝
# ╚══════╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝       ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝


class LeaderboardView(View):
    """Leaderboard display class"""

    def __init__(self, ctx, pages, author):
        """Initialize the view"""
        super().__init__()
        self.ctx = ctx
        self.pages = pages
        self.current_page = 0

        # To prevent other members from interacting
        self.author = author

    async def get_embed(self):
        """Build the embed message"""
        color = BOT['color']['social']
        embed_author_field = STRINGS['system']['guild']
        embed_dict = STRINGS['level']['leaderboard']

        fields = []
        for i, row in enumerate(self.pages[self.current_page], start=self.current_page * 10 + 1):
            user_id, xp, level, next_level = row
            user = self.ctx.guild.get_member(user_id)

            fields.append(
                (
                    f"#{i} — {user.display_name}",
                    f"**Niveau :** {level} | **XP :** {xp}/{next_level}"
                )
            )

        embed = await create_discord_embed(
            color=discord.Color(int(color, 16)),
            title=embed_dict['title'].format(current_page=self.current_page+1, pages=len(self.pages)),
            author=embed_author_field,
            icon=self.ctx.guild.icon,
            fields=fields,
            fields_is_inline=False
        )

        return embed

    async def _update_message(self, ctx: discord.Interaction):
        """Update the message with other embed page"""
        leaderboard = self.get_embed()
        await ctx.response.edit_message(embed=leaderboard, view=self) # type: ignore

    @button(label="⬅️ Précédent", style=discord.ButtonStyle.blurple) # type: ignore
    async def previous(self, ctx: discord.Interaction):
        if ctx.user.id != self.author.id:
            return

        if self.current_page > 0:
            self.current_page -= 1
            await self._update_message(ctx)

    @button(label="➡️ Suivant", style=discord.ButtonStyle.blurple) # type: ignore
    async def next(self, ctx: discord.Interaction):
        if ctx.user.id != self.author.id:
            return

        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            await self._update_message(ctx)
