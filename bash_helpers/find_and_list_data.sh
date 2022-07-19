#!/bin/bash

# Here You put the name of the folder where the data is kept (relative to ../Biologic/)
data_folder="data"
# Here You put the type of Biologic data (_CV_, _CA_, etc.), set to "" if not important
data_type="_CV_"
# Additional filter, i.e. part of filename
read -p "Type any additional filtering criteria (or press Enter): " filter

echo ""
echo "list_filenames = ["
ls $data_folder | grep $data_type | grep -F "$filter" | sed "s&^&'$data_folder/&" | sed "s/$/',/" | sed '$ s/.$//'
echo "]"
echo ""