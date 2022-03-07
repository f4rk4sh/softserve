if [ $# -eq 0 ]; then
	echo "[--all]    - displays the IP addresses and symbolic names of all hosts in the current subnet"
	echo "[--target] - displays a list of open system TCP ports"
fi

function all {
nmap -sP 192.168.0.0/24
}

function target {
nmap -sT -p- localhost
}

case "$1" in
	--all) all ;;
	--target) target ;;
esac

