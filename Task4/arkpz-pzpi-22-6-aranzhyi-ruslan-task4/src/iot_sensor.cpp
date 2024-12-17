#include <iostream>
#include <cpr/cpr.h>

#include "iot_sensor.h"


constexpr double THERMAL_GRADIENT_PER_METER = 0.0065;
constexpr double ZERO_KELVIN = -273.15;


IotSensor::IotSensor(const toml::table& config) {
    const auto api_host = config["server"]["host"].value<std::string>();
    if (!api_host) {
        throw std::runtime_error("Failed to initialize: \"host\" under \"[server]\" is not specified!");
    }
    this->api_host = api_host.value();

    const auto api_key = config["server"]["api_key"].value<std::string>();
    if (!api_key) {
        throw std::runtime_error("Failed to initialize: \"api_key\" under \"[server]\" is not specified!");
    }
    this->api_key = api_key.value();

    const auto measurement_interval = config["sensor"]["measurement_interval"].value<uint32_t>();
    if (!measurement_interval) {
        throw std::runtime_error(
            "Failed to initialize: \"measurement_interval\" under \"[sensor]\" is not specified!");
    }
    this->measurement_interval = measurement_interval.value();

    const auto altitude = config["sensor"]["altitude"].value<uint16_t>();
    if (!altitude) {
        throw std::runtime_error(
            "Failed to initialize: \"altitude\" under \"[sensor]\" is not specified!");
    }
    this->altitude = altitude.value();

    this->source = MeasurementSource::createSource(config);
    if (this->source == nullptr) {
        throw std::runtime_error("Failed to create measurements source!");
    }

    this->measurements_count = config["sensor"]["measurement_count"].value_or<uint16_t>(32);
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

        uint16_t valid_measurements_count = 0;
        for(; valid_measurements_count < measurements_count; ++valid_measurements_count) {
            if(last_measurements[valid_measurements_count].pressure == 0)
                break;
        }

        double trend_pressure;
        double altitude;
        double pressure_at_sea_level;
        uint16_t zambretti_index;
        time_t time_u;
        tm* time_s;

        if(valid_measurements_count < 3) {
            std::cout << "Insufficient data to make simple forecast.\n";
            goto loop_end;
        }

        trend_pressure = last_measurements[0].pressure - last_measurements[2].pressure;
        altitude = this->altitude * THERMAL_GRADIENT_PER_METER;
        pressure_at_sea_level = last_measurements[0].pressure * std::pow(
            1 - altitude / (last_measurements[0].temperature + altitude - ZERO_KELVIN), -5.257);

        std::cout << "Pressure is ";
        if (trend_pressure > 0.5) {
            std::cout << "rising";
            zambretti_index = 179 - 20 * pressure_at_sea_level / 129;
        } else if (trend_pressure < -0.5) {
            std::cout << "falling";
            zambretti_index = 130 - 10 * pressure_at_sea_level / 81;
        } else {
            std::cout << "steady";
            zambretti_index = 147 - 50 * pressure_at_sea_level / 376;
        }

        std::cout << ", prediction is \"";

        time_u = time(nullptr);
        time_s = localtime(&time_u);

        /*if(trend_pressure < -0.5 && (time_s->tm_mon == 11 || time_s->tm_mon == 0 || time_s->tm_mon == 1)) {
            --zambretti_index;
        } else if(trend_pressure > 0.5 && (time_s->tm_mon == 5 || time_s->tm_mon == 6 || time_s->tm_mon == 7)) {
            ++zambretti_index;
        }*/

        switch(zambretti_index) {
            case 1: { std::cout << "Settled Fine"; break; }
            case 2: { std::cout << "Fine Weather"; break; }
            case 3: { std::cout << "Fine, Becoming Less Settled"; break; }
            case 4: { std::cout << "Fairly Fine, Showery Later"; break; }
            case 5: { std::cout << "Showery, Becoming More Unsettled"; break; }
            case 6: { std::cout << "Unsettled, Rain Later"; break; }
            case 7: { std::cout << "Rain at Times, Worse Later"; break; }
            case 8: { std::cout << "Rain at Times, Becoming Very Unsettled"; break; }
            case 9: { std::cout << "Very Unsettled, Rain"; break; }
            case 10: { std::cout << "Settled Fine"; break; }
            case 11: { std::cout << "Fine Weather"; break; }
            case 12: { std::cout << "Fine, Possibly Showers"; break; }
            case 13: { std::cout << "Fairly Fine, Showers Likely"; break; }
            case 14: { std::cout << "Showery, Bright Intervals"; break; }
            case 15: { std::cout << "Changeable, Some Rain"; break; }
            case 16: { std::cout << "Unsettled, Rain at Times"; break; }
            case 17: { std::cout << "Rain at Frequent Intervals"; break; }
            case 18: { std::cout << "Very Unsettled, Rain"; break; }
            case 19: { std::cout << "Stormy, Much Rain"; break; }
            case 20: { std::cout << "Settled Fine"; break; }
            case 21: { std::cout << "Fine Weather"; break; }
            case 22: { std::cout << "Becoming Fine"; break; }
            case 23: { std::cout << "Fairly Fine, Improving"; break; }
            case 24: { std::cout << "Fairly Fine, Possibly Showers Early"; break; }
            case 25: { std::cout << "Showery Early, Improving"; break; }
            case 26: { std::cout << "Changeable, Mending"; break; }
            case 27: { std::cout << "Rather Unsettled, Clearing Later"; break; }
            case 28: { std::cout << "Unsettled, Probably Improving"; break; }
            case 29: { std::cout << "Unsettled, Short Fine Intervals"; break; }
            case 30: { std::cout << "Very Unsettled, Finer at Times"; break; }
            case 31: { std::cout << "Stormy, Possibly Improving"; break; }
            case 32: { std::cout << "Stormy, Much Rain"; break; }
            default: { std::cout << "Unknown"; break; }
        }

        std::cout << "\"\n";

loop_end:
        sleep(measurement_interval);
    }
}

void IotSensor::sendData(Measurement measurement) {
    cpr::Response resp = cpr::Post(cpr::Url{api_host + "/measurements"},
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
