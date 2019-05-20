
echo "Converting all folders to cil message"
for d in */; do
	for f in $d*.pcap; do
		fname=$(basename $f .pcap)
		#echo "$fname"
		ciltool cil_reader $f >> /media/ky/easystore/cil_reader_data/scrimmage2/$fname.json
		echo "Completed converting $fname"
	done
done