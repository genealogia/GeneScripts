#!/bin/bash
for i in `seq 1 324`; do
	NUMBER=`printf "%04d" $i`;
	LINK="http://cdiak.archives.gov.ua/spysok_fondiv/0021/0001/$NUMBER/";
	if [[ ! -f /tmp/ttttt_$NUMBER ]]; then
		wget $LINK -O /tmp/ttttt_$NUMBER;
	fi
	MAX_ID=`grep img-responsive /tmp/ttttt_$NUMBER | sort -r | sed -e 's/m.jpg.*//g' | sed -e 's/.*_//g' | head -n 1 | bc`;
	#echo $NUMBER"_"$MAX_ID;
	for PHOTO in `seq 1 $MAX_ID`; do
		PHOTO_Z=`printf "%04d" $PHOTO`;
		echo "http://cdiak.archives.gov.ua/spysok_fondiv/0021/0001/$NUMBER/img/0021_0001_$NUMBER"_$PHOTO_Z".jpg";
	done

done
