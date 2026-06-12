"""Sensor platform for MeteoChile Weather."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfPrecipitationDepth,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import MeteoChileCoordinator

SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="temperatura",
        name="Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="humedadRelativa",
        name="Relative Humidity",
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="aguaCaida6Horas",
        name="Rainfall (Last 6 Hours)",
        device_class=SensorDeviceClass.PRECIPITATION,
        native_unit_of_measurement=UnitOfPrecipitationDepth.MILLIMETERS,
        state_class=SensorStateClass.TOTAL,
    ),
    SensorEntityDescription(
        key="aguaCaida24Horas",
        name="Rainfall (Last 24 Hours)",
        device_class=SensorDeviceClass.PRECIPITATION,
        native_unit_of_measurement=UnitOfPrecipitationDepth.MILLIMETERS,
        state_class=SensorStateClass.TOTAL,
    ),
)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the sensor platform."""
    coordinator: MeteoChileCoordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        MeteoChileSensor(coordinator, entry, description)
        for description in SENSOR_TYPES
    ]

    async_add_entities(sensors)

class MeteoChileSensor(CoordinatorEntity[MeteoChileCoordinator], SensorEntity):
    """Representation of a MeteoChile Sensor."""

    def __init__(
        self,
        coordinator: MeteoChileCoordinator,
        entry: ConfigEntry,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.station_id}_{description.key}"
        
        station_name = "MeteoChile"
        if coordinator.data and coordinator.data.get("station_name"):
            station_name = coordinator.data.get("station_name")
            
        self._attr_name = f"{station_name} {description.name}"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
            
        value = self.coordinator.data.get(self.entity_description.key)
        if value is None:
            return None
            
        try:
            return float(value)
        except ValueError:
            return None

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        station_name = f"Station {self.coordinator.station_id}"
        if self.coordinator.data and self.coordinator.data.get("station_name"):
            station_name = self.coordinator.data.get("station_name")
            
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.station_id)},
            name=station_name,
            manufacturer="MeteoChile",
            model="Weather Station",
        )

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Return the extra state attributes."""
        attrs = {}
        if self.coordinator.data:
            attrs["momento"] = self.coordinator.data.get("momento")
            
            # Map coordinates
            if self.coordinator.data.get("latitude"):
                try:
                    attrs["latitude"] = float(self.coordinator.data.get("latitude"))
                except ValueError:
                    pass
            if self.coordinator.data.get("longitude"):
                try:
                    attrs["longitude"] = float(self.coordinator.data.get("longitude"))
                except ValueError:
                    pass

        return attrs
