import csv

# read CSV file
def read_csv(filename):
    try:
        with open(filename, mode='r') as csv_file:
            data = []
            reader = csv.DictReader(csv_file)
            for line in reader:
                data.append(line)
        return data
    except:
        print(f"Error: File '{filename}' does not exist")
        return None

# Create Protocol map using data from protcol-numbers-1 file    
def create_protocol_map(filename):
    protocol_data = read_csv(filename)
    if protocol_data == None:
        return None
    protocol_map = ['UNASSIGNED' for i in range(256)]
    for row in protocol_data:
        decimal = row.get('Decimal', 'Default')
        keyword = row.get('Keyword', 'UNASSIGNED')
        if decimal.isdigit() and len(keyword) > 0:
            protocol_map[int(decimal)] = keyword
    return protocol_map

# Create a tag look table using data from lookup.csv file
def create_tag_lookup_table(filename):
    tag_data = read_csv(filename)
    if tag_data == None:
        return None
    tag_lookup_table = {}
    for row in tag_data:
        dst_port = row.get('dstport', 'INVALID')
        protocol = row.get('protocol', 'INVALID')
        tag = row.get('tag', 'INVALID')
        if dst_port != 'INVALID' and protocol != 'INVALID' and tag != 'INVALID':
            concatenated_keyword = dst_port + '--' + protocol
            tag_lookup_table[concatenated_keyword] = tag
    return tag_lookup_table

# Read text file - logs.txt
def read_txt(filename):
    txt_data = []
    with open(filename, mode='r') as file:
        txt_data = file.readlines()
    return txt_data

# Process logs to create two counters for outputs
def process_logs(filename):
    protocol_map = create_protocol_map('data/input/protocol-numbers-1.csv')
    tag_lookup_table = create_tag_lookup_table('data/input/lookup.csv')

    if tag_lookup_table == None or protocol_map == None:
        return None

    tags_counter = {}
    dst_port_protocol_counter = {}

    logs = read_txt(filename)

    for log in logs:
        split_log = log.strip().split(' ')
        # check to ensure dst_port and protocol fields are present and protocol is a digit
        if len(split_log) == 14 and split_log[7].isdigit() and all(word.strip() for word in split_log):
            dst_port = split_log[6]
            protocol_number = int(split_log[7])
            protocol = protocol_map[protocol_number].lower()

            concatenated_dst_port_protocol = dst_port + '--' + protocol
            # check for case sensitivity
            tag = tag_lookup_table.get(concatenated_dst_port_protocol, 'Untagged').lower()
            # increment counter based on presence of the ds_port, protocol combination
            if concatenated_dst_port_protocol not in dst_port_protocol_counter:
                dst_port_protocol_counter[concatenated_dst_port_protocol] = 0
            dst_port_protocol_counter[concatenated_dst_port_protocol] += 1
            # increment counter based on presence of tag
            if tag not in tags_counter:
                tags_counter[tag] = 0
            tags_counter[tag] += 1
        else:
            print(split_log)
            print("Check if the dst_port and protocol fields are present and protocol is a number. Check for the default format of logs")
            return
    output_1 = [["Port", "Protocol", "Count"]]
    print(output_1[0])
    for key in dst_port_protocol_counter.keys():
        dst_port, protocol = key.split('--')
        count = dst_port_protocol_counter[key]
        print([dst_port, protocol, count])
        output_1.append([dst_port, protocol, count])
    
    print("_______________________________________________")

    output_2 = [["Tag", "Count"]]
    print(output_2[0])
    for key in tags_counter.keys():
        print([key, tags_counter[key]])
        output_2.append([key, tags_counter[key]])

    output_3 = output_2 + [' '] + output_1

    write_output('data/output/tag_counts.csv', output_2)
    write_output('data/output/port_protocol_counts.csv', output_1)
    write_output('data/output/consolidated_output.csv', output_3)

# write files in the output directory
def write_output(filename, data):
    with open(filename, mode='w', newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

process_logs('data/input/logs.txt')


