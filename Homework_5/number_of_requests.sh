./mkdir_temporary_files.sh;
echo -en "Total number of requests\n$(wc -l < access.log)" > temporary_files/number_of_requests_answer_sh.txt