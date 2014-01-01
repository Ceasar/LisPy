(begin
  (define (foldr f z xs)
          (if (== (length xs) 0)
              z
              (f (head xs) (foldr f z (tail xs)))))
  (define (sum xs) (foldr + 0 xs))
  (define (divides a b) (== (% a b) 0))
  (define (xrange n i rv) (if (< n i) rv (xrange n (+ i 1) (: i rv))))
  (define (range n) (xrange n 0 ()))
  (sum (range 100))
)
