./mkdir_temporary_files.sh;
echo 'Users by the number of requests' > temporary_files/users_by_number_of_requests_answer_sh.txt;
awk 'match($9, /^5[0-9]*$/) {print $1}' access.log | sort | uniq -c | sort -nrk1 -s | head -5 | awk '{print $2,"-",$1}' | column -t >> temporary_files/users_by_number_of_requests_answer_sh.txt;
