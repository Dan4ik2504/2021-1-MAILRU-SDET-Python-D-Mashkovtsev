./mkdir_temporary_files.sh;
echo 'Most frequent requests' > temporary_files/most_frequent_requests_answer_sh.txt;
awk '{print $7}' access.log | sort | uniq -c | sort -rnk1 -s | head -10 | awk '{print $2,"-",$1}' >> temporary_files/most_frequent_requests_answer_sh.txt