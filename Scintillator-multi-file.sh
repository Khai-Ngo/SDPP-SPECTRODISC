for datafile in $(find $2 -name '*.dat')
do
	py Scintillator-analysis.py $1 $datafile $3
done
