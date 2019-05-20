# #! /bin/bash
# echo "1: FREEPLAY  2: custom name(s)"
# read type2

# if [ $type2 =='1' ]; then
# 	echo "Type FREEPLAY-RESERVATION number(s):"
# 	read -a arr
# 	echo "Downloading ${#arr[@]} files..."

# 	for i in ${arr[@]}
# 	do
# 		rsync -r -aPv -z -e  ssh kb3282@10.248.125.195:/sc2/mirror/FREEPLAY-RESERVATION-$i /media/ky/easystore/CIL_messages/freeplay/
# 		echo "Successfully downloaded FREEPLAY-RESERVATION-$i"
# 	done
# else
# 	echo "Type exect folder name(s):"
# 	read -a arr
# 	echo "Downloading ${#arr[@]} files..."

# 	for i in ${arr[@]}
# 		rsync -r -aPv -z -e  ssh kb3282@10.248.125.195:/sc2/mirror/$i /media/ky/easystore/CIL_messages/custom/
# 		echo "Successfully downloaded $i"
# 	done
# fi
# #echo Logging into server...
# #ssh kb3282@10.248.125.195


#! /bin/bash

echo "Type exect folder name(s):"
read -a arr
echo "Downloading ${#arr[@]} files..."

for i in ${arr[@]}
do
	rsync -r -aPv -z -e ssh kb3282@10.248.125.195:/sc2/mirror/$i /media/ky/easystore/CIL_messages/custom/
	echo "Successfully downloaded $i"
done
#echo Logging into server...
#ssh kb3282@10.248.125.195
