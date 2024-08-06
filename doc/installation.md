(installation)=
# Installing

<!--* freshness: { reviewed: '2024-06-18' } *-->

Using JAX requires installing two packages: `jax`, which is pure Python and
cross-platform, and `jaxlib` which contains compiled binaries, and requires
different builds for different operating systems and accelerators.

**TL;DR** For most users, a typical JAX installation may look something like this:

* **CPU-only (Linux/macOS/Windows)**
  ```
  pip install -U jax
  ```
* **GPU (NVIDIA, CUDA 12)**
  ```
  pip install -U "jax[cuda12]"
  ```

* **TPU (Google Cloud TPU VM)**
  ```
  pip install -U "jax[tpu]" -f https://storage.googleapis.com/jax-releases/libtpu_releases.html
  ```

(install-supported-platforms)=
## Supported platforms

The table below shows all supported platforms and installation options. Check if your setup is supported; and if it says _"yes"_ or _"experimental"_, then click on the corresponding link to learn how to install JAX in greater detail.