let beg=$1-2
cat $beg
echo "stdin.txt"
cat -n stdin.txt | tail -n +$beg | head -n 5
count=1
max=$2
while [ $count -le $max ]
do
		echo "stdout$count.txt"
		cat -n "stdout$count.txt" | tail -n +$beg | head -n 5
		let count++
done
