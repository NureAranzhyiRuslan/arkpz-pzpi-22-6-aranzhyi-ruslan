#pragma once

#include <string>
#include <toml++/toml.hpp>

#include "measurement_source.h"

class IotSensor {
public:
    explicit IotSensor(const toml::table& config);

    void run();

private:
    std::string api_host;
    std::string api_key;
    uint32_t measurement_interval;

    MeasurementSource* source;
    uint16_t measurements_count;
    Measurement* last_measurements;
    uint16_t altitude;

    void sendData(Measurement measurement);
};
