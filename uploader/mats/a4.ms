;;; Spring 2009
;;; Assignment 4
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

(define ref-perfect-square?
  (lambda (x)
    (integer? (sqrt x))))

(define ref-curious?
  (lambda (n)
    (and (ref-perfect-square? (+ n 1))
         (ref-perfect-square? (+ (/ n 2) 1)))))

(define ref-next-curious
  (lambda (n)
    (define next-even
      (lambda (x)
        (if (even? x)
            (+ x 2)
            (+ x 1))))
    (let loop ([n (next-even n)])
      (if (ref-curious? n)
          n
          (loop (+ n 2))))))

(check-run (printf ""))

(grade-set "Problem 1: ls1" 1
  (check-if-bound ls1)
  (pretty-grade
   [ls1 ==> ,(cons 1 (cons 2 '()))]
   ))

(grade-set "Problem 1: ls2" 1
  (check-if-bound ls2)
  (pretty-grade
   [ls2 ==> ,(cons 3 (cons 4 (cons 5 '())))]
   ))

(grade-set "Problem 1: ls3" 1
  (check-if-bound ls3)
  (pretty-grade
   [ls3 ==> ,(cons (cons 6 '())
		  (cons (cons 7 '()) 
			(cons (cons 8 '()) '())))]
   ))

(grade-set "Problem 1: ls4" 1
  (check-if-bound ls4)
  (pretty-grade
   [ls4 ==> ,(cons (cons 9 (cons 10 '())) 
		  (cons 11 '()))]
   ))

(grade-set "Problem 1: ls5" 1
  (check-if-bound ls5)
  (pretty-grade
   [ls5 ==> ,(cons 12
		  (cons (cons 13 (cons 14 '())) '()))]
   ))

(grade-set "Problem 1: ls6" 1
  (check-if-bound ls6)
  (pretty-grade
   [ls6 ==> ,(cons 15
		  (cons (cons 16 (cons (cons 17 '()) '())) '()))]
   ))

(grade-set "Problem 1: ls7" 1
  (check-if-bound ls7)
  (pretty-grade
   [ls7 ==> (((18) 19) 20)]
   ))

(grade-set "Problem 1: ls8" 1
  (check-if-bound ls8)
  (pretty-grade
   [ls8 ==> ,(list 'a 'b 'c 'd 'e 'f)]
   ))


(grade-set "Problem 1: ls9" 1
  (check-if-bound ls9)
  (pretty-grade
   [ls9 ==> ,(list (list (list (list 'g))))]
   ))


(grade-set "Problem 1: ls10" 1
  (check-if-bound ls10)
  (pretty-grade
   [ls10 ==> ,(list (list 'h 'i) (list 'j 'k) (list 'm 'n))]
   ))


(grade-set "Problem 2: neighbors" 1
  (check-if-bound neighbors)
  (pretty-grade
   [(neighbors 3) ==> (2 4)]
   [(neighbors 0) ==> (-1 1)]
   [(neighbors -7) ==> (-8 -6)]
   [(neighbors 10) ==> (9 11)]
   [(neighbors 42) ==> (41 43)]
   [(neighbors -1) ==> (-2 0)]
  ))

(grade-set "Problem 3: extend-sequence" 1
  (check-if-bound extend-sequence)
  (pretty-grade
   [(extend-sequence '(5)) ==> (4 5)]
   [(extend-sequence '(7 0 2 5 1)) ==> (6 7 0 2 5 1)]
   [(extend-sequence (extend-sequence (extend-sequence '(5 4))))
    ==> (2 3 4 5 4)]
   [(extend-sequence '(-5)) ==> (-6 -5)]
   [(extend-sequence '(99 bottles of soda)) ==> (98 99 bottles of soda)]
   [(extend-sequence '(6 7 8)) ==> (5 6 7 8)]
   ))

(grade-set "Problem 4: scrunch-bits" 1
  (check-if-bound scrunch-bits)
  (pretty-grade
   [(scrunch-bits '(1 1 1 0 1 1)) ==> (3 1 0 1 1)]
   [(scrunch-bits '(0 1 0)) ==> (1 0)]
   [(scrunch-bits '(0 0)) ==> (0)]
   [(scrunch-bits '(1 0)) ==> (2)]
   [(scrunch-bits '(0 1)) ==> (1)]
   [(scrunch-bits '(1 1)) ==> (3)]
   [(scrunch-bits '(0 0 0)) ==> (0 0)]
   [(scrunch-bits '(1 0 0)) ==> (2 0)]
   [(scrunch-bits '(0 1 0)) ==> (1 0)]
   [(scrunch-bits '(1 1 0)) ==> (3 0)]
   [(scrunch-bits '(0 0 1)) ==> (0 1)]
   [(scrunch-bits '(1 0 1)) ==> (2 1)]
   [(scrunch-bits '(0 1 1)) ==> (1 1)]
   [(scrunch-bits '(1 1 1)) ==> (3 1)]
   ))

(grade-set "Problem 5: count-down" 1
  (check-if-bound count-down)
  (pretty-grade
    [(count-down 1)  ==>  (1 blastoff!)]
    [(count-down 2)  ==>  (2 1 blastoff!)]
    [(count-down 3)  ==>  (3 2 1 blastoff!)]
    [(count-down 4)  ==>  (4 3 2 1 blastoff!)]
    [(count-down 5)  ==>  (5 4 3 2 1 blastoff!)]
    [(count-down 6)  ==>  (6 5 4 3 2 1 blastoff!)]
    [(count-down 7)  ==>  (7 6 5 4 3 2 1 blastoff!)]
    [(count-down 17)  ==>  (17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1 blastoff!)]
    ))

(grade-set "Problem 6: hugs-and-kisses" 1
  (check-if-bound hugs-and-kisses)
  (pretty-grade
   [(hugs-and-kisses 0)  ==> ()]
   [(hugs-and-kisses 1)  ==> (x o)]
   [(hugs-and-kisses 2)  ==> (x o x o)]
   [(hugs-and-kisses 3)  ==> (x o x o x o)]
   [(hugs-and-kisses 4)  ==> (x o x o x o x o)]
   [(hugs-and-kisses 5)  ==> (x o x o x o x o x o)]
   [(hugs-and-kisses 6)  ==> (x o x o x o x o x o x o)]
   [(hugs-and-kisses 12) ==> (x o x o x o x o x o x o x o x o x o x o x o x o)]
   ))

(grade-set "Problem 7: bean-counter" 1
  (check-if-bound bean-counter)
  (pretty-grade
    [(bean-counter '())                                     ==>  0]
    [(bean-counter '(bean (bean bean) b e a n bean))        ==>  2]
    [(bean-counter '(one bean plus one bean is two beans))  ==>  2]
    [(bean-counter '(a b c d e f g h i j k l m n o p q))    ==>  0]
    [(bean-counter '(bean 0 0 0 0 0 0 bean 0 0 0 0 0 bean)) ==>  3]
    [(bean-counter '(bean bean bean bean bean bean bean))   ==>  7]
    [(bean-counter '(0 bean 0 bean 0 1 bean 0 bean 0 bean 
                     0 bean 0 bean 0 bean 0 1 2 3 bean 0 bean 
                     0 bean 0 1 2 bean 0 bean 0 bean 0 bean 0))
       ==> 15]
    [(bean-counter '(z z z z z z z z z z z z z z z z z z z 
                     z z z z z z z z z z z z z z z z z bean))
       ==> 1]
    [(bean-counter '(#t bean w bean #f bean y bean))        ==> 4]
    [(bean-counter '(abc))  ==> 0]
    [(bean-counter '(bean)) ==> 1]
    [(bean-counter '(#t #f)) ==> 0]
    [(bean-counter '(7 bean)) ==> 1]
    [(bean-counter '(bean 7)) ==> 1]
    [(bean-counter '(bean bean)) ==> 2]
    [(bean-counter '(p q r)) ==> 0]
    [(bean-counter '(p q bean)) ==> 1]
    [(bean-counter '(p bean r)) ==> 1]
    [(bean-counter '(bean q r)) ==> 1]
    [(bean-counter '(p bean bean)) ==> 2]
    [(bean-counter '(bean q bean)) ==> 2]
    [(bean-counter '(bean bean r)) ==> 2]
    [(bean-counter '(bean bean bean)) ==> 3]
    ;; to thwart Ranger Davis:
    [(bean-counter '(_&*_counter 200 bean bean bean)) ==> 3] 
    ))

(grade-set "Problem 8a: coin->cents" 1
  (check-if-bound coin->cents)
  (pretty-grade
   [(coin->cents 'penny) ==> 1]
   [(coin->cents 'nickel) ==> 5]
   [(coin->cents 'dime) ==> 10]
   [(coin->cents 'quarter) ==> 25]
   [(coin->cents 'slug) ==> 0]
   [(coin->cents 5) ==> 0]
   [(coin->cents 'a) ==> 0]
   [(coin->cents 'coin) ==> 0]
))

(grade-set "Problem 8b: inventory-pockets" 1
  (check-if-bound inventory-pockets)
  (pretty-grade
   [(inventory-pockets '())                          ==> 0]
   [(inventory-pockets '(penny))                     ==> 1]
   [(inventory-pockets '(nickel penny))              ==> 6]
   [(inventory-pockets '(dime nickel penny))         ==> 16]
   [(inventory-pockets '(quarter dime nickel penny)) ==> 41]
   [(inventory-pockets '(lint toad pen-knife))       ==> 0]
   [(inventory-pockets
     '(penny
       quarter
       ticket-stub
       dime
       receipt
       quarter
       gum-wrapper
       nickel
       penny
       string))
    ==> 67]
   [(inventory-pockets '(penny penny nickel nickel dime dime quarter quarter))
    ==> 82]
   [(inventory-pockets '(quarter quarter quarter
			 dime dime dime
			 nickel nickel nickel
			 penny penny penny))
    ==> 123]
   [(inventory-pockets '(quarter dime nickel penny
			 penny nickel dime quarter
			 quarter dime nickel penny
			 penny nickel dime quarter))
    ==> 164]
   [(inventory-pockets '(no money in this pocket))             ==> 0]
   [(inventory-pockets '(just a dime here and a nickel there)) ==> 15]
   [(inventory-pockets '(penny lint))                          ==> 1]
   ))

(grade-set "Problem 9: double-dare" 1
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

(grade-set "Problem 10: penny-pincher" 1
  (check-if-bound penny-pincher)
  (pretty-grade
    [(penny-pincher '())  ==>  ()]
    [(penny-pincher '(a penny earned is a penny saved))  
     ==>  (a earned is a saved)]
    [(penny-pincher '(penny (penny) dime penny penny nickel))            
     ==>  ((penny) dime nickel)]
    [(penny-pincher '(penny penny penny penny 1 penny penny penny penny))
     ==>  (1)]
    [(penny-pincher '(a b c d e f g h i j k l m n o p q r s t u v w x y z))
     ==>  (a b c d e f g h i j k l m n o p q r s t u v w x y z)]
    [(penny-pincher '(1 penny penny 2 penny 3 penny 4 5 6 penny 7 8))
     ==>  (1 2 3 4 5 6 7 8)]
    [(penny-pincher '(penny))
     ==>  ()]
    [(penny-pincher '(penny penny))
     ==>  ()]
    [(penny-pincher '(penny #t penny #f penny))
     ==> (#t #f)]
    [(penny-pincher '(9)) ==> (9)]
    [(penny-pincher '(9 8)) ==> (9 8)]
    [(penny-pincher '(9 penny)) ==> (9)]
    [(penny-pincher '(penny 9)) ==> (9)]
    [(penny-pincher '(9 8 7)) ==> (9 8 7)]
    [(penny-pincher '(9 8 penny)) ==> (9 8)]
    [(penny-pincher '(9 penny 7)) ==> (9 7)]
    [(penny-pincher '(penny 8 7)) ==> (8 7)]
    [(penny-pincher '(9 penny penny)) ==> (9)]
    [(penny-pincher '(penny 8 penny)) ==> (8)]
    [(penny-pincher '(penny penny 7)) ==> (7)]
    [(penny-pincher '(penny penny penny)) ==> ()]
  ))

(grade-set "Problem 11 (extra credit): next-curious" 1
  (check-if-bound next-curious)
  (pretty-grade-all next-curious ref-next-curious
    ( ( 5 )
      ( 48 )
      ( 100 )
      ( 65000000 ) )))



#!eof

(grade-set "Problem 6: sum-squares" 1
  (check-if-bound sum-squares)
  (pretty-grade
   [(sum-squares 3) ==> 14]
   [(sum-squares 4) ==> 30]
   [(sum-squares 100) ==> 338350]
   [(sum-squares 0) ==> 0]
   [(sum-squares 1) ==> 1]
   [(sum-squares 2) ==> 5]
   [(sum-squares 5) ==> 55]
   [(sum-squares 6) ==> 91]
   ))

    
(grade-set "Problem 5: count-backwards" 1
  (check-if-bound count-backwards)
  (pretty-grade
    [(count-backwards 0)  ==>  (0)]
    [(count-backwards 1)  ==>  (1 0)]
    [(count-backwards 2)  ==>  (2 1 0)]
    [(count-backwards 3)  ==>  (3 2 1 0)]
    [(count-backwards 4)  ==>  (4 3 2 1 0)]
    [(count-backwards 5)  ==>  (5 4 3 2 1 0)]
    [(count-backwards 6)  ==>  (6 5 4 3 2 1 0)]
    [(count-backwards 7)  ==>  (7 6 5 4 3 2 1 0)]
    [(count-backwards 17)  ==>  (17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1 0)]
    ))
(grade-set "Problem 4: scrunch-sequence" 1
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

(grade-set "Problem 3a: color-ref" 1
  (check-if-bound color-ref)
  (pretty-grade
   [(color-ref '(1 2 3) 'red) ==> 1]
   [(color-ref '(1 2 3) 'green) ==> 2]
   [(color-ref '(1 2 3) 'blue) ==> 3]
   [(color-ref '(4 5 6) 'red) ==> 4]
   [(color-ref '(4 5 6) 'green) ==> 5]
   [(color-ref '(4 5 6) 'blue) ==> 6]
  ))

#|

(grade-set "Problem 3b: spin" 1
  (check-if-bound spin)
  (pretty-grade
   [(spin (color 1 2 3)) ==> ,(color 2 3 1) by color-equal?]
   [(spin (color 1 3 2)) ==> ,(color 3 2 1) by color-equal?]
   [(spin (color 2 1 3)) ==> ,(color 1 3 2) by color-equal?]
   [(spin (color 2 3 1)) ==> ,(color 3 1 2) by color-equal?]
   [(spin (color 3 1 2)) ==> ,(color 1 2 3) by color-equal?]
   [(spin (color 3 2 1)) ==> ,(color 2 1 3) by color-equal?]
))

|#

(grade-set "Problem 3b: spin" 1
  (check-if-bound spin)
  (pretty-grade
   [(spin (list 1 2 3)) ==> ,(list 2 3 1)]
   [(spin (list 1 3 2)) ==> ,(list 3 2 1)]
   [(spin (list 2 1 3)) ==> ,(list 1 3 2)]
   [(spin (list 2 3 1)) ==> ,(list 3 1 2)]
   [(spin (list 3 1 2)) ==> ,(list 1 2 3)]
   [(spin (list 3 2 1)) ==> ,(list 2 1 3)]
))



(grade-set "Problem 1a: ls3" 1
  (check-if-bound ls3)
  (pretty-grade
   [ls3 ==> ,(list (list (list 'p)) (list (list 'q)) (list (list 'r)))]
   ))


(grade-set "Problem 1a: ls4" 1
  (check-if-bound ls4)
  (pretty-grade
   [ls4 ==> ,(list 's (list 't (list 'u (list 'v))))]
   ))

(grade-set "Problem 2: re-colorize" 1
  (check-if-bound re-colorize)
  (pretty-grade
   [(let ((image #(#(#(3 1 2) #(6 4 5) #(9 7 8))
      #(#(12 10 11) #(15 13 14) #(18 16 17))
      #(#(21 19 20) #(24 22 23) #(27 25 26)))))
      (re-colorize image))
    ==> #(#(#(1 2 3) #(4 5 6) #(7 8 9))
          #(#(10 11 12) #(13 14 15) #(16 17 18))
          #(#(19 20 21) #(22 23 24) #(25 26 27)))
    ]
))

(grade-set "Problem 6: reciprocals" 1
 (check-if-bound reciprocals)
 (pretty-grade
  [(reciprocals '())                ==> ()]
  [(reciprocals '(2))               ==> (1/2)]
  [(reciprocals '(0))               ==> (#f)]
  [(reciprocals '(4 5))             ==> (1/4 1/5)]
  [(reciprocals '(7 0))             ==> (1/7 #f)]
  [(reciprocals '(0 11))            ==> (#f 1/11)]
  [(reciprocals '(0 0))             ==> (#f #f)]
  [(reciprocals '(9 10 11))         ==> (1/9 1/10 1/11)]
  [(reciprocals '(22 8 0))          ==> (1/22 1/8 #f)]
  [(reciprocals '(16 0 -4))         ==> (1/16 #f -1/4)]
  [(reciprocals '(0 88 37))         ==> (#f 1/88 1/37)]
  [(reciprocals '(99 0 0))          ==> (1/99 #f #f)]
  [(reciprocals '(0 45 0))          ==> (#f 1/45 #f)]
  [(reciprocals '(0 0 33))          ==> (#f #f 1/33)]
  [(reciprocals '(0 0 0))           ==> (#f #f #f)]
  [(reciprocals '(4 9 0 2/3 0 0 3)) ==> (1/4 1/9 #f 3/2 #f #f 1/3)]
  [(reciprocals '(0 1 0 2 0 3 0 4 0 5 0 0 6 7 0 8 0 9 0 10 0))
   ==> (#f 1 #f 1/2 #f 1/3 #f 1/4 #f 1/5 #f #f 1/6 1/7 #f 1/8 #f 1/9 #f 1/10 #f)]
  ))


(grade-set "Problem 8: upstairs" 1
  (check-if-bound upstairs)
  (pretty-grade
    [(upstairs 0)  ==>  ()]
    [(upstairs 1)  ==>  (up)]
    [(upstairs 2)  ==>  (up (up))]
    [(upstairs 3)  ==>  (up (up (up)))]
    [(upstairs 4)  ==>  (up (up (up (up))))]
    [(upstairs 5)  ==>  (up (up (up (up (up)))))]
    [(upstairs 6)  ==>  (up (up (up (up (up (up))))))]
    [(upstairs 7)  ==>  (up (up (up (up (up (up (up)))))))]
    [(upstairs 10) ==>  (up (up (up (up (up (up (up (up (up (up))))))))))]
    ))

(grade-set "Problem 10a: dna-complement" 1
  (check-if-bound dna-complement)
  (pretty-grade
   [(dna-complement 'a) ==> t]             
   [(dna-complement 't) ==> a]         
   [(dna-complement 'g) ==> c]
   [(dna-complement 'c) ==> g]
   [(dna-complement 'k) ==> error]
   [(dna-complement 'quarter) ==> error]
   ))

(grade-set "Problem 10b: make-dna-strand" 1
  (check-if-bound make-dna-strand)
  (pretty-grade
   [($verify-dna-strand$ (make-dna-strand 0) 0)     ==> #t]
   [($verify-dna-strand$ (make-dna-strand 1) 1)     ==> #t]
   [($verify-dna-strand$ (make-dna-strand 2) 2)     ==> #t]
   [($verify-dna-strand$ (make-dna-strand 3) 3)     ==> #t]
   [($verify-dna-strand$ (make-dna-strand 4) 4)     ==> #t]
   [($verify-dna-strand$ (make-dna-strand 10) 10)   ==> #t]
   [($verify-dna-strand$ (make-dna-strand 100) 100) ==> #t]
   ))

(grade-set "Problem 11: all-even?" 1
  (check-if-bound all-even?)
  (pretty-grade
   [(all-even? '())                   ==> #t]
   [(all-even? '(2 4 6 8))            ==> #t]
   [(all-even? '(2 3 4 5 6 7 8 9))    ==> #f]
   [(all-even? '(two four six eight)) ==> #f]                 
   [(all-even? '(2 4 6 8 10 (12)))    ==> #f]
   [(all-even? '(2 4 7))              ==> #f]
   [(all-even? '(2 4 'a 4))           ==> #f]
   [(all-even? '(0 0 0 0 0 0 0 2 4 6 8 18 34 56 98)) ==> #t]
   [(all-even? '(() hello there quote (1 2 3))) ==> #f]
   ))


#!eof

(grade-set "Problem 5: zip" 1
  (check-if-bound zip)
  (pretty-grade
   [(zip '(a b c d) '(w x y z)) ==> ((a w) (b x) (c y) (d z))]
   [(zip '() '())               ==> ()]
   [(zip '(1) '(2))             ==> ((1 2))]
   [(zip '(1 3) '(2 4))         ==> ((1 2) (3 4))]
   [(zip '(1 3 5) '(2 4 6))     ==> ((1 2) (3 4) (5 6))]
   [(zip '(1 3 5 7 9) '(2 4 6 8 0)) ==> ((1 2) (3 4) (5 6) (7 8) (9 0))]
   [(zip '(q w e r t y u i o p) '(a s d f g h j k l z))
    ==> ((q a) (w s) (e d) (r f) (t g) (y h) (u j) (i k) (o l) (p z))]
   ))

(grade-set "Problem 6: pinch" 1
  (check-if-bound pinch)
  (pretty-grade
   [(pinch 'penny '(quarter penny penny dime penny)) ==> (quarter dime)]     
   [(pinch 'trick '(trick trick trick trick))        ==> ()]
   [(pinch 'a '())                                   ==> ()]
   [(pinch 1 '(1))                                   ==> ()]
   [(pinch 1 '(0 1))                                 ==> (0)]
   [(pinch 1 '(1 0))                                 ==> (0)]
   [(pinch 'a '(a a a))                              ==> ()]
   [(pinch 'a '(a a b))                              ==> (b)]
   [(pinch 'a '(a c a))                              ==> (c)]
   [(pinch 'a '(d a a))                              ==> (d)]
   [(pinch 'a '(a e f))                              ==> (e f)]
   [(pinch 'a '(g a h))                              ==> (g h)]
   [(pinch 'a '(i j a))                              ==> (i j)]
   [(pinch 'a '(k l m))                              ==> (k l m)]
   [(pinch 'x '(x q x w e x r t y x x u x i o x p x))
    ==> (q w e r t y u i o p)]
   ))

(grade-set "Problem 7: replace" 1
  (check-if-bound replace)
  (pretty-grade
   [(replace 'old 'new '()) ==> ()]
   [(replace 'penny 'nickel '(quarter penny penny dime penny))
    ==> (quarter nickel nickel dime nickel)]
   [(replace 'trick 'treat '(trick trick trick trick))
    ==> (treat treat treat treat)]
   [(replace 'a 'b '(a b c a a b c a a a b c)) ==> (b b c b b b c b b b b c)]
   [(replace 0 1 '(0)) ==> (1)]
   [(replace 0 1 '(1)) ==> (1)]
   [(replace 0 1 '(2)) ==> (2)]
   [(replace 0 1 '(0 0)) ==> (1 1)]
   [(replace 0 1 '(0 1)) ==> (1 1)]
   [(replace 0 1 '(0 2)) ==> (1 2)]
   [(replace 0 1 '(1 0)) ==> (1 1)]
   [(replace 0 1 '(1 1)) ==> (1 1)]
   [(replace 0 1 '(1 2)) ==> (1 2)]
   [(replace 0 1 '(2 0)) ==> (2 1)]
   [(replace 0 1 '(2 1)) ==> (2 1)]
   [(replace 0 1 '(2 2)) ==> (2 2)]
   [(replace 'q 'w '(a w s q d f g w h q n x q q d w w n r q))
    ==> (a w s w d f g w h w n x w w d w w n r w)]
   ))

(grade-set "Problem 8: count-occurrences" 1
  (check-if-bound count-occurrences)
  (pretty-grade
   [(count-occurrences 'na '(ba na na na sha na na na)) ==> 6]
   [(count-occurrences 'bean '(bean bag and jelly bean and string bean))
    ==> 3]
   [(count-occurrences 'y '(a e i o u))                 ==> 0]
   [(count-occurrences 'who '())                        ==> 0]
   [(count-occurrences 3 '(1 2 3 2 3 2 1))   ==> 2]
   [(count-occurrences 'a '(b a n a n a s))  ==> 3]
   [(count-occurrences 'as '(is it in us))   ==> 0]
   [(count-occurrences 0 '())                ==> 0]
   [(count-occurrences 0 '(0))               ==> 1]
   [(count-occurrences 0 '(9))               ==> 0]
   [(count-occurrences 0 '(0 0))             ==> 2]
   [(count-occurrences 0 '(0 9))             ==> 1]
   [(count-occurrences 0 '(9 9))             ==> 0]
   [(count-occurrences 0 '(9 0))             ==> 1]
   [(count-occurrences 0 '(0 0 0))           ==> 3]
   [(count-occurrences 0 '(0 0 9))           ==> 2]
   [(count-occurrences 0 '(0 9 0))           ==> 2]
   [(count-occurrences 0 '(0 9 9))           ==> 1]
   [(count-occurrences 0 '(9 0 0))           ==> 2]
   [(count-occurrences 0 '(9 0 9))           ==> 1]
   [(count-occurrences 0 '(9 9 0))           ==> 1]
   [(count-occurrences 0 '(9 9 9))           ==> 0]
   [(count-occurrences 1 '(1 3 1 1 5 0 6 1 a a a 1 a a b 1 w)) ==> 6]
   ))

(grade-set "Problem 9: score-test" 1
  (check-if-bound score-test)
  (pretty-grade
   [(score-test '() '()) ==> 0]
   [(score-test '(?) '(a)) ==> 0]
   [(score-test '(a) '(a)) ==> 1]
   [(score-test '(a) '(b)) ==> -0.25]
   [(score-test '(? ? ? ?) '(a c c b)) ==> 0]
   [(score-test '(a c c b) '(a c c b)) ==> 4]
   [(score-test '(a b d e a c ? b d c)
                '(a c d e b c e b a c)) ==> 5.25]
))

(grade-set "Problem 10: mouse-journey" 1
  (check-if-bound mouse-journey)
  (begin ($set-random-sequence$ '()) #t)
  (pretty-grade
   [($verify-journey$ (mouse-journey 0 3 6) 0 3 6) ==> #t]
   [($verify-journey$ (mouse-journey 7 4 -1) 7 4 -1) ==> #t]
   [($verify-journey$ (mouse-journey 99 97 95) 99 97 95) ==> #t]
   [($verify-journey$ (mouse-journey -22 -21 -20) -22 -21 -20) ==> #t]
   [($verify-journey$ (mouse-journey 1 2 3) 1 2 3) ==> #t]
   [($verify-journey$ (mouse-journey 10 20 30) 10 20 30) ==> #t]
   [($verify-journey$ (mouse-journey 30 20 10) 30 20 10) ==> #t]
   [($verify-journey$ (mouse-journey 1 6 8) 1 6 8) ==> #t]
   [($verify-journey$ (mouse-journey 1 3 8) 1 3 8) ==> #t]
   [($verify-journey$ (mouse-journey 20 15 1) 20 15 1) ==> #t]
   [($verify-journey$ (mouse-journey 10 5 1) 10 5 1) ==> #t]
   [($verify-journey$ (mouse-journey 0 3 6) 0 3 6) ==> #t]
   [($verify-journey$ (mouse-journey 7 4 -1) 7 4 -1) ==> #t]
   [($verify-journey$ (mouse-journey 99 97 95) 99 97 95) ==> #t]
   [($verify-journey$ (mouse-journey -22 -21 -20) -22 -21 -20) ==> #t]
   [($verify-journey$ (mouse-journey 1 2 3) 1 2 3) ==> #t]
   [($verify-journey$ (mouse-journey 10 20 30) 10 20 30) ==> #t]
   [($verify-journey$ (mouse-journey 30 20 10) 30 20 10) ==> #t]
   [($verify-journey$ (mouse-journey 1 6 8) 1 6 8) ==> #t]
   [($verify-journey$ (mouse-journey 1 3 8) 1 3 8) ==> #t]
   [($verify-journey$ (mouse-journey 20 15 1) 20 15 1) ==> #t]
   [($verify-journey$ (mouse-journey 10 5 1) 10 5 1) ==> #t]
   [($verify-journey$ (mouse-journey 0 3 6) 0 3 6) ==> #t]
   [($verify-journey$ (mouse-journey 7 4 -1) 7 4 -1) ==> #t]
   [($verify-journey$ (mouse-journey 99 97 95) 99 97 95) ==> #t]
   [($verify-journey$ (mouse-journey -22 -21 -20) -22 -21 -20) ==> #t]
   [($verify-journey$ (mouse-journey 1 2 3) 1 2 3) ==> #t]
   [($verify-journey$ (mouse-journey 10 20 30) 10 20 30) ==> #t]
   [($verify-journey$ (mouse-journey 30 20 10) 30 20 10) ==> #t]
   [($verify-journey$ (mouse-journey 1 6 8) 1 6 8) ==> #t]
   [($verify-journey$ (mouse-journey 1 3 8) 1 3 8) ==> #t]
   [($verify-journey$ (mouse-journey 20 15 1) 20 15 1) ==> #t]
   [($verify-journey$ (mouse-journey 10 5 1) 10 5 1) ==> #t]
   ))

#!eof


(grade-set "Problem 1b: exaggerate" 1
  (check-if-bound exaggerate)
  (pretty-grade
   [(exaggerate 'exciting) ==> (very very very exciting)]
   [(exaggerate 'boring)   ==> (very very very boring)]
   [(exaggerate 'hot)      ==> (very very very hot)]
   [(exaggerate 'very)     ==> (very very very very)]
   [(exaggerate 'happy)    ==> (very very very happy)]
   ))

(grade-set "Problem 1c: implode" 1
  (check-if-bound implode)
  (pretty-grade
   [(implode '(1 2 3)) ==> 123]
   [(implode '(0 0 9)) ==> 9]
   [(implode '(9 9 9)) ==> 999]
   [(implode '(6 5 4)) ==> 654]
   [(implode '(6 0 5)) ==> 605]
   [(implode '(6 5 0)) ==> 650]
   [(implode '(0 6 5)) ==> 65]
   [(implode '(0 8 0)) ==> 80]
   [(implode '(8 0 0)) ==> 800]
   [(implode '(0 0 0)) ==> 0]
   ))

(grade-set "Problem 2: ls0" 1
  (check-if-bound ls0)
  (pretty-grade
   [ls0 ==> (())]
   ))

(grade-set "Problem 2: ls1" 1
  (check-if-bound ls1)
  (pretty-grade
   [ls1 ==> (() ())]
   ))

(grade-set "Problem 2: ls2" 1
  (check-if-bound ls2)
  (pretty-grade
   [ls2 ==> (() (()))]
   ))

(grade-set "Problem 2: ls3" 1
  (check-if-bound ls3)
  (pretty-grade
   [ls3 ==> (() (() ()) ())]
   ))

(grade-set "Problem 2: ls4" 1
  (check-if-bound ls4)
  (pretty-grade
   [ls4 ==> ((() (())))]
   ))

(grade-set "Problem 2: ls5" 1
  (check-if-bound ls5)
  (pretty-grade
   [ls5 ==> (() (() ((()))))]
   ))

