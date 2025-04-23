import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import CONF_ID

sensor_ns = cg.esphome_ns.namespace('zmpt101b_ns')

Zmpt101bSensor = sensor_ns.class_('ZMPT101BSensor', cg.PollingComponent)

# Обновлённая схема конфигурации
CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(Zmpt101bSensor),
    cv.Required("adc_pin"): cv.int_range(min=0, max=99),  # Пин АЦП
    cv.Optional("sensitivity", default=500): cv.float_range(min=0, max=1000),  # Чувствительность
    cv.Optional("rms_sensor"): sensor.SENSOR_SCHEMA,  # Датчик RMS-напряжения
    cv.Optional("instant_sensor"): sensor.SENSOR_SCHEMA,  # Датчик мгновенного напряжения
})

async def to_code(config):
    # Создаём объект ZMPT101BSensor
    var = cg.new_Pvariable(config[CONF_ID], config["adc_pin"], config["sensitivity"])
    await cg.register_component(var, config)

    # Регистрируем датчик RMS-напряжения
    if "rms_sensor" in config:
        sens_rms = await sensor.new_sensor(config["rms_sensor"])
        cg.add(var.set_rms_sensor(sens_rms))

    # Регистрируем датчик мгновенного напряжения
    if "instant_sensor" in config:
        sens_instant = await sensor.new_sensor(config["instant_sensor"])
        cg.add(var.set_instant_sensor(sens_instant))
