.text
.global main
main : lw $2 20($1)
        and $4, $2, $5
        or $8, $2, $5
        add $9, $4, $2
        slt $1, $5, $7