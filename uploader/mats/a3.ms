;;; Spring 2009
;;; Assignment 3
;;;

(define-syntax pretty-grade-all
  (syntax-rules (by)
    ((_ fn-to-test fn-ref inputs)
     (pretty-grade-all fn-to-test fn-ref inputs ()))
    ((_ fn-to-test fn-ref () (output* ...))
     (pretty-grade output* ...))
    ((_ fn-to-test fn-ref (inputs inputs* ...) (output* ...))
     (pretty-grade-all
      fn-to-test fn-ref
      (inputs* ...)
      (output* ...
               ((apply fn-to-test `inputs) ==>  ,(apply fn-ref `inputs)) )))
    ))

(define close-enough
  (let ((tolerance .000001))
    (lambda (n1 n2)
      (and (number? n1) (number? n2)
           (<= (abs (- n1 n2)) tolerance)))))

(define all-close-enough
  (let ((tolerance .000001))
    (lambda (ls1 ls2)
      (andmap close-enough ls1 ls2))))

(define ref-perfect-square?
  (lambda (x)
    (integer? (sqrt x))))

(define ref-curious?
  (lambda (n)
    (and (ref-perfect-square? (+ n 1))
         (ref-perfect-square? (+ (/ n 2) 1)))))

(check-run (printf "~n"))

(grade-set "Problem 1a: least" 1
  (check-if-bound least)
  (pretty-grade
   [(least 10 20) ==> 10]
   [(least 10 4)  ==> 4]                               
   [(least 3 3)   ==> 3]
   [(least 0 -3)  ==> -3]
   [(least -9 -10)  ==> -10]
   [(least -10 -9)  ==> -10]
   [(least -8 -8)  ==> -8]
   [(least 0 0)  ==> 0]
   ))

(grade-set "Problem 1b: least-of-three" 1
  (check-if-bound least-of-three)
  (pretty-grade
   [(least-of-three 3 2 1) ==> 1]
   [(least-of-three 1 2 3) ==> 1]
   [(least-of-three 3 1 2) ==> 1]
   [(least-of-three 2 1 3) ==> 1]
   [(least-of-three 9 9 9) ==> 9]
   [(least-of-three 0 0 0) ==> 0]
   [(least-of-three -2 -1 -3) ==> -3]
   [(least-of-three -3 -2 -1) ==> -3]
   [(least-of-three -2 -3 -1) ==> -3]
   [(least-of-three -1 -2 -3) ==> -3]
   [(least-of-three -1 -3 -2) ==> -3]
   [(least-of-three -3 -1 -2) ==> -3]
   [(least-of-three 15557 9187 876543) ==> 9187]
   ))

(grade-set "Problem 2: next-even" 1
  (check-if-bound next-even)
  (pretty-grade
   [(next-even 0)       ==> 2]
   [(next-even 1)       ==> 2]
   [(next-even 2)       ==> 4]
   [(next-even 3)       ==> 4]
   [(next-even 4)       ==> 6]
   [(next-even 5)       ==> 6]
   [(next-even -1)       ==> 0]
   [(next-even -2)       ==> 0]
   [(next-even -3)       ==> -2]
   [(next-even -4)       ==> -2]
   [(next-even -5)       ==> -4]
   [(next-even 7326736) ==> 7326738]
   [(next-even 99999)   ==> 100000]
   [(next-even 17) ==> 18]
   [(next-even 342) ==> 344]
   [(next-even 1111111111) ==> 1111111112]
   [(next-even 8765432) ==> 8765434]
   ))

(grade-set "Problem 3: curious?" 1
  (check-if-bound curious?)
  (pretty-grade-all curious? ref-curious?
    ( ( 6 )
      ( 20 )
      ( 48 )
      ( 49 )
      ( 50 )
      ( 51 )
      ( 52 )
      ( 53 )
      ( 54 )
      ( 55 )
      ( 56 )
      ( 57 )
      ( 58 )
      ( 59 )
      ( 60 )
      ( 61 )
      ( 62 )
      ( 63 )
      ( 64 )
      ( 65 )
      ( 1680 )
      ( 10000 )
      ( 65918160 ) )))

(grade-set "Problem 4: sleep-in?" 1
  (check-if-bound sleep-in?)
  (pretty-grade
   [(sleep-in? 'monday) ==> #f]
   [(sleep-in? 'tuesday) ==> #f]
   [(sleep-in? 'wednesday) ==> #f]
   [(sleep-in? 'thursday) ==> #f]
   [(sleep-in? 'friday) ==> #f]
   [(sleep-in? 'saturday) ==> #t]
   [(sleep-in? 'sunday) ==> #t]))

(grade-set "Problem 5: opposite" 1
  (check-if-bound opposite)
  (pretty-grade
   [(opposite "good") ==> "evil"]
   [(opposite "evil") ==> "good"]))

(grade-set "Problem 6: next-compass" 1
  (check-if-bound next-compass)
  (pretty-grade
   [(next-compass 'north) ==> east]
   [(next-compass 'east) ==> south]
   [(next-compass 'south) ==> west]
   [(next-compass 'west) ==> north]
))

(grade-set "Problem 7: next-collatz" 1
  (check-if-bound next-collatz)
  (pretty-grade
   [(next-collatz 7)  ==> 22]               
   [(next-collatz 22) ==> 11]       
   [(next-collatz 1)  ==> 4]           
   [(next-collatz 5)  ==> 16] 
   [(next-collatz 6)  ==> 3]
   [(next-collatz 16) ==> 8]
   [(next-collatz 2)  ==> 1]
   [(next-collatz 3)  ==> 10]
   [(next-collatz 4)  ==> 2]
   [(next-collatz 8)  ==> 4]
   [(next-collatz 9)  ==> 28]
   [(next-collatz 10) ==> 5]
   [(next-collatz 500) ==> 250]
   [(next-collatz 8421) ==> 25264]
   ))

(grade-set "Problem 8: dna-complement" 1
  (check-if-bound dna-complement)
  (pretty-grade
   [(dna-complement 'a) ==> t]             
   [(dna-complement 't) ==> a]         
   [(dna-complement 'g) ==> c]
   [(dna-complement 'c) ==> g]
   [(dna-complement 'k) ==> error]
   [(dna-complement 'quarter) ==> error]
   ))

(grade-set "Problem 9: up-or-down" 1
  (check-if-bound up-or-down)
  (begin ($set-random-sequence$ '(0 1 2 3 4 5 6 7 8 9 10 11 12 13 15 16)) #t)
  (pretty-grade
   [(up-or-down 5)  ==> (4 6) by member]
   [(up-or-down 5)  ==> (4 6) by member]
   [(up-or-down -3) ==> (-4 -2) by member]
   [(up-or-down 10) ==> (9 11) by member]
   [(up-or-down 0)  ==> (-1 1) by member]
   [(eventually? (lambda () (up-or-down 2)) '(1 3)) ==> #t]
   [(eventually? (lambda () (up-or-down 0)) '(-1 1)) ==> #t]
   ))

(grade-set "Problem 10: pick-one-at-random" 1
  (check-if-bound pick-one-at-random)
  (begin ($set-random-sequence$ '(0 1 2 3 4 5 6 7 8 9 10 11 12 13 15 16)) #t)
  (pretty-grade
   [(pick-one-at-random 1 -1)          ==> (1 -1) by member]
   [(pick-one-at-random #t #f)         ==> (#t #f) by member]
   [(pick-one-at-random #t 64)         ==> (#t 64) by member]
   [(pick-one-at-random 'left 'right)  ==> (left right) by member]
   [(pick-one-at-random 'heads 'tails) ==> (heads tails) by member]
   [(eventually? (lambda () (pick-one-at-random 'a 'b)) '(a b)) ==> #t]
   ))

(grade-set "Problem 11: both-odd?" 1
  (check-if-bound both-odd?)
  (pretty-grade
   [(both-odd? 3 3) ==> #t]
   [(both-odd? 3 5) ==> #t]
   [(both-odd? 5 3) ==> #t]
   [(both-odd? 6 3) ==> #f]
   [(both-odd? 3 8) ==> #f]
   [(both-odd? 8 8) ==> #f]
   [(both-odd? 'a 3) ==> #f]
   [(both-odd? 'a 4) ==> #f]
   [(both-odd? 'a 'b) ==> #f]
   [(both-odd? #t #f) ==> #f]
   [(both-odd? + 5) ==> #f]
   [(both-odd? 7 -) ==> #f]
   [(both-odd? + -) ==> #f]))

(grade-set "Problem 12: either-even?" 1
  (check-if-bound both-odd?)
  (pretty-grade
   [(either-even? 4 8) ==> #t]
   [(either-even? -1238 0) ==> #t]
   [(either-even? 3 0) ==> #t]
   [(either-even? 6.2 3) ==> #f]
   [(either-even? 4 'a) ==> #t]
   [(either-even? 3 'a) ==> #f]
   [(either-even? 'b 8) ==> #t]
   [(either-even? 3 5) ==> #f]
   [(either-even? #t odd?) ==> #f]
   [(either-even? '() '#()) ==> #f]
))

#!eof


(grade-set "Problem 5: score->letter" 1
  (check-if-bound score->letter)
  (pretty-grade
   [(score->letter 50) ==> F]
   [(score->letter 60) ==> D]
   [(score->letter 76) ==> B]
   [(score->letter 80) ==> B]
   [(score->letter 91) ==> A]
   [(score->letter 51) ==> f]
   [(score->letter 53) ==> d]
   [(score->letter 63) ==> d]
   [(score->letter 65) ==> c]
   [(score->letter 75) ==> c]
   [(score->letter 77) ==> b]
   [(score->letter 87) ==> b]
   [(score->letter 89) ==> a]
   [(score->letter 100) ==> a]
   [(score->letter 88) ==> a]
   [(score->letter 76) ==> b]
   [(score->letter 64) ==> c]
   [(score->letter 52) ==> d]
   [(score->letter 87.99) ==> b]
   [(score->letter 75.99) ==> c]
   [(score->letter 63.99) ==> d]
   [(score->letter 51.99) ==> f]
  ))

(grade-set "Problem 2: sgn" 1
  (check-if-bound sgn)
  (pretty-grade
   [(sgn 5)    ==> 1]
   [(sgn -2.4) ==> -1]
   [(sgn 0)    ==> 0]
   [(sgn 1000000) ==> 1]
   [(sgn -1000000)    ==> -1]
   ))

(grade-set "Problem 10: both-even?" 1
  (check-if-bound both-even?)
  (pretty-grade
   [(both-even? 2 2) ==> #t]
   [(both-even? 2 4) ==> #t]
   [(both-even? 4 2) ==> #t]
   [(both-even? 5 2) ==> #f]
   [(both-even? 2 7) ==> #f]
   [(both-even? 9 7) ==> #f]
   [(both-even? 'a 2) ==> #f]
   [(both-even? 'a 3) ==> #f]
   [(both-even? 'a 'b) ==> #f]
   [(both-even? #t #f) ==> #f]
   [(both-even? + 4) ==> #f]
   [(both-even? 8 -) ==> #f]
   [(both-even? + -) ==> #f]))

(grade-set "Problem 9: valid?" 1
  (check-if-bound valid?)
  (pretty-grade
   [(valid? 47715497443)       ==> #t]
   [(valid? 24038868863995)    ==> #t]
   [(valid? 777777777777770)   ==> #t]
   [(valid? 123456789)         ==> #f]
   [(valid? 2135340034971134)  ==> #f]
   [(valid? 5437651012035600)  ==> #f]
   [(valid? 212324759860048)   ==> #f]
   [(valid? 55503988104811002) ==> #t]
   [(valid? 33333333)          ==> #t]
   [(valid? 999999999999999)   ==> #f]
   [(valid? 10000000000000006) ==> #t]
   ))


(grade-set "Problem 3: echo" 1
  (check-if-bound echo)
  (pretty-grade
   [(echo 5)       ==> 5]
   [(echo 'echo)   ==> echo]               
   [(echo echo)    ==> ,echo]      
   [(echo '(echo)) ==> (echo)]
   [(echo #t)      ==> #t]
   [(echo #f)      ==> #f]
   [(echo '(1 2 3)) ==> (1 2 3)]
   [(echo '())     ==> ()]
   [(echo 98.6)    ==> 98.6]
   [(echo cons)    ==> ,cons]
   [(echo "abc")   ==> "abc"]
   ))


(grade-set "Problem 2: next-light" 1
  (check-if-bound next-light)
  (pretty-grade
   [(next-light 'red)       ==> green]
   [(next-light 'green)     ==> yellow]
   [(next-light 'yellow)    ==> red]
   ))
(grade-set "Problem 5: twins" 1
  (check-if-bound twins)
  (pretty-grade
   [(twins #t) ==> (#t #t)]
   [(twins 'girl) ==> (girl girl)]
   [(twins (list 111 222)) ==> ((111 222) (111 222))]
   [(twins 3) ==> (3 3)]
   [(twins 'a) ==> (a a)]
   [(twins '()) ==> (() ())]
  ))

(grade-set "Problem 7: exchange" 1
  (check-if-bound exchange)
  (pretty-grade
   [(exchange '(1 2)) ==> (2 1)]
   [(exchange '(pat vanna)) ==> (vanna pat)]
   [(exchange '(meow mix)) ==> (mix meow)]
   [(exchange '(#t #f)) ==> (#f #t)]
   [(exchange '(x (x))) ==> ((x) x)]
  ))

; +or-

(grade-set "Problem 8: both-the-same?" 1
  (check-if-bound both-the-same?)
  (pretty-grade
   [(both-the-same? '(0 0)) ==> #t]
   [(both-the-same? '(a a)) ==> #t]
   [(both-the-same? '((a) (a))) ==> #t]
   [(both-the-same? '((a) (b))) ==> #f]
   [(both-the-same? '(5 (+ 2 3))) ==> #f]
   [(both-the-same? (cons #t (cons #t '()))) ==> #t]
   [(both-the-same? (cons 0 (cons 0 '()))) ==> #t]
   [(both-the-same? (cons 'a (cons 'A '()))) ==> #t]
   [(both-the-same? (cons 5 (cons '(+ 1 2) '()))) ==> #f]
   [(both-the-same? (cons + (cons - '()))) ==> #f]
   [(both-the-same? (cons 0 (cons 1 '()))) ==> #f]
   [(both-the-same? (cons 'a (cons 'b '()))) ==> #f]
  ))

(grade-set "Problem 9: insert-between" 1
  (check-if-bound insert-between)
  (pretty-grade
   [(insert-between 'baloney '(bread bread))    ==> (bread baloney bread)]
   [(insert-between 'medium '(small large))     ==> (small medium large)]
   [(insert-between '() '((rock) (hard-place))) ==> ((rock) () (hard-place))]
   [(insert-between 'to '(19 25))               ==> (19 to 25)]
   [(insert-between 0 '(-1 1))                  ==> (-1 0 1)]
   [(insert-between 'b '(a c))                  ==> (a b c)]
))

(grade-set "Problem 10: stagger" 1
  (check-if-bound stagger)
  (pretty-grade
   [(stagger 1 2 3) ==> (1 (2 (3)))]
   [(stagger 'deep 'deeper 'deepest) ==> (deep (deeper (deepest)))]
   [(stagger '() '() '()) ==> (() (() (())))]))

(grade-set "Problem 11: monsters" 1
  (check-if-bound monsters)
  (pretty-grade
   [(monsters 0) ==> (there are 0 monsters approaching)]
   [(monsters 1) ==> (there is 1 monster approaching)]
   [(monsters 2) ==> (there are 2 monsters approaching)]
   [(monsters 6) ==> (there are 6 monsters approaching)]
   [(monsters 7) ==> (there are 7 monsters approaching)]
   [(monsters 8) ==> (there are 8 monsters approaching)]
   [(monsters 9) ==> (there are 9 monsters approaching)]
   [(monsters 1471982471289) ==> (there are 1471982471289 monsters approaching)]
   ))


(grade-set "Problem 12: threatens?" 1
  (check-if-bound threatens?)
  (pretty-grade
   [(threatens? '(5 5) '(8 8)) ==> #t]
   [(threatens? '(5 5) '(5 8)) ==> #t]
   [(threatens? '(5 5) '(2 8)) ==> #t]
   [(threatens? '(2 5) '(6 1)) ==> #t]
   [(threatens? '(4 7) '(2 3)) ==> #f]
   [(threatens? '(1 1) '(1 2)) ==> #t]
   [(threatens? '(1 1) '(1 3)) ==> #t]
   [(threatens? '(1 1) '(1 4)) ==> #t]
   [(threatens? '(1 1) '(1 5)) ==> #t]
   [(threatens? '(1 1) '(1 6)) ==> #t]
   [(threatens? '(1 1) '(1 7)) ==> #t]
   [(threatens? '(1 1) '(1 8)) ==> #t]
   [(threatens? '(1 1) '(2 1)) ==> #t]
   [(threatens? '(1 1) '(3 1)) ==> #t]
   [(threatens? '(1 1) '(4 1)) ==> #t]
   [(threatens? '(1 1) '(5 1)) ==> #t]
   [(threatens? '(1 1) '(6 1)) ==> #t]
   [(threatens? '(1 1) '(7 1)) ==> #t]
   [(threatens? '(1 1) '(8 1)) ==> #t]
   [(threatens? '(1 1) '(2 2)) ==> #t]
   [(threatens? '(1 1) '(3 3)) ==> #t]
   [(threatens? '(1 1) '(4 4)) ==> #t]
   [(threatens? '(1 1) '(5 5)) ==> #t]
   [(threatens? '(1 1) '(6 6)) ==> #t]
   [(threatens? '(1 1) '(7 7)) ==> #t]
   [(threatens? '(1 1) '(8 8)) ==> #t]
   [(threatens? '(1 8) '(2 7)) ==> #t]
   [(threatens? '(1 8) '(3 6)) ==> #t]
   [(threatens? '(1 8) '(4 5)) ==> #t]
   [(threatens? '(1 8) '(5 4)) ==> #t]
   [(threatens? '(1 8) '(6 3)) ==> #t]
   [(threatens? '(1 8) '(7 2)) ==> #t]
   [(threatens? '(1 8) '(8 1)) ==> #t]
   [(threatens? '(1 8) '(3 7)) ==> #f]
   [(threatens? '(1 8) '(4 6)) ==> #f]
   [(threatens? '(1 8) '(5 5)) ==> #f]
   [(threatens? '(1 8) '(6 4)) ==> #f]
   [(threatens? '(1 8) '(7 3)) ==> #f]
   [(threatens? '(1 8) '(8 2)) ==> #f]
))

(grade-set "Problem 14: scrunch-sequence" 1
  (check-if-bound scrunch-sequence)
  (pretty-grade
   [(scrunch-sequence '(1 2 3 4 5)) ==> (3 3 4 5)]
   [(scrunch-sequence '(5 4 3 2)) ==> (9 3 2)]
   [(scrunch-sequence '(3 5)) ==> (8)]
   [(scrunch-sequence '(5 3)) ==> (8)]
   [(scrunch-sequence (scrunch-sequence (scrunch-sequence '(6 1 7 9))))
    ==> (23)]
   [(scrunch-sequence '(1 1 1 1 1 1)) ==> (2 1 1 1 1)]
   [(scrunch-sequence '(1 1 1 1 1 1)) ==> (2 1 1 1 1)]
   [(scrunch-sequence '(2 2 2 2)) ==> (4 2 2)]
   [(scrunch-sequence '(42 -42 0 0 0 0 0 0 0 0 0)) ==> (0 0 0 0 0 0 0 0 0 0)]
   ))


#!eof

(grade-set "Problem 11a: interval-contains?" 1
  (check-if-bound interval-contains?)
  (pretty-grade
   [(interval-contains? '(2 5) '(2 5)) ==> #t]
   [(interval-contains? '(2 4) '(2 5)) ==> #t]
   [(interval-contains? '(3 5) '(2 5)) ==> #t]
   [(interval-contains? '(3 4) '(2 5)) ==> #t]
   [(interval-contains? '(0 4) '(2 5)) ==> #f]
   [(interval-contains? '(3 9) '(2 5)) ==> #f]))

(grade-set "Problem 11b: box-contains?" 1
  (check-if-bound box-contains?)
  (pretty-grade
   [(box-contains? '((2 5) (7 8)) '((2 5) (7 8))) ==> #t]
   [(box-contains? '((3 5) (7 8)) '((2 5) (7 8))) ==> #t]
   [(box-contains? '((3 5) (7 7)) '((2 5) (7 8))) ==> #t]
   [(box-contains? '((3 5) (7 9)) '((2 5) (7 8))) ==> #f]))



(grade-set "Problem 4: couple" 1
  (check-if-bound couple)
  (pretty-grade
   [(couple 'anthony 'cleopatra) ==> (anthony cleopatra)]
   [(couple (+ 2 3) -5) ==> (5 -5)]
   [(couple (couple '() '()) '()) ==> ((() ()) ())]
   [(couple 1 2) ==> (1 2)]
   [(couple #t #f) ==> (#t #f)]
   [(couple #f #t) ==> (#f #t)]
  ))

(grade-set "Problem 2: flip-coin" 1
  (check-if-bound flip-coin)
  (begin ($set-random-sequence$ '(1 2 3 4 5 6 7 8 9 10 11 12)) #t)
  (pretty-grade
   [(flip-coin) ==> (heads tails) by member]
   [(flip-coin) ==> (heads tails) by member]
   [(flip-coin) ==> (heads tails) by member]
   [(flip-coin) ==> (heads tails) by member]
   [(flip-coin) ==> (heads tails) by member]
   [(flip-coin) ==> (heads tails) by member]
   [(flip-coin) ==> (heads tails) by member]
   [(flip-coin) ==> (heads tails) by member]
   [(flip-coin) ==> (heads tails) by member]
   [(flip-coin) ==> (heads tails) by member]
  ))

(grade-set "Problem 3: middle-digit" 1
  (check-if-bound middle-digit)
  (pretty-grade
;   [(string-length "\n") ==> 100]
   [(middle-digit 123)  ==> 2]
   [(middle-digit 806)  ==> 0]
   [(middle-digit -121) ==> 2]
   [(middle-digit 003) ==> 0]
   [(middle-digit 000) ==> 0]
   [(middle-digit 058) ==> 5]
   [(middle-digit 461) ==> 6]
  ))


(grade-set "Problem 5: convert-grade" 1
  (check-if-bound convert-grade)
  (pretty-grade
   [(convert-grade 90)  ==> 4.0]
   [(convert-grade 80)  ==> 3.0]
   [(convert-grade 70)  ==> 2.0]            
   [(convert-grade 60)  ==> 1.0]
   [(convert-grade 50)  ==> 0.0]  
   [(convert-grade 40)  ==> 0.0]
   [(convert-grade 100) ==> 4.0]          
   [(convert-grade 95)  ==> 4.0]         
   [(convert-grade 99)  ==> 4.0]
   [(convert-grade 90.1)  ==> 4.0]
   [(convert-grade 89.9)  ==> 3.0]
   [(convert-grade 80.1)  ==> 3.0]
   [(convert-grade 79.9)  ==> 2.0]
   [(convert-grade 70.1)  ==> 2.0]
   [(convert-grade 69.9)  ==> 1.0]
   [(convert-grade 60.1)  ==> 1.0]
   [(convert-grade 59.9)  ==> 0.0]
   [(convert-grade 43)  ==> 0.0]
   [(convert-grade 15)  ==> 0.0]
   [(convert-grade 0)  ==> 0.0]
  ))


(grade-set "Problem 8: num-digits" 1
  (check-if-bound num-digits)
  (pretty-grade
   [(num-digits 0)     ==> 1]              
   [(num-digits 1)     ==> 1]              
   [(num-digits 2)     ==> 1]              
   [(num-digits 3)     ==> 1]              
   [(num-digits 4)     ==> 1]              
   [(num-digits 5)     ==> 1]
   [(num-digits 6)     ==> 1]              
   [(num-digits 7)     ==> 1]              
   [(num-digits 8)     ==> 1]              
   [(num-digits 9)     ==> 1]              
   [(num-digits 10)    ==> 2]              
   [(num-digits 11)    ==> 2]              
   [(num-digits 99)    ==> 2]              
   [(num-digits 100)   ==> 3]              
   [(num-digits 101)   ==> 3]              
   [(num-digits 999)   ==> 3]              
   [(num-digits 1000)  ==> 4]              
   [(num-digits 1001)  ==> 4]              
   [(num-digits 87600)                  ==> 5]  
   [(num-digits 12345678)               ==> 8]      
   [(num-digits 2222222222222222222222) ==> 22]
   [(num-digits 9876543210012345678998765432100123456789) ==> 40]
   ))



(grade-set "Problem 10b: collatz-steps" 1
  (check-if-bound collatz-steps)
  (pretty-grade
   [(collatz-steps 1)    ==> 0]
   [(collatz-steps 2)    ==> 1]
   [(collatz-steps 3)    ==> 7]
   [(collatz-steps 4)    ==> 2]
   [(collatz-steps 5)    ==> 5]
   [(collatz-steps 6)    ==> 8]
   [(collatz-steps 7)    ==> 16]                 
   [(collatz-steps 8)    ==> 3]
   [(collatz-steps 9)    ==> 19]
   [(collatz-steps 10)   ==> 6]
   [(collatz-steps 100)  ==> 25]
   [(collatz-steps 2000) ==> 112]
   ))


(grade-set "Problem 10c: collatz-sequence" 1
  (check-if-bound collatz-sequence)
  (pretty-grade
   [(collatz-sequence 1)  ==> (1)]    
   [(collatz-sequence 2)  ==> (2 1)]    
   [(collatz-sequence 3)  ==> (3 10 5 16 8 4 2 1)]    
   [(collatz-sequence 4)  ==> (4 2 1)]    
   [(collatz-sequence 5)  ==> (5 16 8 4 2 1)]    
   [(collatz-sequence 6)  ==> (6 3 10 5 16 8 4 2 1)]    
   [(collatz-sequence 7)  ==> (7 22 11 34 17 52 26 13 40 20 10 5 16 8 4 2 1)]
   [(collatz-sequence 8)  ==> (8 4 2 1)]    
   [(collatz-sequence 9)  ==> 
    (9 28 14 7 22 11 34 17 52 26 13 40 20 10 5 16 8 4 2 1)]
   [(collatz-sequence 10) ==> (10 5 16 8 4 2 1)]    
   [(collatz-sequence 99) ==>
    (99 298 149 448 224 112 56 28 14 7 22 11 34 17 52 26 13 40 20 10 5 16 8
     4 2 1)]
   ))



(grade-set "Problem 15: double-dare" 1
  (check-if-bound double-dare)
  (pretty-grade
   [(double-dare '())               ==> ()]
   [(double-dare '(z))              ==> (z)]
   [(double-dare '(dare))           ==> (dare dare)]
   [(double-dare '(y z))            ==> (y z)]
   [(double-dare '(dare z))         ==> (dare dare z)]
   [(double-dare '(z dare))         ==> (z dare dare)]
   [(double-dare '(dare dare))      ==> (dare dare dare dare)]
   [(double-dare '(0 1 2))          ==> (0 1 2)]
   [(double-dare '(0 1 dare))       ==> (0 1 dare dare)]
   [(double-dare '(0 dare 1))       ==> (0 dare dare 1)]
   [(double-dare '(dare to try))    ==> (dare dare to try)]
   [(double-dare '(a dare dare))    ==> (a dare dare dare dare)]
   [(double-dare '(dare a dare))    ==> (dare dare a dare dare)]
   [(double-dare '(dare dare a))    ==> (dare dare dare dare a)]
   [(double-dare '(truth or dare or triple dog dare))
    ==> (truth or dare dare or triple dog dare dare)]
   [(double-dare '(dare dare dare)) ==> (dare dare dare dare dare dare)]
   [(double-dare '(#f dare #t #f dare dare #f #t #f #t dare #f dare #t))
    ==> (#f dare dare #t #f dare dare dare dare
	 #f #t #f #t dare dare #f dare dare #t)]
))

