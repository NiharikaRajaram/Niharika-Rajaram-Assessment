# Niharika-Rajaram-Assessment

A Python Script to parse a log file and find the corresponding outputs as per the requirements.

## Table of Contents
- [Requirements](#requirements)
- [Assumptions](#assumptions)
- [Execution](#Execution)
- [Observations](#Observations)

## Requirements
- Parse a file containing flow log data and map each row to a tag based on the lookup table. 
- Also display the counts of dst_port and protocol combinations.

## Assumptions
- This code supports only default log format for logs.txt.
- Version supported is 2 for logs.txt. Format is exactly the same as provided in the link https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html#flow-logs-custom
- Protocol mapping are obtained from the CSV file provided in the link https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
-  If any field while creating the tag lookup table is empty, the tag for the dst_port and protocol will not be created.
- sv_P1 and sv_p1 are treated the same since case insensitive matching is performed here. The output tags will contain the lower case version.

## Execution
- Either clone the project or download the Zip of project, unzip it and follow the following instructions.
- Input files are available in the folder named data/input.
- Ouput files will be written in the folder named data/output once the code is executed.
- Programming language - Python 3.12
- Dependencies - None (Default Python package named 'csv' is used)
- To run the code, you need to be in the folder named Niharika-Rajaram-Assessment and run the following command
`python process_data.py` (or `python3 process_data.py` as per your local system configuration)

### data/input 
- `logs.txt`: Contains flow log data
- `lookup.csv`: Contains the lookup table for tags
- `protocol-numbers-1.csv`:  Contains the protocol numbers and the corresponding protocols. Downloaded from https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml 

###  data/output
- `tag_counts.csv`: Contains the tags and their counts
- `port_protocol_counts.csv`: Contains the dst_ports, protocols and their counts
- `consolidated_output.csv`: File containing the above two outputs together

## Observations
- Performed tests to eliminate all possibile error scenarios such as case sensitivity, empty fields and incorrect counts.
- Code has been written using modular approach and comments have been provided for better understanding and convenience.
- Hashmaps are the prmimary data structure that is used as they operate on O(1) time complexity and performance of the code is better with the use of hashmaps (AKA dictionary in Python).

