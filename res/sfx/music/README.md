# 🎵 Sistema de Música - Galaxy Runner

Este directorio contiene los archivos de música de fondo para diferentes estados del juego.

## 📁 Archivos de Música Requeridos:

Coloca tus archivos de música aquí con estos nombres exactos:

### 🎼 Música de Menú
- **menu_music.mp3** - Música que se reproduce en las pantallas de menú (pantalla1, pantalla2, ranking)

### ⚔️ Música de Gameplay
- **enemies_music.mp3** - Música durante combate con esbirros (niveles 1, 2 y 3)

### 👹 Música de Jefes
- **boss1_music.mp3** - Música específica para el Jefe 1
- **boss2_music.mp3** - Música específica para el Jefe 2  
- **boss3_music.mp3** - Música específica para el Jefe 3

## 🎮 Comportamiento del Sistema de Música:

### 🎵 **Música de Menú** (`menu_music.mp3`):
- ✅ Se reproduce al iniciar el juego
- ✅ Continúa en pantalla1, pantalla2 y ranking
- ⏸️ Se **PAUSA** cuando se inicia el gameplay (pantalla2 → playing)
- ▶️ Se **REANUDA** cuando se vuelve al menú desde game over o victory

### ⚔️ **Música de Esbirros** (`enemies_music.mp3`):
- ✅ Se reproduce durante combate con esbirros
- ✅ **MISMA CANCIÓN** para todos los niveles (1, 2 y 3)
- ⏸️ Se **PAUSA** cuando aparece un jefe
- ▶️ Se **REANUDA** cuando el jefe es derrotado

### 👹 **Música de Jefes**:
- **Jefe 1**: `boss1_music.mp3` - Se reproduce solo durante combate con el jefe del nivel 1
- **Jefe 2**: `boss2_music.mp3` - Se reproduce solo durante combate con el jefe del nivel 2
- **Jefe 3**: `boss3_music.mp3` - Se reproduce solo durante combate con el jefe del nivel 3

## 🔄 Transiciones de Música:

### 📈 **Flujo de Música en el Juego**:

```
Inicio del Juego
    ↓
🎵 MENU_MUSIC (pantalla1, pantalla2)
    ↓ (presionar ENTER en pantalla2)
⏸️ PAUSA (fade out 1 segundo)
    ↓
⚔️ ENEMIES_MUSIC (combate con esbirros)
    ↓ (aparece jefe)
👹 BOSS_MUSIC (específica del nivel)
    ↓ (jefe derrotado)
⚔️ ENEMIES_MUSIC (siguiente nivel)
    ↓ (Game Over o Victory)
🎵 MENU_MUSIC (volver al menú)
```

### 🎛️ **Características Técnicas**:
- **Transiciones suaves**: Fade in/out de 1 segundo
- **Sin superposición**: Solo una música a la vez
- **Loop infinito**: Todas las músicas se repiten automáticamente
- **Control de volumen**: Ajustable desde configuración
- **Detección automática**: El sistema cambia música según el estado del juego

## 🎨 Recomendaciones de Música:

### 🎵 **Música de Menú**:
- **Estilo**: Épico, espacial, atmosférico
- **Tempo**: Moderado, no muy acelerado
- **Duración**: 2-4 minutos (se repite en loop)
- **Ambiente**: Misterioso, aventurero

### ⚔️ **Música de Esbirros**:
- **Estilo**: Acción, combate, dinámico
- **Tempo**: Rápido, energético
- **Duración**: 2-3 minutos (se repite en loop)
- **Ambiente**: Tensión, batalla espacial

### 👹 **Música de Jefes**:
- **Jefe 1**: Intenso pero no demasiado épico (jefe inicial)
- **Jefe 2**: Más dramático y complejo (jefe intermedio)
- **Jefe 3**: Épico, final, máxima intensidad (jefe final)
- **Duración**: 3-5 minutos cada una
- **Ambiente**: Cada jefe debe tener personalidad musical única

## 📝 Especificaciones Técnicas:

- **Formato**: MP3 (recomendado)
- **Calidad**: 128-320 kbps
- **Volumen**: Normalizado (el sistema ajusta automáticamente)
- **Loop**: Diseñadas para repetirse sin cortes abruptos
- **Tamaño**: Optimizado para carga rápida

## ⚠️ Notas Importantes:

- Los nombres de archivo deben coincidir **exactamente** (sensible a mayúsculas)
- Si un archivo no existe, el juego funcionará sin esa música específica
- El sistema detecta automáticamente qué archivos están disponibles
- Las transiciones son automáticas según el estado del juego
- No se superponen múltiples músicas

## 🎧 Prueba del Sistema:

1. **Coloca** tus 5 archivos MP3 en esta carpeta
2. **Ejecuta** el juego
3. **Verifica** que se carguen en la consola: "Música encontrada: [nombre]"
4. **Prueba** las transiciones navegando por los menús y jugando

¡Tu sistema de música dinámico está listo para crear una experiencia sonora inmersiva! 🚀🎵
