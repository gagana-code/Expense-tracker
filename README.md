# 💰 Expense Tracker

A simple desktop **Expense Tracker** built with Python's `tkinter` for the GUI and `matplotlib` for visual analytics. Add, view, and delete expenses, and see a live pie-chart breakdown of your spending by category — all backed by a local JSON file, no database or internet connection required.

## Features

- 📝 **Add expenses** with date, amount, category, and description
- 🗑️ **Delete** selected expense entries (auto re-indexes IDs)
- 📊 **Transactions tab** — sortable table view of all recorded expenses
- 📈 **Analytics Dashboard tab** — live pie chart of spending by category
- ✅ **Input validation** for date format (`YYYY-MM-DD`) and amount (positive number)
- 💾 **Persistent storage** — expenses are saved to `expenses.json` and reloaded automatically on launch

## Tech Stack

| Component     | Technology              |
|---------------|--------------------------|
| GUI           | `tkinter`, `ttk`         |
| Charts        | `matplotlib`             |
| Data storage  | JSON (`expenses.json`)   |
| Language      | Python 3.9+              |

## Project Structure

```
Expense-Tracker/
├── main.py           # Application entry point (GUI + logic)
├── expenses.json      # Auto-generated data file (created on first run)
├── requirements.txt   # Python dependencies
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.9 or higher
- `tkinter` (bundled with most standard Python installs; on Linux you may need to install it separately — see below)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/expense-tracker.git
   cd expense-tracker
   ```

2. **(Optional but recommended) create a virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   > **Linux users:** `tkinter` isn't installed via pip. Install it via your package manager first, e.g.:
   > ```bash
   > sudo apt-get install python3-tk
   > ```

### Running the app

```bash
python main.py
```

The application window will open. Expense data is stored in `expenses.json` in the project directory and will persist between runs.

## Usage

1. Fill in the **Date**, **Amount**, **Category**, and **Description** fields on the left panel.
2. Click **Add Expense** to save the entry — it will immediately appear in the **Transactions** tab and update the **Analytics Dashboard** pie chart.
3. To remove an entry, select a row in the **Transactions** table and click **Delete Selected**.

## Roadmap / Ideas for Contribution

- [ ] Filter/search expenses by date range or category
- [ ] Export data to CSV/Excel
- [ ] Monthly spending trend (line chart) in addition to the category pie chart
- [ ] Edit existing expense entries
- [ ] Multi-currency support

Contributions and pull requests are welcome!

## License

This project is licensed under the MIT License — feel free to use and modify it.
