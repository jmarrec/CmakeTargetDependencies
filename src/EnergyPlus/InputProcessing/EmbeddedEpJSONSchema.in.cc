#include <array>

namespace EnergyPlus {

namespace EmbeddedEpJSONSchema {

// clang-format off
    ${embedded_epJSON_schema}
// clang-format on

const gsl::span<const std::uint8_t> embeddedEpJSONSchema() {
  return gsl::span<const std::uint8_t>(embeddedSchema);
}

const std::string_view embeddedEpJSONSchemaView() {
  static const std::string str(embeddedSchema.begin(), embeddedSchema.end());
  return str;
}

}  // namespace EmbeddedEpJSONSchema

}  // namespace EnergyPlus
