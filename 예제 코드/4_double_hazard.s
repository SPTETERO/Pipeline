.text
.global main
main : sub $2 $1 $1
        and $4, $2, $1
        or $4, $4, $2
        add $9, $4, $2