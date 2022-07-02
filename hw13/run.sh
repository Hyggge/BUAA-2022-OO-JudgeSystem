count=1
while [ $count -le $1 ]; do
	echo -e "\033[1;34;40m>>>>>>>>>> Test $count <<<<<<<<<<\033[0m"
	python3 generate.py $count
	let count++
done
