# Conan Cheat Sheet

Here's a **Conan (C++ package manager) Cheat Sheet** to help you quickly recall essential commands and concepts:

---

## 🧩 Basic Concepts

| Concept | Description |
|--------|-------------|
| **Package** | A C++ library with metadata (name, version, settings, etc.) |
| **Recipe** | `conanfile.py` or `conanfile.txt` describing how to build/package |
| **Remote** | A repository where packages are stored (e.g., `conancenter`) |
| **Profile** | Compilation settings (compiler, version, architecture, etc.) |

---

## 🔧 Common Commands

### 📦 Installing Packages

```bash
conan install .         # Install using conanfile in current dir
conan install . -if build # Install to 'build' folder
conan install . --build=missing  # Build missing packages from source
```

### 🏗️ Creating Packages

```bash
conan create .          # Create a package from current dir
conan create . user/channel  # With user/channel info
```

### 🔁 Building Locally

```bash
conan build .           # Build using local recipe and source
```

### 🔍 Searching

```bash
conan search            # List installed packages
conan search zlib       # Search local packages
conan search zlib -r=conancenter  # Search remote
```

### 🌐 Managing Remotes

```bash
conan remote list
conan remote add myremote https://my.repo.url
conan remote remove myremote
```

### 🧪 Profiles

```bash
conan profile list
conan profile show default
conan profile new myprofile --detect
conan profile update settings.compiler=gcc myprofile
```

---

## 📁 File Structure

### `conanfile.txt` example

```ini
[requires]
fmt/9.1.0

[generators]
cmake
```

### `conanfile.py` example (minimal)

```python
from conan import ConanFile

class HelloConan(ConanFile):
    name = "hello"
    version = "1.0"
    settings = "os", "compiler", "build_type", "arch"
    requires = "fmt/9.1.0"
    generators = "CMakeToolchain", "CMakeDeps"
```

---

## 🛠️ Integration with CMake

```cmake
include(${CMAKE_BINARY_DIR}/conan_toolchain.cmake)
find_package(fmt REQUIRED)
```

---

## 📤 Uploading Packages

```bash
conan upload hello/1.0@user/channel --all -r=myremote
```

---

## 🧹 Cleanup

```bash
conan remove "*" -f           # Remove all local packages
conan remove "pkg/*" -p pkgid # Remove specific package ID
```

---

## 🐳 Docker Integration (Bonus)

```bash
conan profile detect --force
conan create . --profile:build=default --profile:host=default
```
