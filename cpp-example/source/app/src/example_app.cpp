#include <iostream>
#include <memory>

#include "cpp-example/example_lib.hpp"

int main() {
  auto lib = std::make_shared<cppexample::ExampleLib>(12);

  std::cout << lib->Add(4) << std::endl;

  return 0;
}