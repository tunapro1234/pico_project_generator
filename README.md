# Pico Project Generator
Raspberry Pi pico için proje oluşturan bir script.
Her seferinde python3 pico_gen_makefile.py yazmakla uğraşmamak için bash alias eklenebilir.
Proje klasörü içinde `Makefile`, `main.c`, `generate_cmake.py` adlarında 3 dosya oluşturuluyor.
Daha sonra build klasörü içine gerekli kurulumları yapıyor.


## Kullanım
```python3 pico_gen_makefile.py <path_to_project_folder>/<project_name>```

### Derleme
Proje klasörü içindeyken `make compile` ya da build klasörü içinde `make` komutu ile yapılabilir.

### Yükleme
Raspberry pi pico /mnt/pico klasörüne mountlanırsa `make upload` komutu kullanılabilir.
Mount klasörünü proje klasöründeki Makefileı düzenleyerek değiştirebilirsiniz
