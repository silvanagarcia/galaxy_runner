# Documento de diseño — Galaxy Runner

> Versión en Markdown del documento de diseño original
> (`documento-diseno.docx`, incluido en esta misma carpeta).
> Para el diseño **técnico** ver [ARQUITECTURA.md](ARQUITECTURA.md).

---

## Concepto

Galaxy Runner es un *space shooter* 2D inspirado en el *Space Invaders* de los
años 80, con estilo **pixel art** y mecánicas sencillas de movimiento, disparo de
proyectiles, colisiones y puntuación. Desarrollado en **Python** con la librería
**Pygame** para el motor gráfico y **SQLite** para el registro de puntuaciones.

## Descripción general

El jugador controla una nave con el objetivo de eliminar oleadas de enemigos
mientras esquiva proyectiles y objetos, y acumula puntos. El juego cuenta con
**3 niveles** distintos; la dificultad del entorno pone a prueba al jugador a
medida que avanza. La jugabilidad es sencilla pero desafiante.

## Características principales

- Tres escenarios con ambientaciones distintas.
- Tres niveles de dificultad progresiva.
- Sistema de disparos y colisiones entre naves y proyectiles.
- Enemigos con patrones de movimiento simples.
- Sistema de puntuación y registro en base de datos.
- Efectos de sonido y música de fondo.
- Diseño en pixel art para un estilo retro.

## Mecánicas del juego

- **Movimiento de la nave:** izquierda/derecha y arriba/abajo.
- **Colisiones:** se detectan impactos entre proyectiles y enemigos/meteoritos,
  y entre enemigos/meteoritos y la nave del jugador.
- **Progresión:** cada nivel aumenta la velocidad y la frecuencia de disparo,
  además de la vida de los jefes.
- **Game Over:** ocurre al perder todas las vidas.
- **Puntaje:** cada enemigo destruido otorga una cantidad determinada de puntos.
  Cuando un jefe muere, el jugador pasa al siguiente nivel.

## Base de datos

El juego utiliza **SQLite** para almacenar:

- **Jugadores:** información de usuario.
- **Puntuaciones:** ranking de cada jugador (máximo **TOP 10**).

## Objetivos del jugador

- Recolectar puntos con cada baja para ganar power-ups y subir en la tabla de
  ranking.
- Eliminar a los jefes de cada nivel.

## Niveles

| Nivel | Contenido                          |
|-------|-----------------------------------|
| 1     | Juego base + Jefe                 |
| 2     | Velocidad aumentada + Jefe        |
| 3     | Máxima dificultad + Jefe final    |

## Power-ups

| Tipo           | Efecto                          |
|----------------|--------------------------------|
| Vida           | Recupera una vida               |
| Disparo rápido | Mayor cadencia de disparo       |
| Escudo         | Bloquea daño temporalmente      |

## Puntuación

| Objetivo  | Puntos |
|-----------|--------|
| Enemigo   | 20     |
| Meteorito | 50     |
| Jefe 1    | 100    |
| Jefe 2    | 200    |
| Jefe 3    | 300    |
