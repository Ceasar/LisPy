(begin
  (define (foldr f z xs)
          (if (== (length xs) 0)
              z
              (f (head xs) (foldr f z (tail xs)))))
  (define (sum xs) (foldr + 0 xs))
  (define (divides a b) (== (% a b) 0))
  (define (range n) (if (== n 0) () (: n (range (- n 1)))))
  (sum (range 100))
)
