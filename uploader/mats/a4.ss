(define sum-squares 
  (lambda (n)
    (if (= n 0)
        (+ n 0)
        (+ (* n n) (sum-squares (* (- n 1) (- n 1)))))))

(define count-backwards
  (lambda (n)
    (if (zero? n)
        (cons 0 '())
        (cons n (count-backwards n)))))

#!eof


;;; Suzanne Menzel
;;; menzel@cs.indiana.edu
;;; C211 Assignment 4

(load "image.ss")

(define spin
  (lambda (clr)
    (color (color-ref clr 'green)
           (color-ref clr 'blue)
           (color-ref clr 'red))))

(define re-colorize
  (lambda (img)
    (image-map spin img)))

(define photo-negative 
  (lambda (img)
    (image-map (lambda (clr)
                 (color (- 255 (color-ref clr 'red))
                        (- 255 (color-ref clr 'green))
                        (- 255 (color-ref clr 'blue))))
               img)))


(define obamicon 
  (lambda (img)
    (image-map (lambda (clr)
                 (let ([x (+ (color-ref clr 'red)
                             (color-ref clr 'green)
                             (color-ref clr 'blue))])
                   (cond
                    [(<= x 181) (color 0 51 76)]
                    [(<= x 363) (color 217 26 33)]
                    [(<= x 545) (color 112 150 158)]
                    [else (color 252 227 166)])))
               img)))

(define sum-squares
  (lambda (n)
    (if (zero? n)
        0
        (+ (* n n) (sum-squares (- n 1))))))

(define matryoshka
  (lambda (ls)
    (if (or (null? ls) (null? (cdr ls)))
        ls
        (cons (car ls)
              (list (matryoshka (cdr ls)))))))


(define all-even?
  (lambda (ls)
    (or (null? ls)
	(and (integer? (car ls))
	     (even? (car ls))
	     (all-even? (cdr ls))))))

;; Problem 5b
(define some-even?
  (lambda (ls)
    (and (not (null? ls))
	 (or (and (integer? (car ls)) (even? (car ls)))
	     (some-even? (cdr ls))))))


; Exercise 1 --------------------------------------------------------------
;
;; The procedure hugs-and-kisses takes a positive integer n and
;; returns a list of n x's and o'x.

(define hugs-and-kisses
  (lambda (n)
    (if (zero? n)
        '()
        (insert-xo (hugs-and-kisses (- n 1))))))

; adds an x and an o to the front of ls
(define insert-xo
  (lambda (ls)
    (cons 'x (cons 'o ls))))

(define count-backwards
  (lambda (n)
    (if (zero? n)
        (cons 0 '())
        (cons n (count-backwards (- n 1))))))

; Exercise 3 --------------------------------------------------------------
;
;; upstairs takes a non-negative integer n and returns a list of n up's
;; nested within each other, e.g., (upstairs 3) ==> (up (up (up)))

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

; Exercise 4 --------------------------------------------------------------
;
;; bean-counter takes a list ls and returns the number of times the
;; symbol bean occurs at top level.

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

; Exercise 5 --------------------------------------------------------------
;
;; penny-pincher takes a list ls and returns the list with all
;; top-level occurrences of the symbol penny removed.

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


(define double-dare
  (lambda (ls)
    (if (null? ls)
	'()
	(if (equal? (car ls) 'dare)
	    (cons 'dare (cons 'dare (double-dare (cdr ls))))
	    (cons (car ls) (double-dare (cdr ls)))))))

; Exercise 6 --------------------------------------------------------------
;
;; fib-list? takes a list ls of two or more numbers and returns #t if
;; ls has the fibonnacci property, and #f otherwise.

(define fib-list?
  (lambda (ls)
    (if (null? (cddr ls))        ; cddr is more efficient than using length
        #t
        (if (fib-sequence-of-three? (car ls) (cadr ls) (caddr ls))
            (fib-list? (cdr ls))
            #f))))

; Returns true iff the arguments form a fibonnacci sequence of length 3.
(define fib-sequence-of-three?
  (lambda (x y z)
    (= (+ x y) z)))

; Here's a different version that does not use if or cond:
(define fib-list?
  (lambda (ls)
    (or (null? (cddr ls))
        (and (fib-sequence-of-three? (car ls) (cadr ls) (caddr ls))
             (fib-list? (cdr ls))))))



(define score-test
  (lambda (answers key)
    (cond
     [(null? key) 0]
     [(equal? (car answers) '?) (score-test (cdr answers) (cdr key))]
     [(equal? (car key) (car answers))
      (+ 1 (score-test (cdr answers) (cdr key)))]
     [else
      (- (score-test (cdr answers) (cdr key)) .25)])))

(define insert-between
  (lambda (item pair)
    (cons (car pair)
	  (cons item (cdr pair)))))

(define exaggerate
  (lambda (adj)
    (cons 'very (cons 'very (cons 'very (cons adj '()))))))

(define reflect
  (lambda (a b)
    (cons a (cons b (cons b (cons a '()))))))

(define implode
  (lambda (digit-list)
    (+ (* (car digit-list) 100)
       (* (cadr digit-list) 10)
       (caddr digit-list))))

(define ls0 '(()))
(define ls0 (cons '() '()))
(define ls1 '(() ()))
(define ls1 (cons '() (cons '() '())))
(define ls2 '(() (())))
(define ls3 '(() (() ()) ()))
(define ls3 (cons '() (cons (cons '() (cons '() '())) (cons '() '()))))
(define ls4 '((() (()))))
(define ls4 (cons (cons '() (cons (cons '() '()) '())) '()))
(define ls5 '(() (() ((())))))

(define double-dare
  (lambda (ls)
    (if (null? ls)
	'()
	(if (equal? (car ls) 'dare)
	    (cons 'dare (cons 'dare (double-dare (cdr ls))))
	    (cons (car ls) (double-dare (cdr ls)))))))

(define age-group
  (lambda (age)
    (cond
     [(< age 13) 'child]
     [(< age 20) 'teen]
     [(>= age 65) 'senior]
     [else 'adult])))

(define coin-value
  (lambda (coin)
    (cond
     [(equal? coin 'quarter) 25]
     [(equal? coin 'dime) 10]
     [(equal? coin 'nickel) 5]
     [(equal? coin 'penny) 1]
     [else 0])))

(define dna-complement
  (lambda (base)
    (cond
     [(equal? base 'a) 't]
     [(equal? base 't) 'a]
     [(equal? base 'g) 'c]
     [(equal? base 'c) 'g]
     [else 'error])))

(define get-nucleotide
  (lambda (i)
    (cond
     [(= i 0) 'a]
     [(= i 1) 't]
     [(= i 2) 'g]
     [else 'c])))

(define make-dna-strand
  (lambda (n)
    (if (zero? n)
	'()
	(cons (get-nucleotide (random 4)) (make-dna-strand (- n 1))))))


(define periodic?
  (lambda (item n ls)
    (periodic-help? item 1 n ls)))

(define periodic-help?
  (lambda (item pos n ls)
    (if (null? ls)
        #t
        (if (zero? (remainder pos n))
            (and (equal? item (car ls))
                 (periodic-help? item (+ pos 1) n (cdr ls)))
            (periodic-help? item (+ pos 1) n (cdr ls))))))
                

(define list-add1
  (lambda (ls)
    (if (null? ls)
	'()
	(cons (add1 (car ls))
	      (list-add1 (cdr ls))))))

(define list-sqrt
  (lambda (ls)
    (if (null? ls)
	'()
	(cons (sqrt (car ls))
	      (list-sqrt (cdr ls))))))

(define invert
  (lambda (x)
    (if (zero? x)
	#f
	(/ x))))

(define reciprocals
  (lambda (ls)
    (if (null? ls)
	'()
	(cons (invert (car ls))
	      (reciprocals (cdr ls))))))

(define deepen
  (lambda (ls)
    (if (null? ls)
	'()
	(cons (cons (car ls) '())
	      (deepen (cdr ls))))))

(define sublist-lengths
  (lambda (ls)
    (if (null? ls)
	'()
	(cons (length (car ls))
	      (sublist-lengths (cdr ls))))))

(define hamming-distance
  (lambda (pat1 pat2)
    (if (null? pat1)
	0
	(+ (abs (- (car pat1) (car pat2)))
	   (hamming-distance (cdr pat1) (cdr pat2))))))


;; trim takes a non-empty list ls and removes all elements at the
;; beginning of ls that match the first element of ls.

(define trim
  (lambda (ls)
    (cond
     [(null? (cdr ls)) '()]
     [(first-two-same? ls) (trim (cdr ls))]
     [else (cdr ls)])))

; assumes ls contains two or more items
(define first-two-same?
  (lambda (ls)
    (equal? (car ls) (cadr ls))))

; Here's a different version that separates the first item in the list
; from the remainder and hands off to an iterative helper.

(define trim
  (lambda (ls)
    (trim-it (car ls) (cdr ls))))

(define trim-it
  (lambda (item ls)
    (cond
     [(null? ls) '()]
     [(equal? item (car ls)) (trim-it item (cdr ls))]
     [else ls])))


(define pick-one-at-random
  (lambda (a b)
    (if (zero? (random 2)) 
	a
	b)))

(define mouse-journey
  (lambda (cat mouse cheese)
    (cond
     [(= mouse cat) (list mouse 'sad)]
     [(= mouse cheese) (list mouse 'happy)]
     [else (cons mouse 
		 (mouse-journey cat 
				(+ mouse (pick-one-at-random 1 -1))
				cheese))])))

(define mouse-journey
  (lambda (cat mouse cheese)
    (random 1)
    (if (= mouse cat)
	(list mouse 'sad)
	(if (= mouse cheese)
	    (list mouse 'happy)
	    (cons mouse
		  (mouse-journey 
		   cat
		   (+ mouse (pick-one-at-random 1 -1))
		   cheese))))))

(define nucleotide-counts
  (lambda (strand)
    (list (list 'a (count-occurrences 'a strand))
	  (list 'c (count-occurrences 'c strand))
	  (list 'g (count-occurrences 'g strand))
	  (list 't (count-occurrences 't strand)))))

(define bigfoot
  (lambda (calls limit)
    (bigfoot-it calls limit 1 calls '())))

(define bigfoot-it
  (lambda (calls limit day total history)
    (if (>= total limit)
	(cons (list day limit) history)
	(bigfoot-it (* 2 calls) 
		    limit
		    (+ 1 day)
		    (+ total (* 2 calls))
		    (cons (list day total) history)))))

(define give-away
  (lambda (coins)
    (give-away-it coins 0 0)))

(define give-away-it
  (lambda (coins alice bob)
    (if (null? coins)
	(list alice bob)
	(if (< bob alice)
	    (give-away-it (cdr coins)
			  alice
			  (+ (car coins) bob))
	    (give-away-it (cdr coins)
			  (+ (car coins) alice)
			  bob)))))

(define run-mouse-program
  (lambda (cat mouse cheese program)
    (run-mouse-program-it cat mouse cheese program 0 'normal 'uneaten)))

(define run-mouse-program-it
  (lambda (cat mouse cheese program address termination-status cheese-status)
    (case (car program)
      [(eat) (if (and (= mouse cheese) (equal? cheese-status 'uneaten))
		 (run-mouse-program-it cat mouse cheese (cdr program) (+ address 1)
				       'normal 'eaten)
		 (terminate 'no-cheese-here address mouse cheese-status))]
      [(stop) (terminate 'normal address mouse cheese-status)]
      [(left) (if (= (- mouse 1) cat)
		  (terminate 'cat-got-me address (- mouse 1) cheese-status)
		  (run-mouse-program-it cat (- mouse 1) cheese (cdr program) 
					(+ address 1) 'normal cheese-status))]
      [(right) (if (= (+ mouse 1) cat)
		   (terminate 'cat-got-me address (+ mouse 1) cheese-status)
		   (run-mouse-program-it cat (+ mouse 1) cheese (cdr program) 
					 (+ address 1) 'normal cheese-status))]
      [else (terminate 'no-such-instruction address mouse cheese-status)])))

(define terminate
  (lambda (termination-status address mouse cheese-status)
    (list (list 'termination termination-status)
	  (list 'address address)
	  (list 'mouse-position mouse)
	  (list 'cheese cheese-status))))

(define execute-instruction
  (lambda (store instruction)
    (case (car instruction)
      [(clear) 0]
      [(load) (cadr instruction)]
      [(add) (+ store (cadr instruction))]
      [(sub) (- store (cadr instruction))]
      [(mult) (* store (cadr instruction))]
      [(div) (quotient store (cadr instruction))]
      [(print) (printf "~a~n" store) store]
      [(stop) 'done]
      [else 'error])))

(define execute-program
  (lambda (store program)
    (if (symbol? store)
	store
	(if (null? program)
	    'error
	    (execute-program 
	     (execute-instruction store (car program))
	     (cdr program))))))


; Exercise 1 --------------------------------------------------------------
;
;; num-digits takes a nonnegative integer n and returns the number of
;; digits in n.  Any unnecessary leading zeros in the input are not
;; counted as digits in the number.

(define num-digits
  (lambda (n)
    (if (< n 10)
        1
        (+ 1 (num-digits (quotient n 10))))))


; Exercise 2 --------------------------------------------------------------
;
;; count-occurrences takes an item and a list as its arguments and
;; returns the number of times the given item occurs in the given
;; list.

(define count-occurrences
  (lambda (item ls)
    (cond
     [(null? ls) 0]
     [(equal? (car ls) item) (add1 (count-occurrences item (cdr ls)))]
     [else (count-occurrences item (cdr ls))])))

;; Here's an alternate solution that uses let:

(define count-occurrences
  (lambda (item ls)
    (if (null? ls)
        0
        (let ([a (car ls)]
              [result (count-occurrences item (cdr ls))])
          (if (equal? a item)
              (add1 result)
              result)))))


(define pairwise-add
  (lambda (ls1 ls2)
    (if (null? ls1)
	'()
	(cons (+ (car ls1) (car ls2))
	      (pairwise-add (cdr ls1) (cdr ls2))))))

(define pairwise-match
  (lambda (ls1 ls2)
    (if (null? ls1)
	'()
	(cons (equal? (car ls1) (car ls2))
	      (pairwise-match (cdr ls1) (cdr ls2))))))


; Exercise 3 --------------------------------------------------------------
;
;; zip takes two lists, ls1 and ls2, of the same length and returns a
;; list that consists of two element sublists.  The first sublist in
;; the result consists of the first item in ls1 and the first item in
;; ls2.  The second sublist in the result consists of the second item
;; in ls1 and the second item in ls2, and so on.

(define zip
  (lambda (ls1 ls2)
    (if (null? ls1)
        '()
        (cons (list (car ls1) (car ls2))
              (zip (cdr ls1) (cdr ls2))))))


; Exercise 4 --------------------------------------------------------------
;
;; interleave takes two lists, ls1 and ls2, as its arguments and returns a
;; single list that starts with the first item in ls1, and then
;; alternates between the two lists for its successive items. If one
;; list is shorter than the other, the last items are taken from the
;; longer list.

(define interleave
  (lambda (ls1 ls2)
    (cond
     [(null? ls1) ls2]
     [(null? ls2) ls1]
     [else
      (cons (car ls1)
            (cons (car ls2)
                  (interleave (cdr ls1) (cdr ls2))))])))


; Exercise 5 --------------------------------------------------------------
;
;; oscillate takes three arguments: two items, first and second, and a
;; nonnegative integer n.  This procedure returns a list of length n
;; where the first item in the list is first, the next item is second,
;; the next is first again, then second, and so on.

(define oscillate
  (lambda (first second n)
    (cond
     [(zero? n) '()]
     [(= n 1) (cons first '())]
     [else (cons first
                 (cons second
                       (oscillate first second (- n 2))))])))

;; Here's an interesting alternate solution:
(define oscillate
  (lambda (first second n)
    (oscillate-helper first second n #t)))

(define oscillate-helper
  (lambda (first second n use-first?)
    (if (zero? n)
        '()
        (cons (if use-first?
                  first
                  second)
              (oscillate-helper first
                                second
                                (- n 1)
                                (not use-first?))))))

;; Here's yet another possibility:
(define oscillate
  (lambda (first second n)
    (if (zero? n)
        '()
        (cons first
              (oscillate second first (- n 1))))))


; Exercise 6 --------------------------------------------------------------
;
;; pinch takes an item and a list and returns the list with all
;; occurrences of item removed.

(define pinch
  (lambda (item ls)
    (cond
     [(null? ls) '()]
     [(equal? item (car ls))
      (pinch item (cdr ls))]
     [else (cons (car ls) (pinch item (cdr ls)))])))


; Exercise 7 --------------------------------------------------------------
;
;; replace takes two items and a list and returns the list with all
;; occurrences of the first item replaced with the second item.

(define replace
  (lambda (old new ls)
    (cond
     [(null? ls) '()]
     [(equal? (car ls) old)
      (cons new (replace old new (cdr ls)))]
     [else (cons (car ls) (replace old new (cdr ls)))])))


; Exercise 8 --------------------------------------------------------------
;
;; The procedure intersection takes two lists, ls1 and ls2, of symbols,
;; each containing no duplicated elements and returns
;; a list containing those elements of ls1 that are also in ls2.

(define intersection
  (lambda (ls1 ls2)
    (cond
     [(null? ls1) '()]
     [(member (car ls1) ls2)
      (cons (car ls1) (intersection (cdr ls1) ls2))]
     [else (intersection (cdr ls1) ls2)])))


; Exercise 9 --------------------------------------------------------------
;
;; every-nth-one takes a list ls and a positive integer n, and returns
;; a list that contans every nth element of ls starting with the nth
;; one.

(define every-nth-one
  (lambda (ls n)
    (let ([nth (has-nth ls n)])
      (if (not nth)
	  '()
	  (cons (car nth)
		(every-nth-one (cdr nth) n))))))

(define has-nth
  (lambda (ls n)
    (if (null? ls)
	#f
	(if (= n 1)
	    ls
	    (has-nth (cdr ls) (- n 1))))))

; Exercise 10 -------------------------------------------------------------
;
;; trick-or-treat? takes a list ls and returns #t if every item in ls
;; is the symbol trick or every item in ls is the symbol treat.
;; Otherwise, #f is returned.

(define trick-or-treat?
  (lambda (ls)
    (or (null? ls)
        (and (one-or-the-other (car ls) 'trick 'treat)
             (all-same? ls)))))

(define one-or-the-other?
  (lambda (item one other)
    (or (equal? item one)
        (equal? item other))))

;; From Assignment 2:
(define all-same?
  (lambda (ls)
    (or (null? ls)
        (null? (cdr ls))
        (and (equal? (car ls) (cadr ls))
             (all-same? (cdr ls))))))

;; Here's an alternate, less efficient, solution that makes use of
;; length and count-occurrences.
(define trick-or-treat?
  (lambda (ls)
    (let ([n (length ls)])
      (or (= n (count-occurrences 'trick ls))
          (= n (count-occurrences 'treat ls))))))


; Exercise 11 -------------------------------------------------------------
;
;; cats-and-dogs? takes a list ls and returns #t if ls contains only
;; the symbols cats and dogs and contains at least one occurrence of
;; each.  Otherwise, #f is returned.

(define cats-and-dogs?
  (lambda (ls)
    (cats-and-dogs-it? ls 0 0)))

(define cats-and-dogs-it?
  (lambda (ls cats dogs)
    (cond 
     [(null? ls) (positive? (* cats dogs))]
     [(equal? (car ls) 'cats) (cats-and-dogs-it? (cdr ls) (add1 cats) dogs)]
     [(equal? (car ls) 'dogs) (cats-and-dogs-it? (cdr ls) cats (add1 dogs))]
     [else #f])))

;; Here's an alternate, less efficient, solution that makes use of
;; length and count-occurrences.
(define cats-and-dogs?
  (lambda (ls)
    (let ([n (length ls)]
          [dogs (count-occurrences 'dogs ls)]
          [cats (count-occurrences 'cats ls)])
      (and (positive? dogs)
           (positive? cats)
           (= n (+ dogs cats))))))


; Exercise 12 -------------------------------------------------------------
;
;; count-forwards takes a nonnegative integer n and returns a list of
;; integers from 0 up to and including n.

(define count-forwards
  (lambda (n)
    (count-forwards-it n '())))

(define count-forwards-it
  (lambda (n acc)
    (if (< n 0)
        acc
        (count-forwards-it (sub1 n) (cons n acc)))))

;; Here's a solution that uses an aps helper, but is not iterative:

(define count-forwards
  (lambda (n)
    (count-forwards-help 0 n)))

(define count-forwards-help
  (lambda (curr limit)
    (if (> curr limit)
        '()
        (cons curr (count-forwards-help (add1 curr) limit)))))


; Exercise 13 -------------------------------------------------------------
;
;; unique that takes a list ls and returns a list consisting of the
;; first occurrence of each item in ls.  The original order of the
;; elements is preserved.

(define unique
  (lambda (ls)
    (unique-it ls '())))

(define unique-it
  (lambda (ls acc)
    (cond
     [(null? ls) (reverse acc)]
     [(member (car ls) acc) (unique-it (cdr ls) acc)]
     [else (unique-it (cdr ls) (cons (car ls) acc))])))

;; Here's a non-iterative solution that makes use of the pinch
;; procedure we defined previously:

(define unique
  (lambda (ls)
    (if (null? ls)
        '()
        (cons (car ls)
              (unique (pinch (car ls) (cdr ls)))))))


; Exercise 14 -------------------------------------------------------------
;
;; bet-winner takes a list of DJ's free-throw attempts and returns
;; the name of the winner of the bet.  The symbol DJ is returned if
;; there are five consecutive baskets.  Otherwise, the symbol Nikki is
;; returned.  For every basket that DJ makes on a free-throw attempt,
;; there is a b in the list and for every miss of a free-throw there is
;; an m.

(define bet-winner
  (lambda (attempts)
    (bet-winner-it attempts 0)))

(define run-length 5)

(define bet-winner-it
  (lambda (attempts made-so-far)
    (cond
     [(= made-so-far run-length) 'dj]
     [(null? attempts) 'nikki]
     [(equal? (car attempts) 'b)
      (bet-winner-it (cdr attempts) (+ 1 made-so-far))]
     [else (bet-winner-it (cdr attempts) 0)])))


; Exercise 15 -------------------------------------------------------------
;
;; coke-machine simulates the behavior of a coke machine.  This
;; procedure takes a nonnegative integer representing the initial
;; number of cokes in the machine and a list of legal inputs to a coke
;; machine.  The legal inputs are coin values (5, 10, and 25) and the
;; symbol press. A list containing the machine's output is returned.

(define coke-machine
  (lambda (num-cokes input)
    (coke-machine-help num-cokes input 0)))

(define cost-of-coke 60)

(define coke-machine-help
  (lambda (num-cokes input cents)
    (cond
     [(null? input) '()]
     [(number? (car input))
      ;; a coin was entered
      (coke-machine-help num-cokes (cdr input) (+ (car input) cents))]
     ;; from here on out, we know a button was just pressed
     [(zero? cents)
      ;; no money at all, so just ignore the press
      (coke-machine-help num-cokes (cdr input) 0)]
     [(or (zero? num-cokes) (< cents cost-of-coke))
      ;; not enough cokes or money so just give back the money
      (cons cents (coke-machine-help num-cokes (cdr input) 0))]
     [(> cents cost-of-coke)
      ;; dispense a coke and some change
      (cons 'coke
            (cons (- cents cost-of-coke)
                  (coke-machine-help (sub1 num-cokes) (cdr input) 0)))]
     [else
      ;; the exact amount was entered so just dispense a coke
      (cons 'coke
            (coke-machine-help (sub1 num-cokes) (cdr input) 0))])))


; Exercise 16 -------------------------------------------------------------
;
;; The procedure infix->prefix translates arithmetic expressions from
;; infix to prefix.  Arithmetic expressions in the input are assumed to
;; be numbers or three-element lists in which the first and third elements
;; are arithmetic expressions and the second element is a symbol representing
;; the operator.

(define infix->prefix
  (lambda (expr)
    (if (number? expr)
        expr
        (cons (cadr expr)
              (cons (infix->prefix (car expr))
                    (cons (infix->prefix (caddr expr)) '()))))))

;; Here's an alternate solution that uses the list procedure:

(define infix->prefix
  (lambda (expr)
    (if (number? expr)
        expr
        (list (cadr expr)
              (infix->prefix (car expr))
              (infix->prefix (caddr expr))))))


(define roll-die
  (lambda ()
    (+ 1 (random 6))))

(define doubles?
  (lambda ()
    (= (roll-die) (roll-die))))

(define take-turn
  (lambda ()
    (if (doubles?)
        (if (doubles?)
            (if (doubles?)
                3
                2)
            1)
        0)))

(define jail-probability
  (lambda (n)
    (/ (jail-frequency n) n)))
;    '?))

(define jail-frequency
  (lambda (n)
    (if (zero? n)
	0
	(+ (if (= 3 (take-turn)) 1 0) (jail-frequency (- n 1))))))

