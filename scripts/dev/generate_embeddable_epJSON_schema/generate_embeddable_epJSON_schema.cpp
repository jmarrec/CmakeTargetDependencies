#include <iostream>
#include <fstream>
#include <sstream>
#include <cstdio>

int main(int argc, char const* argv[]) {
  if (argc != 2) {
    std::cout << "usage: ./generate_embeddable_schema path/to/Energy+.schema.epJSON";
    return 1;
  }
  std::ifstream schema_stream(argv[1], std::ifstream::in);
  if (!schema_stream.is_open()) {
    std::cout << "schema file path " << argv[1] << " not found" << std::endl;
    return 1;
  }

  std::stringstream buffer;
  buffer << schema_stream.rdbuf();
  const std::string content = buffer.str();

  printf("	static constexpr std::string_view embeddedSchema =  R\"embedded(%s)embedded\";\n", content.data());

  return 0;
}
