
echo "Converting all folders to cil message"
for d in */; do
	for f in $d*.pcap; do
		fname=$(basename $f .pcap)
		#echo "$fname"
		ciltool cil_checker $f --src-auto >> /media/ky/easystore/cil_checker_data/scrimmage2/$fname.json
		echo "Completed converting checker: $fname"
	done
done