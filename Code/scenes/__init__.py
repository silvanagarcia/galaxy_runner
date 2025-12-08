

from .start_menu import StartMenuScene
from .game_scene import GameScene
from .leaderboard_scene import LeaderboardScene
from .credits_scene import CreditsScene

# Intentar importar escenas opcionales si existen
try:
    from .game_over_scene import GameOverScene
except ImportError:
    GameOverScene = None

try:
    from .options_scene import OptionsScene
except ImportError:
    OptionsScene = None

__all__ = [
    'StartMenuScene', 'GameScene', 'LeaderboardScene', 'CreditsScene',
    'GameOverScene', 'OptionsScene'
]
