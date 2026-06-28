"""Discord UI view for the paginated leaderboard for level cog.

Displays XP/level of users rankings with navigation buttons.
Only the user who triggered the command can interact with the view.

© by hassanpacary
"""

# --- Standard library ---
from typing import cast

# --- Third-party ---
import discord
from discord.ui import View, button
from discord.utils import MISSING

# --- Internal ---
from bot.cogs.core import core_strings
from bot.cogs.level import level_strings
from bot.config import colors_config
from bot.utils import discord_utils


class LeaderboardView(View):
    """Paginated leaderboard view.

    Attributes:
        ctx: The Discord interaction context.
        pages: A list of pages, each containing a list of leaderboard rows.
        author: The user who triggered the leaderboard command.
        current_page: The current page when enter on the leaderboard.
    """

    def __init__(
            self,
            ctx: discord.Interaction,
            pages: list[list],
            author: discord.User | discord.Member,
    ) -> None:
        super().__init__()
        self.ctx = ctx
        self.pages = pages
        self.author = author
        self.current_page: int = 0

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Prevents other members from interacting with the buttons.

        Args:
            interaction: The incoming button interaction.

        Returns:
            True if the interacting user is the original author, False otherwise.
        """
        if interaction.user != self.author:
            await interaction.response.send_message(
                content=level_strings.Leaderboard.PREVENT_OTHER_MEMBER_INTERACTION,
                ephemeral=True,
            )
            return False
        return True

    async def get_embed(self) -> discord.Embed:
        """Builds the embed for the current page.

        Returns:
            A fully constructed discord.Embed for the current leaderboard page.
        """
        guild = cast(discord.Guild, self.ctx.guild)
        title = level_strings.Leaderboard.TITLE.format(
            current_page=self.current_page + 1,
            pages=len(self.pages),
        )
        icon = str(guild.icon.url) if hasattr(guild.icon, "url") else MISSING
        fields = []

        for i, row in enumerate(
            self.pages[self.current_page],
            start=self.current_page * 10 + 1,
        ):
            user_id, xp, level, next_level = row
            member = guild.get_member(user_id)

            if member is not None:
                display_name = member.display_name
            else:
                display_name = level_strings.Leaderboard.UNKNOWN_USER

            fields.append((
                level_strings.Leaderboard.USER_NAME_FIELD.format(
                    rank=i,
                    display_name=display_name,
                ),
                level_strings.Leaderboard.USER_LEVEL_FIELD.format(
                    level=level,
                    xp=xp,
                    next_level=next_level,
                )
            ))

        return await discord_utils.create_discord_embed(
            color=discord.Color(int(colors_config.ORANGE, 16)),
            title=title,
            author=core_strings.GUILD_NAME,
            icon=icon,
            fields=fields,
            fields_is_inline=False,
        )

    async def _update_message(self, interaction: discord.Interaction) -> None:
        """Updates the message with the current page embed.

        Args:
            interaction: The button interaction that triggered the update.
        """
        leaderboard = await self.get_embed()
        await interaction.response.edit_message(embed=leaderboard, view=self)

    @button(
        label=level_strings.Leaderboard.BUTTON_PREVIOUS,
        style=discord.ButtonStyle.blurple,
    )
    async def _previous(
            self: "LeaderboardView",
            interaction: discord.Interaction,
            _btn: discord.ui.Button,
    ) -> None:
        """Navigates to the previous leaderboard page.

        Args:
            interaction: The button interaction.
            _btn: The button that was clicked.
        """
        if self.current_page > 0:
            self.current_page -= 1
            await self._update_message(interaction)

    @button(
        label=level_strings.Leaderboard.BUTTON_NEXT,
        style=discord.ButtonStyle.blurple,
    )
    async def _next(
            self: "LeaderboardView",
            interaction: discord.Interaction,
            _btn: discord.ui.Button,
    ) -> None:
        """Navigates to the next leaderboard page.

        Args:
            interaction: The button interaction.
            _btn: The button that was clicked.
        """
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            await self._update_message(interaction)
