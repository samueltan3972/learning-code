# CPP Example

## build

```bash
mkdir build
cd build
cmake ..
cmake --build . -- -j   # same like make ., but cmake --build will help determine what is the underlying build system

# conan (install and build dependency) - at repo directory
conan install . \
    --output-folder ./build/gcc11__x86_64-pc-linux-elf__release \
    --profile:host  ./tools/conan/gcc11__x86_64-pc-linux-elf__release \
    --profile:build ./tools/conan/gcc11__x86_64-pc-linux-elf__release \
    --build missing

cd ./build/gcc11__x86_64-pc-linux-elf__release

cmake -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_TOOLCHAIN_FILE=./conan_toolchain.cmake ../../
cmake --build . -- -j   # rebuild the project
```

## build with test

```bash
rm -rf build

conan install . \
    --output-folder ./build/gcc11__x86_64-pc-linux-elf__release \
    --profile:host  ./tools/conan/gcc11__x86_64-pc-linux-elf__release \
    --profile:build ./tools/conan/gcc11__x86_64-pc-linux-elf__release \
    --build missing

cd ./build/gcc11__x86_64-pc-linux-elf__release

cmake -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_TOOLCHAIN_FILE=./conan_toolchain.cmake ../../
cmake --build . -- -j

# running benchmark
./build/gcc11__x86_64-pc-linux-elf__release/source/lib/bench/cpp-example-lib-bench
```

## static code analysis

```bash
rm -rf build

conan install . \
    --output-folder ./build/clang14__x86_64-pc-linux-elf__release \
    --profile:host  ./tools/conan/clang14__x86_64-pc-linux-elf__release \
    --profile:build ./tools/conan/clang14__x86_64-pc-linux-elf__release \
    --build missing

cd ./build/clang14__x86_64-pc-linux-elf__release

cmake -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_TOOLCHAIN_FILE=./conan_toolchain.cmake -DANALYSIS=clang-tidy ../../
cmake --build . -- -j
```

## Clang

```bash
# Remember to install Clang
sudo apt update
sudo apt install clang-14
```

## Sanitizer

```bash
rm -rf build

conan install . \
    --output-folder ./build/clang14__x86_64-pc-linux-elf__release \
    --profile:host  ./tools/conan/clang14__x86_64-pc-linux-elf__release \
    --profile:build ./tools/conan/clang14__x86_64-pc-linux-elf__release \
    --build missing

cd ./build/clang14__x86_64-pc-linux-elf__release

cmake -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_TOOLCHAIN_FILE=./conan_toolchain.cmake -DSANITIZER=asan ../../
cmake --build . -- -j
./build/clang14__x86_64-pc-linux-elf__release/source/app/cpp-example-app
```