
# Entities - Entidades del juego (jugador, enemigos, proyectiles, etc.)


from .player import Player
from .enemigos import Enemy
from .boss import Boss
from .meteorito import Meteor
from .proyectiles import Projectile
from .powerup import PowerUp

# Intentar importar explosiones si existe
try:
    from .explosiones import Explosion
except ImportError:
    Explosion = None

__all__ = [
    'Player', 'Enemy', 'Boss', 'Meteor', 'Projectile', 'PowerUp', 'Explosion'
]
