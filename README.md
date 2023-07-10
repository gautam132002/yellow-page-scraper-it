# Yellow Page Scraper Italy

A GUI scraper for the website [Pagine Gialle](https://www.paginegialle.it/), designed to extract information based on user input from a CSV file. The scraper utilizes a simple PyQt5 interface to facilitate the selection of an input CSV file (semicolon-separated) with two columns: job profession and state (or zip code of the state). It then generates a CSV file (semicolon-separated) containing all possible matches for each row in the input file.

## Features

The yellow-page-scraper-italy tool extracts the following information from each match:

- RAGIONE SOCIALE (Business Name)
- INDIRIZZO (Address)
- PROVINCIA (Province)
- COMUNE (City)
- CAP (Postal Code)
- TELEFONO (Phone Number)
- WHATSAPP (WhatsApp Number)
- EMAIL (Email Address)
- SITO INTERNET (Website)
- DETAILS LINK (Link to detailed information)

## Requirements

To run the yellow-page-scraper-italy, ensure that you have the following requirements installed:

- Python 3.x

You can install the required packages by running the following command:

```bash
pip install -r req.txt
```

## Getting Started
1. Clone the repository to your local machine.
2. Activate the virtual environment by running the following command:
   
```bash
source bin/activate
```

3. Launch the scraper GUI by executing the following command:
   
```bash
python scrapper.py
```
4. Use the GUI to select the input CSV file containing the job professions and states.
   
After selecting the file, the scraper will generate a CSV file with the extracted information.

## Examples csv

1. input => in.csv , output => in_result.csv
2. input => EDILI Milano.csv, output => EDILI Milano_result.csv

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
  This project is licensed under the MIT License.
  Feel free to modify and customize the README to better suit your project.





