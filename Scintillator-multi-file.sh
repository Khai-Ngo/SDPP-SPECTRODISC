for datafile in $(find $2 -name '*.dat' | sort -n -t _ -k 2)
do
	py Scintillator-analysis.py $1 $datafile $3
done
