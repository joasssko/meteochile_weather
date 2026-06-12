"""Config flow for MeteoChile Weather integration."""
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_STATION_ID, CONF_EMAIL, CONF_TOKEN

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_STATION_ID): str,
        vol.Required(CONF_EMAIL): str,
        vol.Required(CONF_TOKEN): str,
    }
)

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    station_id = data[CONF_STATION_ID].strip()
    email = data[CONF_EMAIL].strip()
    token = data[CONF_TOKEN].strip()
    
    url = f"https://climatologia.meteochile.gob.cl/application/servicios/getEmaResumenDiario/{station_id}?token={token}&usuario={email}"
    session = async_get_clientsession(hass)
    
    try:
        async with session.get(url, timeout=10) as response:
            response.raise_for_status()
            result = await response.json(content_type=None)
            
            # Validation
            if "datosEstacion" not in result or not result.get("datosEstacion", {}).get("nombreEstacion"):
                raise ValueError("invalid_station")
                
            station_name = result["datosEstacion"]["nombreEstacion"]
    except Exception as e:
        raise ValueError("cannot_connect") from e

    return {"title": f"{station_name} ({station_id})"}

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MeteoChile Weather."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                
                # Ensure values are cleaned
                user_input[CONF_STATION_ID] = user_input[CONF_STATION_ID].strip()
                user_input[CONF_EMAIL] = user_input[CONF_EMAIL].strip()
                user_input[CONF_TOKEN] = user_input[CONF_TOKEN].strip()
                
                # Check if already configured
                await self.async_set_unique_id(user_input[CONF_STATION_ID])
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(title=info["title"], data=user_input)
            except ValueError as e:
                errors["base"] = str(e)
            except Exception:  # pylint: disable=broad-except
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )
