# 📊 Proyecto Vacunas COVID-19

Dashboard interactivo para visualizar datos de vacunación contra COVID-19 por jurisdicción en Argentina.

## 🚀 Características

- **Gráfico de barras**: Muestra la cantidad de dosis aplicadas por jurisdicción
- **Gráfico circular**: Visualiza la distribución porcentual de dosis entre jurisdicciones
- **Controles interactivos**: Permite alternar entre primera y segunda dosis
- **Diseño responsivo**: Interface limpia y fácil de usar

## 📋 Requisitos

- Python 3.7+
- pip

## ⚙️ Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/julianaalgarin/proyecto_vacunas.git
cd proyecto_vacunas
```

2. Crea un entorno virtual:
```bash
python -m venv .venv
```

3. Activa el entorno virtual:
- Windows: `.venv\Scripts\activate`
- Linux/Mac: `source .venv/bin/activate`

4. Instala las dependencias:
```bash
pip install dash plotly pandas
```

## 🏃‍♀️ Uso

1. Ejecuta la aplicación:
```bash
python index.py
```

2. Abre tu navegador en: http://127.0.0.1:8050

3. Usa los controles para alternar entre primera y segunda dosis

## 📁 Estructura del proyecto

```
proyecto_vacunas/
├── index.py                      # Aplicación principal Dash
├── Covid19VacunasAgrupadas.csv   # Datos de vacunación
├── assets/
│   └── vacuna.png               # Imagen del header
└── README.md                    # Este archivo
```

## 📊 Datos

Los datos incluyen información de vacunación COVID-19 por jurisdicción con las siguientes columnas:
- `jurisdiccion_nombre`: Nombre de la jurisdicción
- `primera_dosis_cantidad`: Cantidad de primeras dosis aplicadas
- `segunda_dosis_cantidad`: Cantidad de segundas dosis aplicadas

## 🛠️ Tecnologías utilizadas

- **Dash**: Framework web para Python
- **Plotly**: Librería de visualización interactiva
- **Pandas**: Manipulación y análisis de datos