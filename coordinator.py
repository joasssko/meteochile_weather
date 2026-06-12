"""DataUpdateCoordinator for MeteoChile Weather."""
import logging
from datetime import timedelta

import aiohttp
import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, CONF_STATION_ID, CONF_EMAIL, CONF_TOKEN, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

class MeteoChileCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize."""
        self.station_id = entry.data[CONF_STATION_ID]
        self.email = entry.data[CONF_EMAIL]
        self.token = entry.data[CONF_TOKEN]
        self.session = async_get_clientsession(hass)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        url = f"https://climatologia.meteochile.gob.cl/application/servicios/getEmaResumenDiario/{self.station_id}?token={self.token}&usuario={self.email}"
        try:
            async with async_timeout.timeout(10):
                response = await self.session.get(url)
                response.raise_for_status()
                data = await response.json(content_type=None)
                return self._parse_data(data)
                
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}")

    def _parse_data(self, data: dict) -> dict:
        """Parse the API response."""
        datos_estacion = data.get("datosEstacion", {})
        valores = data.get("datos", {}).get("valoresMasRecientes", {})
        
        result = {
            "station_name": datos_estacion.get("nombreEstacion"),
            "latitude": datos_estacion.get("latitud"),
            "longitude": datos_estacion.get("longitud"),
            "temperatura": valores.get("temperatura"),
            "humedadRelativa": valores.get("humedadRelativa"),
            "aguaCaida6Horas": valores.get("aguaCaida6Horas"),
            "aguaCaida24Horas": valores.get("aguaCaida24Horas"),
            "momento": valores.get("momento"),
        }
        
        return result
