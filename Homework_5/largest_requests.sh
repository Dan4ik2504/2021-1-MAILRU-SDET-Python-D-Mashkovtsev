./mkdir_temporary_files.sh;
echo 'Largest requests' > temporary_files/largest_requests_answer_sh.txt;
awk 'match($9, /^4[0-9]*$/) {print $7, "-", $9, "-", $10, "-", $1}' access.log | sort -u | sort -t "-" -b -rnk3,3 -s | head -5 >> temporary_files/largest_requests_answer_sh.txt;