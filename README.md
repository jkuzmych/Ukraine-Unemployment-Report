# Unemployment Rates in Ukraine

A web application for visualizing unemployment data in Ukraine. This project provides interactive charts showing unemployment statistics by social groups, regions, and comparing real vs. registered unemployment.

## Features

- **Unemployment Rate by Social Group**: Visualizes unemployment rates and absolute numbers broken down by gender (Men/Women) and area type (Urban/Rural)
- **Real vs. Registered Unemployment**: Compares actual unemployment numbers with officially registered unemployment
- **Unemployment by Regions**: Displays unemployment rates across different regions of Ukraine
- **Interactive Charts**: Interactive line charts with legend toggling
- **Data Sources**: Data sourced from UkrStat and Ministry of Finance of Ukraine

## Tech Stack

- **Frontend**: React 19, TypeScript
- **Build Tool**: Vite
- **Charts**: Recharts
- **Data Processing**: Python (pandas)
- **Styling**: CSS

## Project Structure

```
.
├── data/                          # Raw Excel data files
├── frontend/
│   └── uud/                      # React application
│       ├── public/
│       │   └── data/             # Processed JSON data files
│       ├── src/
│       │   ├── components/       # React components
│       │   ├── hooks/            # Custom React hooks
│       │   ├── App.tsx           # Main application component
│       │   └── main.tsx          # Application entry point
│       └── package.json
├── prepare_unemp_by_categories_json.py    # Data processing script
├── prepare_unemp_by_regions_json.py       # Data processing script
├── prepare_unemp_real_registered.py       # Data processing script
└── README.md
```

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn
- Python 3.x with pandas (only to rewrite jsons)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd "Unemployment Rates"
```

2. Install frontend dependencies:
```bash
cd frontend/uud
npm install
```

### Data Processing (Optional)

If you need to regenerate the JSON data files from Excel sources:

1. Ensure you have the raw Excel files in the `data/` directory
2. Install Python dependencies:
```bash
pip install pandas openpyxl
```

3. Run the data processing scripts:
```bash
python prepare_unemp_by_categories_json.py
python prepare_unemp_by_regions_json.py
python prepare_unemp_real_registered.py
```

The processed JSON files will be generated in `frontend/uud/public/data/`.

### Running the Application

1. Start the development server:
```bash
cd frontend/uud
npm run dev
```

2. Open your browser and navigate to the URL shown in the terminal (typically `http://localhost:5173`)

### Building for Production

```bash
cd frontend/uud
npm run build
```

The production build will be in the `dist/` directory.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run typecheck` - Run TypeScript type checking

## Data Sources

- **UkrStat**: [Official Statistics Portal of Ukraine](https://www.ukrstat.gov.ua/)
- **Ministry of Finance**: [Ministry of Finance of Ukraine](https://index.minfin.com.ua/)

## Notes on Data

- Data excludes temporarily occupied territories (Crimea, Sevastopol, and parts of Donetsk and Luhansk regions)
- Unemployment rates are calculated using ILO (International Labor Organization) methodology
- Data frequency varies by chart (quarterly or yearly)
- See the Notes section in each chart view for detailed information

## License

MIT License - Copyright (c) 2025 Yuliia Kuzmych

