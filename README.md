## Introduction

1. My installation is based on miniconda and additional packages. Use
   the following command after downloading the repository to get your
   environment ready. The file that contains all the packages used is
   [requirements.txt](requirements.txt)
   
		conda create --name <env> --file requirements.txt
		
2. For this "work task" I have worked on 

	- Assignment 1: G2 Scraper
	- Assignment 3: Duplicates detection

## Assignment1 instructions

After installation of `requirement.txt`, please install the
appropriate [chrome-driver](https://chromedriver.chromium.org/downloads) for your chrome browser. And point to
it's unzipped location in the `path` variable in
[assignment1\_final.py](assignment1_final.py). Currently it points to:

	path = "../dater/driver/chromedriver"
	
The code can then be run.

**The structure of the code is as follows**:

1. Import statements
2. Definition of all functions used
3. Actual script running all the functions

## Assignment 3 instructions

Just running the `.py` file should be sufficient.

## Files

1. [assignment\_1\_and\_3\_documentation.md](assignment_1_and_3_documentation.markdown): Documentation of the question,
method, code logic for both Assignment 1 and Assignment 3 can be found
here.

2. [assignment1\_final.py](assignment1_final.py): Python file showing the G2 Scraping.

3. [assignment1\_output.csv](assignment1_output.csv): Output.csv of the modified data

4. [assignment3\_final.py](assignment3\_final.py): Python file showing the duplicates detection.

5. [assignment3\_output.csv](assignment3_output.csv): Output.csv of the duplicates alone.


