(begin
  (define (xrange n i l)
          (if (== n i)
              l
              (xrange n (+ 1 i) (: i l))))
  (define (range n) (xrange n 0 ()))
  (range 10)
)
