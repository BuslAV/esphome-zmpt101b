#pragma once

#include "esphome.h"
#include "esphome/components/sensor/sensor.h"
#include "zmpt101b.h"

namespace esphome {
namespace zmpt101b_ns {

class ZMPT101BSensor : public PollingComponent, public sensor::Sensor {
 public:
  uint8_t adcPin;
  esphome::zmpt101b_ns::ZMPT101B *zmpt101b;

  // Новый датчик для мгновенных значений напряжения
  Sensor *instant_voltage_sensor = new Sensor();

  // Конструктор
  ZMPT101BSensor(uint8_t adcPin, float sensitivity) : PollingComponent(1000) {
    this->adcPin = adcPin;
    this->zmpt101b = new esphome::zmpt101b_ns::ZMPT101B(adcPin);
    this->zmpt101b->setSensitivity(sensitivity);
  }

  float get_setup_priority() const override { return esphome::setup_priority::HARDWARE; }

  void setup() override {
    // Ничего не делаем
  }

  void update() override {
    // Публикуем RMS-напряжение
    float Vrms = this->zmpt101b->getRmsVoltage();
    publish_state(Vrms);

    // Публикуем мгновенное напряжение
    float Vinstant = this->zmpt101b->getInstantVoltage();
    this->instant_voltage_sensor->publish_state(Vinstant);
  }
};

}
}
