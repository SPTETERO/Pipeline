.text
.global main
main : sub $2, $1, $3
       and $12, $2, $5
       or $13, $6, $2
       add $14, $2, $2
       sw $15, 100($2)