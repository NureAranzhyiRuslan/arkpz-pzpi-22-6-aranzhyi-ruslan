#include <iostream>
#include "iot_sensor.h"

int main() {
    IotSensor* iot;

    try {
        const toml::table config = toml::parse_file("config.toml");
        iot = new IotSensor(config);
    } catch (const std::exception& ex) {
        std::cerr << "Initialization error: " << ex.what() << std::endl;
        return 1;
    }

    iot->run();
    delete iot;

    return 0;
}