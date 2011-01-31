;;; Suzanne Menzel
;;; menzel@cs.indiana.edu
;;; C211 Assignment 3

;; Problem 1
(define echo
  (lambda (x)
    x))

;; Problem 2
(define pick-one-at-random
  (lambda (a b)
    (if (zero? (random 2)) 
        a 
        b)))

;; Problem 3
(define middle-digit
  (lambda (n)
    (abs (remainder (quotient n 10) 10))))

;; Problem 4
(define next-light
  (lambda (light)
    (if (equal? light 'red)
	'green
	(if (equal? light 'green)
	    'yellow
	    'red))))

;; Problem 5
(define convert-grade
  (lambda (grade)
    (if (>= grade 90)
	4.0
	(if (>= grade 80)
	    3.0
	    (if (>= grade 70)
		2.0
		(if (>= grade 60)
		    1.0
		    0.0))))))

;; Problem 6
(define ls0 (cons 'a (cons 'b '())))
(define ls1 (cons 'c (cons 'd (cons 'e '()))))
(define ls2 (cons (cons 'f '())
		  (cons (cons 'g '()) 
			(cons (cons 'h '()) '()))))
(define ls3 (cons (cons 'i (cons 'j '())) 
		  (cons 'k '())))
(define ls4 (cons 'l
		  (cons (cons 'm (cons 'n '())) '())))
(define ls5 (cons 'o
		  (cons (cons 'p (cons (cons 'q '()) '())) '())))
(define ls6 (cons (cons (cons 'r '()) (cons 's '()))
		  (cons 't '())))

;; Problem 7a
(define couple
  (lambda (x y)
    (list x y)))

;; Problem 7b
(define twins
  (lambda (x)
    (couple x x)))

;; Problem 7c
(define neighbors
  (lambda (x)
    (couple (sub1 x) (add1 x))))

;; Problem 7d
(define exchange
  (lambda (ls)
    (cons (cadr ls) (cons (car ls) '()))))

;; Problem 7e
(define both-the-same?
  (lambda (ls2)
    (let ([ans (equal? (car ls2)
		       (cadr ls2))])
      (if (symbol? (car ls2))
	  (string-ci=? (symbol->string (car ls2))
		       (symbol->string (cadr ls2)))
	  ans))))

;; Problem 7f
(define +or-
  (lambda (x y)
    (cons (+ x y) (cons (- x y) '()))))

;; Problem 7g
(define insert-between
  (lambda (item pair)
    (cons (car pair)
	  (cons item (cdr pair)))))

;; Problem 8
(define num-digits
  (lambda (n)
    (if (< n 10)
	1
	(+ 1 (num-digits (quotient n 10))))))

;; Problem 9
(define count-backwards
  (lambda (n)
    (if (zero? n)
        (cons 0 '())
        (cons n (count-backwards (- n 1))))))

;; Problem 10a
(define next-collatz
  (lambda (n)
    (if (even? n)
	(/ n 2)
	(+ (* 3 n) 1))))

;; Problem 10b
(define collatz-steps
  (lambda (a0)
    (if (= a0 1)
	0
	(+ 1 (collatz-steps (next-collatz a0))))))

;; Problem 10c
(define collatz-sequence
  (lambda (a0)
    (if (= a0 1)
	(cons 1 '())
	(cons a0 (collatz-sequence (next-collatz a0))))))

;; Problem 11
(define hugs-and-kisses
  (lambda (n)
    (if (zero? n)
        '()
        (insert-xo (hugs-and-kisses (- n 1))))))

; adds an x and an o to the front of ls
(define insert-xo
  (lambda (ls)
    (cons 'x (cons 'o ls))))

;; Problem 12
(define upstairs
  (lambda (n)
    (cond
     [(zero? n) '()]
     [(= n 1) (wrap-once 'up)]
     [else (cons 'up
                 (wrap-once (upstairs (- n 1))))])))

; puts one layer of parens around the item
(define wrap-once
  (lambda (item)
    (cons item '())))

;; Problem 13
(define bean-counter
  (lambda (ls)
    (cond
     [(null? ls) 0]
     [(bean? (car ls)) (+ 1 (bean-counter (cdr ls)))]
     [else (bean-counter (cdr ls))])))

(define bean?
  (lambda (item)
    (equal? item 'bean)))

; Here's an alternate solution:

(define bean-counter
  (lambda (ls)
    (if (null? ls)
        0
        (+ (if (bean? (car ls))
               1
               0)
           (bean-counter (cdr ls))))))

;; Problem 14
(define penny-pincher
  (lambda (ls)
    (cond
     [(null? ls) '()]
     [(penny? (car ls)) (penny-pincher (cdr ls))]
     [else (cons (car ls)
                 (penny-pincher (cdr ls)))])))

(define penny?
  (lambda (item)
    (equal? item 'penny)))


;; Problem 15
(define double-dare
  (lambda (ls)
    (if (null? ls)
	'()
	(if (equal? (car ls) 'dare)
	    (cons 'dare (cons 'dare (double-dare (cdr ls))))
	    (cons (car ls) (double-dare (cdr ls)))))))

#!eof

(define flip-coin
  (lambda ()
    (if (zero? (random 2))
	'heads
	'tails)))