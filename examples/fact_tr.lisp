(begin
  (define (fact_tr n rv) (if (== n 0) rv (fact_tr (- n 1) (* n rv))))
  (define (fact n) (fact_tr n 1))
  (fact 1000)
)
