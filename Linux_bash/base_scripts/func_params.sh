#!/bin/bash
function plus {
	let result="$1 + $2"
	echo $1 + $2 = $result
}

plus 3 10
plus a b
plus good 88
