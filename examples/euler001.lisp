(do
  (:= foldr (\ (f z xs) (if (== (length xs) 0) z (f (head xs) (foldr f z (tail xs))))))
  (:= sum (\ (xs) (foldr + 0 xs)))
  (:= divides (\ (a b) (== (% a b) 0)))
  (:= range (\ (n) (if (== n 0) [] (: n (range (- n 1))))))
  (sum (range 100))
)
