# Draguz Shop · Videos

Videos promocionales verticales (9:16) de Draguz Shop para Reels, TikTok y Shorts. *Define your different.*

## Videos/

| Video | Duración |
|---|---|
| Material y calidad v2 | 23 s |
| Tarjeta de lealtad | 21 s |
| Cotiza en 10 segundos | 22 s |
| DTF textil vs DTF UV | 26 s |
| Diseños listos para estampar | 23 s |

## Proyectos/

Cada carpeta es un proyecto de [HyperFrames](https://hyperframes.dev) (HTML + GSAP → MP4):
`video-draguz` (material), `video-draguz-lealtad`, `video-draguz-cotiza`, `video-draguz-tecnicas` (DTF textil vs UV) y `video-draguz-disenos`.

- Voz: ElevenLabs, "Antonio".
- Música: beat instrumental generado con ElevenLabs Music.
- GSAP va incluido en `assets/vendor/`.

Para editar y volver a renderizar (necesita Node y FFmpeg):

```
cd Proyectos/video-draguz-cotiza
npx -y hyperframes@0.8.190 preview
npx -y hyperframes@0.8.190 render
```
