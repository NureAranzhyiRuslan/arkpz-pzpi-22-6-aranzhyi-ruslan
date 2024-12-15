#include "measurement_source.h"

CSVMeasurementSource::CSVMeasurementSource(const toml::table& config) : MeasurementSource(config) {
    const auto filename = config["source"]["csv"]["file_path"].value<std::string>();
    if (!filename) {
        throw std::runtime_error(R"(Failed to open CSV file: "file_path" under "[source.csv]" is not specified!)");
    }

    file.open(filename.value());
    if (!file.is_open()) {
        throw std::runtime_error("Failed to open CSV file: " + filename.value());
    }

    std::string header;
    std::getline(file, header);
}

Measurement CSVMeasurementSource::getMeasurement() {
    std::string line;
    if (std::getline(file, line)) {
        std::istringstream iss(line);
        std::string temp, press;
        std::getline(iss, temp, ',');
        std::getline(iss, press, ',');
        return {std::stod(temp), std::stod(press)};
    }

    throw std::runtime_error("No more data in CSV file");
}


MeasurementSource* MeasurementSource::createSource(const toml::table& config) {
    const std::string sourceClass = config["sensor"]["measurement_source"].value_or<std::string>("");
    if (sourceClass == "CSVMeasurementSource") {
        return new CSVMeasurementSource(config);
    }

    return nullptr;
}
