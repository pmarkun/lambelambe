rm merge.csv
find . -name "*.csv" | xargs -n 1 tail -n +2 > merge.tmp
head -n 1 201201_Transferencias.csv > merge.csv
cat merge.tmp >> merge.csv
rm merge.tmp

