#!/bin/bash
# Skrypt do pobierania danych z http://www.pther.net/Plockie/Index.html bazujacy na
# ciaglej numeracji zdjec i pomijajacy niepotrzebne pobieranie stron html na ktorych
# te zdjecia sa osadzone.

EPS="Plockiegrodzkiewieczyste Plockiegrodzkiedecretaiudicialia Plockiegrodzkieoblaty Plockieziemskiewieczysterelacje Plockieziemskiedecreta"
CD=`date +"%Y-%m-%d-%H%M%S"`
CD_FILES="images_$CD.txt"
CD_ERRORS="errors_$CD.txt"
echo "Lista plikow zapisana bedzie w $CD_FILES";
echo "Lista bledow bedzie w $CD_ERRORS";
echo "";

MYWGET="wget -nv -T7 -t0 -w10 "

for EP in $EPS; do
	echo "[i] $EP";
	url="http://www.pther.net/Plockie/$EP/index.html"
	$MYWGET $url -O tmpfile
	grep Index.html tmpfile | sed -e 's/.*href..//g' | sed -e 's/".*//g' > tmpfile2
	for SYGNATURA in `cat tmpfile2`; do
		
		if [ -f tmpfile3 ]; then
			rm tmpfile3;
		fi
		if [ -f tmpfile5 ]; then
			rm tmpfile5;
		fi
		
		echo "";
		echo "[i] $EP $SYGNATURA";
		url2="http://www.pther.net/Plockie/$EP/$SYGNATURA"
		$MYWGET $url2 -O tmpfile3;
		res=$?
		if [ "0" == "$res" ]; then
			cat tmpfile3 | sed -e 's/ /\n/g' | grep Index00 | sed -e 's/.*href..//g' | sed -e 's/".*//g' | sort -r > tmpfile4
			for LAST in `cat tmpfile4`; do
				url3=`echo $url2 | sed -e "s/Index.html/$LAST/g"`
				url3dir=`echo $url2 | sed -e "s/Index.html//g"`
				echo "[i] Pobieram $LAST";
				$MYWGET $url3 -O tmpfile5;
				res=$?
				if [ "0" == "$res" ]; then
					echo "[+] znaleziono ostatnia strone!";
					FILE_LAST=`cat tmpfile5  | grep PL_ | grep jpg | grep -v tn_ | sed -e 's/.*href..//g' | sed -e 's/.html.*//g' | sort -r | uniq | grep ^PL | grep -v _9999 | head -n1`;
					if [ "$FILE_LAST" == "" ]; then
						echo "[!] tylko na niej jest sama okladka, trzeba spr. kolejna!";
						continue;
					fi
					break;
				fi
			done
			
			if [ -f tmpfile3 ] && [ -f tmpfile5 ]; then
				FILE_LAST=`cat tmpfile5  | grep PL_ | grep jpg | grep -v tn_ | sed -e 's/.*href..//g' | sed -e 's/.html.*//g' | sort -r | uniq | grep ^PL | grep -v _9999 | head -n1`;
				FILES=`cat tmpfile3  | grep PL_ | grep jpg | grep -v tn_ | sed -e 's/.*href..//g' | sed -e 's/.html.*//g' | sort | uniq | grep ^PL | grep -v _9999`;
				
				FILE_LAST_ID=`echo "$FILE_LAST" | sed -e 's/_/ /g' | awk '{print $5}'`
				FILE_LAST_PREFIX=`echo "$FILE_LAST" | sed -e "s/$FILE_LAST_ID.*//g"`
				echo "[i] seq 1 $FILE_LAST_ID";
				for ID in `seq 1 $FILE_LAST_ID`; do
					IDZ=$(printf "%04d" $ID)
					echo $url3dir$FILE_LAST_PREFIX$IDZ".jpg" >> $CD_FILES;
				done
				
				# te pliki z poczatku jeszcze
				for ID in $FILES; do
					FILE_NAME=`echo $ID | sed -e 's/_jpg/.jpg/g'`
					if [ "" == "`grep $FILE_NAME $CD_FILES`" ]; then
						echo "[i] seq add $FILE_NAME";
						echo $url3dir$FILE_NAME >> $CD_FILES;
					fi
				done
				
			else
				echo "[-] zonk, brak ostatniej strony $EP/$SYGNATURA";
				echo "[-] zonk, brak ostatniej strony $EP/$SYGNATURA" >> $CD_ERRORS;
			fi
			
		else
			echo "[-] $EP $SYGNATURA BLAD";
			echo "[-] $EP $SYGNATURA BLAD" >> $CD_ERRORS;
		fi
	done
done
