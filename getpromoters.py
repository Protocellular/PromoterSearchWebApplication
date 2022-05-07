#!/usr/local/bin/python3

# Scans the parts registry catalogue to gather the BioBricks accessions of every
#   promoter avaible on the Parts Registry. Then, the webpage entry for each
#   accession is accessed and scraped to gather further information for each
#   promoter, including the creator, number of uses, regulatory status, chassis
#   it is deisgned for, and more.

import re
import requests
import os
from bs4 import BeautifulSoup
import unicodedata
import csv

def main():
    # File containing catalogue with accessions and names for all parts in registry
    partsRegistryFull = "All_Parts.fasta.txt"

    # Convert FASTA to different format
    header = None
    seq = ''
    headers = []
    seqs = []

    file = open(partsRegistryFull)
    for line in file:
        line = line.rstrip('\n')

        head = re.match(r">(\S+)\s+(.+)", line)
        if not head:
            seq += line
        else:
            seqs.append(seq)
            header = head.group()
            headers.append(header)
            # Clear previously stored sequence
            seq = ''

    # correct indices of seqs to remove blank one at index 0
    sequences = seqs[1:]
    file.close()

    # Open new file to write reformatted data to
    partsReformatted = open("reformatted_parts.txt", "w")

    # Replace line breaks with $$ to clarify separate catalogue entries
    for hdr, seq in zip(headers, sequences):
        partsReformatted.write(hdr + "$$" + seq + '\n\n')

    partsReformatted.close()

    # Parse IDs, Promoter Names, and Promoter Sequences from reformatted file
    promoters = [] #should be 1222 entries total
    allParts = "reformatted_parts.txt"

    file2 = open(allParts)
    for line in file2:
        line = line.rstrip('\n')
        # Parse entries with type "Regulatory" denoted in header
        if re.search(r'\sRegulatory\s', line):
            # Parse regulatory entries with promoter in the name
            if re.search(r"Promoter", line, flags=re.IGNORECASE):
                # split header from sequence
                entry = re.split('\$\$', line)
                header = entry[0]
                sequence = entry[1]

                # Get accessions and part names
                id_obj = re.search(r'BBa_\S+\s', header)
                name_obj = re.search(r'(?<=\").+(?=\")', header)

                # convert from RE objects to strings
                id = id_obj.group()
                name = name_obj.group()

                # clean-up non-sense characters
                name = clean_data(name)

                # Store all data for promoter in list
                promoter=[id, name, sequence]
                promoters.append(promoter)
    file2.close()

    # use ids to download web page for each promoter as txt
    bare_url = "http://parts.igem.org/Part:"
    final_data = []

    numeric_id = 1

    for entry in promoters:
        promoter = ['', '', '', '', '', '', '', '', '', '', '', '', '']
        promoter[0] = entry[0]
        promoter[1] = entry[1]
        id = str(promoter[0])
        full_url = bare_url + id

        r = requests.get(full_url)
        file_name = id + '.txt'
        # File with HTML removed by beautiful soup
        text_file = id + '_textonly.txt'

        # Write info from webpage to new file
        with open(file_name, 'w') as file:
            file.write(r.text)

        # parse file
        with open(file_name) as fp:
            soup = BeautifulSoup(fp, 'html.parser').get_text(strip=True)
            clean_soup = unicodedata.normalize("NFKD", soup)

        with open(text_file, 'w') as file:
            file.write(clean_soup)

        data = open(text_file)
        info = data.read()

        # Get designer name
        des = re.search('(?<=Designed by:\s).+(?=\s{4}Group)', info)
        if des:
            designer = des.group()
            promoter[2] = designer

        # Get research group name
        grp = re.search('(?<=Group:\s)(.+\s{2,})(?=\(\d)', info)
        #grp = re.search('(?<=Group:\s).+(?=\s+\(\d{4})', info)
        if grp:
            group = grp.group()
            #group_split = "\s{3,}"
            #if re.search(group_split, group):
            #    g_split = group_split.split(group)
            #    group = g_split[0]
            promoter[3] = group

        # Get number of uses
        tms_use = re.search('\d+(?=\sUses)', info)
        if tms_use:
            times_used = tms_use.group()
            promoter[4] = times_used

        # Get Rating
        rtng = re.search('\d+(?=\sRegistry Star)', info)
        if rtng:
            rating = rtng.group()
            promoter[5] = rating

        # Get polymerase type
        pol = re.search('(?<=Categories\/\/)((rnap).+\/\/)(?=direction)', info) ######################################
        if pol:
            polymerase = pol.group()
            polymerase = re.sub(r'/', ' ', polymerase)
            promoter[6] = polymerase

        # Get direction of transcription
        direction = ''
        if re.search('(?<=\/\/direction\/)(forward)', info): ##################
            direction = 'forward'
        if re.search('(?<=\/\/direction\/)(reverse)', info): ##################
            direction = 'reverse'
        if re.search('(?<=\/\/direction\/)(bidirectional)', info): ##################
            direction = 'bidirectional'
        promoter[7] = direction

        # Get chassis
        chas = re.search('(?<=\/\/chassis\/)(.+(\/){2}(promoter))(?=\/\/regulation)', info) ###########
        if chas:
            chassis = chas.group()
            cha = re.split("/",chassis)
            promoter[8] = cha[0]

        # Get regulation type
        regulation = ''
        if re.search('(?<=\/\/regulation\/)positive', info):
            regulation = 'positive'
        if re.search('(?<=\/\/regulation\/)negative', info):
            regulation = 'negative'
        if re.search('(?<=\/\/regulation\/)multiple', info):
            regulation = 'multiple'
        if re.search('(?<=\/\/regulation\/)constitutive', info):
            regulation = 'constitutive'
        promoter[9] = regulation

        #ctl = re.search('(?<=biologycontrol).+(?=direction)', info)
        #if ctl:
        #    control = ctl.group()
        #    promoter[10] = control

        promoter[10] = full_url
        promoter[11] = str(numeric_id)
        promoter[12] = entry[2]

        numeric_id += 1

        data.close()
        final_data.append(promoter)

        # delete files
        filepath1 = "./" + file_name
        filepath2= "./" + text_file
        os.remove(filepath1)
        os.remove(filepath2)

    #print(final_data) to check for correctness
    all_data = open("alldata.txt", "w")

    for promoter in final_data:
       print(promoter, file=all_data)
       print("\n\n", file=all_data)
    all_data.close()


    # output data to file in CSV format so you can use a different script to
    # load it into database.
    #
    with open("complete_promoter_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(final_data)

# method to clean messy data
def clean_data(name):
    # Clean up incompatible characters
    #semicolon (but will switch to colon)
    name = re.sub(r'%3A', ':', name)
    name = re.sub('%3B', ':', name)
    # colon
    name = re.sub(r'%3A', ':', name)
    #italics
    name = re.sub(r'%3CI%3E', '', name, flags=re.IGNORECASE)
    #end_italics
    name = re.sub(r'%3C/I%3E', '', name, flags=re.IGNORECASE)
    #junk
    name = re.sub(r'%3Cbr%3E', '', name)
    name = re.sub('%3D', '=', name)
    name = re.sub(r'=%3E', '>', name)
    name = re.sub('(?<=\-)%3E', '>', name)
    # &
    name = re.sub('%26', '&', name)
    #phi
    name = re.sub(r'&%23981%3B', '', name)
    # "
    name = re.sub('%27%27', '', name)
    name = re.sub('%22', '', name)
    # subscripts
    name = re.sub('%3Csub%3E',' ', name)
    name = re.sub(r'%3C/sub%3E', '', name)
    # square brackets
    name = re.sub('%5B', '[', name)
    name = re.sub('%5D', ']', name)
    # curly braces
    name = re.sub('%7B', '{', name)
    name = re.sub('%7D', '}', name)
    # #
    name = re.sub('%23', '#', name)
    # degrees
    name = re.sub('%B0', 'deg ', name)
    # gamma
    name = re.sub(r'&#947:', 'gamma', name)
    # %
    name = re.sub(r'%25', '%', name)
    #lambda
    name = re.sub(r'&#955:', 'lambda', name)
    # < >
    name = re.sub('%3E', '>', name)
    name = re.sub('%3C', '<', name)
    name = re.sub('%27', "\'", name)
    # !
    name = re.sub('%21', '!', name)
    # nothing visible
    name = re.sub('%09', '', name)
    # sigma
    name = re.sub(r'&#963', 'sigma', name)
    name = re.sub(r'&#981', 'phi', name)
    name = re.sub(r'&#65292:', ',', name)

    return name

if __name__ == '__main__':
    main()
