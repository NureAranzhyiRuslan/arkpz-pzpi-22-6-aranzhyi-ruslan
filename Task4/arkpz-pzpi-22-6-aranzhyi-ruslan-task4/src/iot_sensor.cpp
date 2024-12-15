#include <iostream>
#include <cpr/cpr.h>

#include "iot_sensor.h"


IotSensor::IotSensor(const toml::table& config) {
    const auto api_host = config["server.host"].value<std::string>();
    if (!api_host) {
        throw std::runtime_error("Failed to initialize: \"host\" under \"[server]\" is not specified!");
    }
    this->api_host = api_host.value();

    const auto api_key = config["server.api_key"].value<std::string>();
    if (!api_key) {
        throw std::runtime_error("Failed to initialize: \"api_key\" under \"[server]\" is not specified!");
    }
    this->api_key = api_key.value();

    const auto measurement_interval = config["server.host"].value<uint32_t>();
    if (!measurement_interval) {
        throw std::runtime_error(
            "Failed to initialize: \"measurement_interval\" under \"[sensor]\" is not specified!");
    }
    this->measurement_interval = measurement_interval.value();

    this->source = MeasurementSource::createSource(config);
    if (this->source == nullptr) {
        throw std::runtime_error("Failed to create measurements source!");
    }

    this->measurements_count = config["sensor.measurement_count"].value_or<uint16_t>(32);
    this->last_measurements = new Measurement[this->measurements_count];

    for (int i = 0; i < measurements_count; ++i) {
        this->last_measurements[i].temperature = this->last_measurements[i].pressure = 0;
    }
}

void IotSensor::run() {
    while (true) {
        const Measurement ms = this->source->getMeasurement();
        sendData(ms);
        memcpy(last_measurements + 1, last_measurements, sizeof(Measurement) * (measurements_count - 1));
        last_measurements[0] = ms;

        // TODO: make forecast

        sleep(measurement_interval);
    }
}

void IotSensor::sendData(Measurement measurement) {
    cpr::Response resp = cpr::Post(cpr::Url{api_host},
                                   cpr::Header{{"Authorization", api_key}},
                                   cpr::Body{
                                       std::format("{{ \"temperature\": {:.2f}, \"pressure\": {:.2f} }}",
                                                   measurement.temperature, measurement.pressure)
                                   },
                                   cpr::Header{{"Content-Type", "application/json"}});
    if (resp.status_code != 200) {
        std::cerr << std::format("Failed to send data: {} - {}\n", resp.status_code, resp.text);
    } else {
        std::cout << "Data sent successfully.\n";
    }
}
