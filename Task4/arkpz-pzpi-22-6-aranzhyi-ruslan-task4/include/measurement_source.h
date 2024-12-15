#pragma once

#include <toml++/toml.hpp>
#include "measurement.h"

class MeasurementSource {
public:
    explicit MeasurementSource(const toml::table& config) {};
    virtual ~MeasurementSource() = default;
    virtual Measurement getMeasurement() = 0;

    static MeasurementSource* createSource(const toml::table& config);
};


class CSVMeasurementSource final : public MeasurementSource {
public:
    explicit CSVMeasurementSource(const toml::table& config);
    Measurement getMeasurement() override;

private:
    std::ifstream file;
};
