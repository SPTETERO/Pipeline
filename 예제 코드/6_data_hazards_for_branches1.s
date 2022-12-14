.text
.global main
main : add $1, $2, $3
       add $4, $5, $6
       add $7, $8, $9
       beq $1, $4, target
       add $11, $10, $12
target : add $10, $11, $12