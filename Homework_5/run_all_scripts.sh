#!/bin/bash

scripts_list=('largest_requests' 'most_frequent_requests' 'number_of_requests'
'number_of_requests_by_type' 'users_by_number_of_requests')

for script_name in "${scripts_list[@]}"; do
  ./"$script_name.sh"
  python3 "$script_name.py"
  python3 "$script_name.py" --json
done
