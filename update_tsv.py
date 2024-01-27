import argparse
import csv
import xml.etree.ElementTree as ET

def decode_shift_jis(hex_string): # decoding function which converts music_info.xml name_string to JIS
    bytes_object = bytes.fromhex(hex_string)
    return bytes_object.decode("shift_jisx0213")

def load_music_info_xml(music_info_xml):
    global body
    tree = ET.parse(music_info_xml) #load music_info.xml
    root = tree.getroot()
    body = root.find('body') # Look at <body> which then contains <music_id> and <name_string>

def create_music_info_tsv(filename): # create music_info.tsv
    with open('music_info.tsv', mode='w', newline='', encoding='utf-8') as tsv_file:
        writer = csv.writer(tsv_file, delimiter='\t')
        # writer.writerow(['Music ID', 'Name String'])

        for data in body.findall('data'):
            try:
                music_id = data.find('music_id').text
                name_string_hex = data.find('name_string').text
                name_string = decode_shift_jis(name_string_hex)
                writer.writerow([music_id, name_string])
            except Exception as e:
                print(f"Error processing data: {e}")

def read_tsv(filename):
    ids = []
    names = []
    with open(filename) as file:
        tsv_file = csv.reader(file, delimiter="\t")

        for line in tsv_file:
            ids.append(str(line[0])) 
            names.append(str(line[1]))
    return ids, names

def main():
 # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Update jubeat.tsv with missing music_ids from output.tsv')
    parser.add_argument('--xml', help='Path to the XML file (default: music_info.xml)', default='music_info.xml')
    parser.add_argument('--tsv', help='Path to the TSV file (default: jubeat.tsv)', default='jubeat.tsv')
    args = parser.parse_args()

    # Load music_info.xml
    load_music_info_xml(args.xml)

    # Create music_info.tsv
    create_music_info_tsv(args.xml)

    # Grab IDs and names
    music_info_id_list, music_info_name_list = read_tsv('music_info.tsv')
    jubeat_tsv_id_list, justbeat_tsv_name_list = read_tsv('jubeat.tsv')

    # Figure out which IDs are missing
    missing_info = []
    for i in range(len(music_info_id_list)):
        if music_info_id_list[i] not in jubeat_tsv_id_list:
            missing_info.append((music_info_id_list[i],music_info_name_list[i]))

    with open('jubeat.tsv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        rows = list(reader)
        
    for i in missing_info:
        rows.append(i)

    sorted_rows = sorted(rows, key=lambda x: int(x[0]))
    with open('jubeat_new.tsv', 'w', newline='', encoding='utf-8') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
        writer.writerows(sorted_rows)
        tsvfile.close()

    print(len(missing_info), "missing IDs added to jubeat.tsv")
if __name__ == "__main__":
    main()