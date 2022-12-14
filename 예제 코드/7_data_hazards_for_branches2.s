.text
.global main
main : lw $1 0($2)
       add $4, $5, $6
       beq $1, $5, target
       sub $1, $2, $3
target : add $1, $2, $3