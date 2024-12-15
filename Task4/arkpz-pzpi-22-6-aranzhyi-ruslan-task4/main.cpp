#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <toml++/toml.h>
#include <cpr/cpr.h>

typedef struct Measurement {
    double temperature;
    double pressure;
} Measurement;

class MeasurementSource {
public:
    explicit MeasurementSource(const toml::table& config) {
    };
    virtual ~MeasurementSource() = default;
    virtual Measurement getMeasurement() = 0;

    static MeasurementSource* createSource(const toml::table& config);
};

class CSVMeasurementSource final : public MeasurementSource {
public:
    explicit CSVMeasurementSource(const toml::table& config) : MeasurementSource(config) {
        const auto filename = config["source.csv.file_path"].value<std::string>();
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

    Measurement getMeasurement() override {
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

private:
    std::ifstream file;
};

MeasurementSource* MeasurementSource::createSource(const toml::table& config) {
    const std::string sourceClass = config["sensor.measurement_source"].value_or<std::string>("");
    if (sourceClass == "CSVMeasurementSource") {
        return new CSVMeasurementSource(config);
    }

    return nullptr;
}

class IotSensor {
public:
    explicit IotSensor(const toml::table& config) {
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

        for(int i = 0; i < measurements_count; ++i) {
            this->last_measurements[i].temperature = this->last_measurements[i].pressure = 0;
        }
    }

    void run() {
        while(true) {
            const Measurement ms = this->source->getMeasurement();
            sendData(ms);
            memcpy(last_measurements + 1, last_measurements, sizeof(Measurement) * (measurements_count - 1));
            last_measurements[0] = ms;

            // TODO: make forecast

            sleep(measurement_interval);
        }
    }

private:
    std::string api_host;
    std::string api_key;
    uint32_t measurement_interval;

    MeasurementSource* source;
    uint16_t measurements_count;
    Measurement* last_measurements;

    void sendData(Measurement measurement) {
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
};

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
