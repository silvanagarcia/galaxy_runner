

### Sistema de explosiones


import pygame

class Explosion:
    def __init__(self, x: int, y: int, size: int = 30):
        self.x = x
        self.y = y
        self.size = size
        self.max_size = size * 2
        self.current_size = 0
        self.duration = 0.3  # segundos
        self.timer = 0
        self.active = True
        
    def update(self, dt: float) -> bool:
        
        ### Actualizar explosión. Retorna False cuando termina
        
        self.timer += dt
        self.current_size = int(self.max_size * (self.timer / self.duration))
        
        if self.timer >= self.duration:
            self.active = False
            return False
        return True
    
    def draw(self, screen: pygame.Surface):
        
        ### Dibujar la explosión
        
        if not self.active:
            return
        
        # Explosión simple: círculos concéntricos
        alpha = int(255 * (1 - self.timer / self.duration))
        
        # Círculo exterior
        pygame.draw.circle(screen, (255, 255, 0), 
                          (int(self.x), int(self.y)), 
                          self.current_size)
        
        # Círculo interior
        if self.current_size > 5:
            pygame.draw.circle(screen, (255, 0, 0), 
                              (int(self.x), int(self.y)), 
                              self.current_size // 2)

