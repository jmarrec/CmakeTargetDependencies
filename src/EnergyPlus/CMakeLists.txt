configure_file("${PROJECT_SOURCE_DIR}/idd/Energy+.idd.in" "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/Energy+.idd")

add_custom_command(
        OUTPUT "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/Energy+.schema.epJSON"
        COMMAND ${Python_EXECUTABLE} "${PROJECT_SOURCE_DIR}/scripts/dev/generate_epJSON_schema/generate_epJSON_schema.py" "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}"
        MAIN_DEPENDENCY "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/Energy+.idd"
        VERBATIM
)

add_custom_target(epjson_schema ALL DEPENDS "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/Energy+.schema.epJSON")
set_target_properties(epjson_schema PROPERTIES FOLDER "Internal")

add_custom_command(
  OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/EmbeddedEpJSONSchema.cc"
  COMMAND
    ${CMAKE_COMMAND}
        -D "EnergyPlus_SOURCE_DIR:PATH=${CMAKE_CURRENT_SOURCE_DIR}"
        -D "EnergyPlus_RUNTIME_OUTPUT_DIRECTORY:PATH=${CMAKE_RUNTIME_OUTPUT_DIRECTORY}"
        -D "EnergyPlus_BINARY_DIR:PATH=${CMAKE_CURRENT_BINARY_DIR}"
        -D "EnergyPlus_CURRENT_BINARY_DIR:PATH=${CMAKE_CURRENT_BINARY_DIR}"
        -D "EnergyPlus_embeddable_epJSON_schema:PATH=$<TARGET_FILE:generate_embeddable_epJSON_schema>"
        -P "${PROJECT_SOURCE_DIR}/scripts/dev/generate_embeddable_epJSON_schema/generate_embedded_epJSON_schema.cmake"
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
  DEPENDS
    generate_embeddable_epJSON_schema
    # "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/Energy+.schema.epJSON" # File-level dependency
    epjson_schema                                             # target-level dependency, to avoid race conditions
    "${CMAKE_CURRENT_SOURCE_DIR}/InputProcessing/EmbeddedEpJSONSchema.in.cc"
  VERBATIM)


add_custom_target(embedded_epjson_source ALL DEPENDS "${CMAKE_CURRENT_BINARY_DIR}/EmbeddedEpJSONSchema.cc")
set_target_properties(embedded_epjson_source PROPERTIES FOLDER "Internal")

add_library(energyplusparser STATIC parser.cc)
add_dependencies(energyplusparser embedded_epjson_source)

add_library(energypluslib STATIC lib.cc)
add_dependencies(energypluslib embedded_epjson_source)

add_library(energyplusapi STATIC CommandLineInterface.cc)
target_link_libraries(energyplusapi PRIVATE energypluslib)

add_executable(energyplus main.cc)
target_link_libraries(energyplus PRIVATE energyplusapi project_options project_fp_options project_warnings)
