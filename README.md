# <div align="center"><b>📄 requirementsHelper 🐍</b></div>

</hr>

## <div align="center"> Tool for updating your `requirements.txt` file to match the versions of the packages you currently have installed.</div>

</hr>

## 📂 Features

- **Version Comparison**: Compares package versions in your `requirements.txt` with the installed versions.
- **Visual Feedback**: 
  - Displays packages that are "Up to date" in the default color.
  - Highlights packages with a "Different version" in yellow.
  - Highlights missing or uninstalled packages in red.
- **Automatic Update**: Optionally update your `requirements.txt` to reflect the installed package versions.

## ⬇️ Installation

1. Ensure you have [Python 3.8+](https://www.python.org/downloads/) installed.
2. Clone the repository:
   ```bash
   git clone https://github.com/PoyBoi/requirementsHelper
   ```
3. Navigate to the project directory:
   ```bash
   cd requirementsHelper
   ```

## 🔧 Usage

Run the script using Python:

```bash
python requirementsHelper.py
```

You will be prompted to enter a path to a `requirements.txt` file or a directory containing one or more requirements.txt files. The tool will then:
- Compare the versions specified in the file with the versions installed in your environment.
- Display the comparison in a formatted table with color-coded statuses.
- Prompt you to update the requirements.txt file if discrepancies are found.

### 🗃️ Example Output

```mathematica
Enter the path to requirements.txt file or directory containing requirements.txt: </path/to/your/project>
Using requirements file: /path/to/your/project/requirements.txt

Comparing requirements.txt with installed packages:
------------------------------------------------------------------------------------
Package                                  Required       Installed       Status
------------------------------------------------------------------------------------
python-dateutil                          2.9.0.post0    2.9.0.post0     Up to date
pytz                                     2024.2         2024.2          Up to date
opencv-python                            4.10.0.84      Not installed   Missing
lxml                                     4.9.4          Not installed   Missing
typing-extensions                        4.12.2         Not installed   Missing
python-dotenv                            1.0.1          Not installed   Missing
llama-index-llms-llama-cpp               0.4.0          Not installed   Missing
llama-index-llms-huggingface             0.4.2          0.4.2           Up to date
```

In the output above:
- Yellow indicates a package with a different version than required.
- Red indicates a package that is missing or not installed.

## 🤓 Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.