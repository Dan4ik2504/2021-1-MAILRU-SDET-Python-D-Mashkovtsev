./mkdir_temporary_files.sh;
echo "Number of requests by type" > temporary_files/number_of_requests_by_type_answer_sh.txt;
awk '{gsub(/"/, "", $6); if (length($6) < 10) print $6}' access.log | sort | uniq -c | sort -nrk1 -s | awk '{print $2,"-",$1}' | column -t >> temporary_files/number_of_requests_by_type_answer_sh.txt