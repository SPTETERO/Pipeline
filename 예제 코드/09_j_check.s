.text
.global main
main : and $3 $2 $1
       j here
       add $4 $2 $3
       add $4 $2 $3
       add $4 $2 $3
here : sub $5 $3 $4
       slt $6 $2 $1