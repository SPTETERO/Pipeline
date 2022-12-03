
.text
main : lw $1 0($5)
        beq $1 $4 next
next : add $8 $9 $10