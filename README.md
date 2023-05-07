# SpendWise

This is a Python-based expense tracker that allows users to keep track of their expenses and visualize them using pie charts. It uses the \`tkinter\` library for creating a graphical user interface, \`matplotlib\` for creating pie charts, and \`sqlite3\` for managing the database.

## Features

- Add, edit, and delete expenses
- View expenses by date range and category
- View expenses as pie charts

# Screenshots
### Entry Screen:
![Entry Screen](https://lh3.googleusercontent.com/drive-viewer/AFGJ81qwK_MeefPE1wREYA7Xk7DkyB4N5yeyE8p8qmfPpTQdyiGm-U27MIo1wCsu-3o_9uqoWGqoQoilD4Rrp7qWmUY6k0e2=w1920-h941)
### Main Screen:
![Main Screen](https://lh3.googleusercontent.com/drive-viewer/AFGJ81pv67yyNF7_z_UtOKWasXUG8lWW_35vxwQUPR095v00ec5sHcNEIwqpXqCN_GPxwDMOaiKfuDLgotoiUCPYXLLAEwt8jg=w1920-h941)
### Pie Chart:
![Pie Chart](https://lh3.googleusercontent.com/drive-viewer/AFGJ81p02cVjN96rkgcaNGvCdG31Velil623G1XasCUAUUkwTD3LsyAXvMxCNszzRjQbdqcV2nTtWaveUVfKm_FqPNuhLy1KQQ=w1920-h941)
### Adjusting Balance:
![Pie Chart](https://lh3.googleusercontent.com/drive-viewer/AFGJ81rLpC7bZ6xh9EmKmlIn75tmFhuw3rmmFIEP0lVEOYK3TCGoEZgWIxMFm_asu89-STVNlaSn9KrEyzxmPsqplsR-gkGG=w1920-h941)

## Requirements

- Python 3.x
- \`tkinter\` library
- \`matplotlib\` library
- \`sqlite3\` library

## Installation

1. Clone the repository:

   \`\`\`
   git clone https://github.com/A-4-Atom/spendwise.git
   \`\`\`

2. Install the required libraries using pip:

   \`\`\`
   pip install tkinter matplotlib sqlite3
   \`\`\`

## Usage

1. Navigate to the project directory in the terminal:

   \`\`\`
   cd spendwise
   \`\`\`

2. Run the application:

   \`\`\`
   python main .py
   \`\`\`

3. Use the GUI to add, edit, and delete expenses, as well as view expenses by date range and category.

## Database

The application uses an sqlite3 database to store expense data. The database is created automatically when the application is run for the first time, and is stored in a file called \`test.db\` in the project directory. Also the application automatically creates a text file named \`initialAmount.db\` to store the total balance.

## Credits

This project was created by \`Gunjan\` as a personal project. It uses the \`tkinter\`, \`matplotlib\`, and \`sqlite3\` libraries, which are all open source.
