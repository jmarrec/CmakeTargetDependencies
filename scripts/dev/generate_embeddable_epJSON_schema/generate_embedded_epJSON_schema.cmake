execute_process(
  COMMAND "${EnergyPlus_embeddable_epJSON_schema}" "${EnergyPlus_RUNTIME_OUTPUT_DIRECTORY}/Energy+.schema.epJSON"
  TIMEOUT 90
  RESULT_VARIABLE generate_embedded_epJSON_schema
  OUTPUT_VARIABLE embedded_epJSON_schema
)
message(AUTHOR_WARNING "generating embedded epJSON schema")
if(${generate_embedded_epJSON_schema} MATCHES ".*timeout.*")
  message(FATAL_ERROR "Generating embedded epJSON Schema from epJSON Schema failed: ${generate_embedded_epJSON_schema}")
endif()
configure_file("${EnergyPlus_SOURCE_DIR}/InputProcessing/EmbeddedEpJSONSchema.in.cc" "${EnergyPlus_CURRENT_BINARY_DIR}/EmbeddedEpJSONSchema.cc")
