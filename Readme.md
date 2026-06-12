# MeteoChile Weather Integration for Home Assistant

![HACS Valid](https://img.shields.io/badge/HACS-Custom-orange.svg)

Esta es una integración personalizada (Custom Integration) para Home Assistant que obtiene las temperaturas y condiciones actuales directamente desde las estaciones meteorológicas en Chile proporcionadas por Climatología MeteoChile.

## Características

- Temperatura Actual (°C)
- Humedad Relativa (%)
- Agua Caída en las últimas 6 y 24 horas (mm)
- Coordenadas geográficas de la estación (para uso en el mapa de Home Assistant)
- Soporte para configurar múltiples estaciones simultáneamente.

## Requisitos

Para usar esta integración, necesitas una cuenta gratuita en [Climatología MeteoChile](https://climatologia.meteochile.gob.cl/).
Una vez registrado, podrás obtener:
1. Tu **Email** registrado.
2. Tu **Token** (API Token de la cuenta).
3. El **ID de la Estación** a la que quieres conectarte (ej: `330020` para Quinta Normal, Santiago).

## Instalación a través de HACS

Esta integración es compatible con HACS (Home Assistant Community Store).

1. Ve a HACS en tu panel de Home Assistant.
2. Selecciona **Integraciones**.
3. Haz clic en los tres puntos (menú) en la esquina superior derecha y selecciona **Repositorios Personalizados (Custom repositories)**.
4. Agrega la URL de este repositorio (`https://github.com/joasssko/meteochile_weather`) y selecciona la categoría **Integration**.
5. Haz clic en **Agregar**.
6. Busca "MeteoChile Weather" en HACS y dale a **Descargar**.
7. ¡Reinicia tu Home Assistant!

## Configuración

Una vez instalada y reiniciado Home Assistant:

1. Ve a **Ajustes** > **Dispositivos y Servicios** > **Añadir Integración**.
2. Busca **MeteoChile Weather**.
3. Ingresa el **ID de la Estación**, tu **Email** y tu **Token**.
4. ¡Listo! Se crearán los sensores automáticamente para esa estación.

Puedes repetir este proceso para agregar más de una estación a tu Home Assistant.
