# Tubes1-learning_rate
Program penjadwalan kelas mingguan dengan pendekatan _Local Search_ menggunakan Bahasa Python

---

<!-- CONTRIBUTOR -->
 <div align="center" id="contributor">
   <strong>
     <h3> learning_rate (K2) </h3>
     <table align="center">
       <tr align="center">
         <td>NIM</td>
         <td>Name</td>
         <td>GitHub</td>
       </tr>
       <tr align="center">
         <td>13523004</td>
         <td>Razi Rachman Widyadhana</td>
         <td align="center" >
           <div style="margin-right: 20px;">
           <a href="https://github.com/zirachw" ><img src="https://avatars.githubusercontent.com/u/148220821?v=4" width="48px;" alt=""/> 
             <br/> <sub><b> @zirachw </b></sub></a><br/>
           </div>
         </td>
       </tr>
       </tr>
       <tr align="center">
         <td>13523074</td>
         <td>Ahsan Malik Alfarisi</td>
         <td align="center" >
           <div style="margin-right: 20px;">
           <a href="https://github.com/ahsuunn" ><img src="https://avatars.githubusercontent.com/u/141555703?v=4" width="48px;" alt=""/> 
             <br/> <sub><b> @ahsuunn </b></sub></a><br/>
           </div>
         </td>
       </tr>
       <tr align="center">
         <td>13523118</td>
         <td>Farrel Athalla Putra</td>
         <td align="center" >
           <div style="margin-right: 20px;">
           <a href="hhttps://github.com/farrelathalla" ><img src="https://avatars.githubusercontent.com/u/130957219?v=4" width="48px;" alt=""/> 
             <br/> <sub><b> @farrelathalla </b></sub></a><br/>
           </div>
         </td>
       </tr>
     </table>
   </strong>
 </div>

<div align="center">
  <h3 align="center"> Tech Stacks </h3>

  <p align="center">
    
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)][python-url]
  
  </p>
</div>

---

### Deskripsi

Repository ini dibuat untuk memenuhi Tugas Besar 1 Mata Kuliah Intelegensi Artifisial 2025/2026. Repository ini mengandung program yang berfungsi untuk melakukan penjadwalan kelas dari mata kuliah sesuai dengan jumlah sksnya menggunakan konsep Local Search melalui antarmuka GUI. Adapun algoritma yang diimplementasi dalam program ini yaitu:
1. Steepest Ascent Hill Climbing
2. Random Restart Hill Climbing
3. Sideways Hill Climbing
4. Stochastic Hill Climbing
5. Simulated Annealing
6. Genetic Algorithm

---

### Installation <a name="install"></a>

> [!NOTE]  
> Before you start, install these dependencies first with links given :D
> - [**Git**](Git-url) - 2.47.0 or later
> - [**Python**](python-url) - 1.87.0
> - [**uv**](uv-url) - 0.9.4

### Initialization

- **Clone the repository**

  ```
  git clone https://github.com/zirachw/Tubes1-learning_rate.git
  ```

- **Buat virtual environment dengan uv**

  ```bash
  uv venv
  ```

- **Aktifkan venv**

  ```bash
  # Windows:
  .venv\Scripts\activate
  
  # macOS/Linux:
  source venv/bin/activate
  ```

- **Install Dependency Program**

  ```bash
  uv synv
  ```

- **Jalankan antarmuka GUI untuk memulai program**

  ```bash
  # Pastikan berada di root directory
  uv run -m src.main
  ```
---

### Usage <a name="usage"></a>

<br>

1.  Buat `.json` file dengan format berikut:
   ```json
    {
      "kelas_mata_kuliah": [
        {
          "kode": "IF3071_K01",
          "jumlah_mahasiswa": 60,
          "sks": 3
        }
      ],
      "ruangan": [
        {
          "kode": "7609",
          "kuota": 60
        }
      ],
      "mahasiswa": [
        {
          "nim": "13523601",
          "daftar_mk": ["IF3071_K01"],
          "prioritas": [1]
        }
      ]
    }
   ```

2. Pilih algoritma yang ingin dipakai
3. Masukkan parameter tambahan yang mungkin diperlukan oleh algoritma
4. Klik tombol 'Search' dan tunggu hingga program selesai berjalan
5. Hasil pdf report akan muncul di antarmuka GUI yang terurut secara waktu pembuatan dan dapat dilihat dengan cara membuka PDFDialog di dalam GUI dengan 'View Report' atau dapat juga 

---

### Struktur Folder
```
└── Tubes1-learning_rate/
    ├── .gitignore
    ├── .python-version
    ├── pyproject.toml
    ├── README.md
    ├── uv.lock
    ├── test/
    │   ├── algorithm.py
    │   └── state.py
    │
    ├── src/
    │   ├── main.py
    │   ├── utils/
    │   │   ├── parse.py
    │   │   ├── pdf_report.py
    │   │   └── __pycache__/
    │   │       ├── parse.cpython-313.pyc
    │   │       └── pdf_report.cpython-313.pyc
    │   │
    │   ├── ui/
    │   │   ├── main_window.py
    │   │   ├── pdf_viewer.py
    │   │   ├── ui_handlers.py
    │   │   └── __pycache__/
    │   │       ├── main_window.cpython-313.pyc
    │   │       ├── pdf_viewer.cpython-313.pyc
    │   │       └── ui_handlers.cpython-313.pyc
    │   │
    │   ├── core/
    │   │   ├── entity.py
    │   │   ├── state.py
    │   │   └── __pycache__/
    │   │       ├── entity.cpython-313.pyc
    │   │       └── state.cpython-313.pyc
    │   │
    │   ├── algorithm/
    │       ├── genetic_algorithm.py
    │       ├── local_search.py
    │       ├── random_restart_hill_climbing.py
    │       ├── sideways_hill_climbing.py
    │       ├── simulated_annealing.py
    │       ├── steepest_hill_climbing.py
    │       └── stochastic_hill_climbing.py
    │
    ├── output/
    │   ├── report/
    │   │   └── *.pdf
    │   │
    │   └── plot/
    │       └── *.png
    │
    ├── input/
    │   └── *.json
    ├── doc/
    │   └── learning_rate.pdf
    └── .venv/
```

---

### Pembagian Tugas

<div align="center">
<table>
<tr>
<th>Nama</th>
<th>NIM</th>
<th>Workload</th>
</tr>
<tr>
<td>Razi Rachman Widyadhana</td>
<td>13523004</td>
<td>State, Simulated Annealing, Genetic Algorithm</td>
</tr>
<tr>
<td>Ahsan Malik Al Farisi</td>
<td>13523074</td>
<td>Sideways, Random-Restart Hill Climbing, Parser, PDF Report</td>
</tr>
<tr>
<td>Farrel Athalla Putra</td>
<td>13523118</td>
<td>Steepest, Stochastic Hill Climbing, GUI</td>
</tr>
</table>
</div>


<!-- MARKDOWN LINKS & IMAGES -->
[git-url]: https://git-scm.com/
[python-url]: https://www.python.org/
[uv-url]: https://docs.astral.sh/uv/getting-started/installation/

