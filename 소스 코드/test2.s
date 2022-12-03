.text
.globl main
main:
    add $t8, $t0, $t1
    sub $t8, $t0, $t1
    addi $t6, $t2, 30
    sll $10, $16, 4
    sw $4, 8($5)
    lw $5, 8($6)