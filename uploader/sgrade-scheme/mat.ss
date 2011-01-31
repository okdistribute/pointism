;;; ==============================
;;; mat.ss
;;; deals with the mat files, and the syntax thereof
;;; ==============================

;;;------------------------------
;; formatted output

(include "sgrade-scheme/hereis.ss")

;;; ------------------------------
;;; accumulator variables

(define mat-score 0)
(define mat-total 0)

;; there are two interfaces for grading:

(define-syntax grade-set
  (lambda (x)
    (syntax-case x ()
      [(_ name points exp ...)
       (number? (syntax-object->datum (syntax points)))
       (syntax
	 (begin
	   (set! mat-total (+ mat-total points))
	   (myprintf "~20a --> ~a" (quote name)
	    (let* ([op (open-output-string)]
		   [v (parameterize ([current-output-port op])
			(and exp ...))])
	      (if v
		  (begin
		    (set! mat-score (+ mat-score points))
		    (myformat "  correct: ~-2a/~a~n~a" points points
		      (get-output-string op)))
		  (myformat "incorrect:  0/~a~n~a" points
		    (get-output-string op)))))))])))

(define-syntax safely
  (syntax-rules ()
    [(% %e ...)
     (run-safely sgrade-tics sgrade-bytes
       (lambda () (values (eval `%e) ...)))])) ;; !!! special!

(define-syntax check-if-bound-proper
  (syntax-rules ()
    [(% %v)
     (or (and (top-level-bound? '%v) %v)
	 (begin
	   (when visible? 
		 (printf "   ~a is not bound~n" '%v))
	   #f))]))

(define-syntax check-if-bound
  (syntax-rules ()
    [(% %v)
     (or (top-level-bound? '%v)
	 (begin
	   (when visible?
	     (printf "   ~a not bound~n" '%v))
	   #f))]))

(define-syntax check
  (syntax-rules ()
    [(% %f %e ...)
     (mv-let ([(v out) (safely %e ...)])
       (record-case v
	 [values vals
	   (or (apply %f vals)
	       (notify-bad-return '(%f %e ...)
		 `(%f ,@(map (lambda (x) `',x) vals))))]
	 [else
	   (notify-bad-error '(%f %e ...) v)]))]))

(define-syntax check-run
  (syntax-rules ()
    [(% %e0 %e ...)
     (mv-let ([(v out) (safely (begin %e0 %e ...))])
       (record-case v
	 [values ignored
	   (display out)
	   (newline)
	   #t]
	 [else
	   (notify-bad-error '(begin %e0 %e ...) v)]))]))

(define-syntax check-output
  (syntax-rules ()
    [(% %f %e)
     (mv-let ([(v out) (safely %e)])
       (record-case v
	 [values ignored
	   (or (%f out) (notify-bad-output '%e out))]
	 [else
	   (notify-bad-error '%e v)]))]))

(define-syntax check-output-equiv
  (lambda (x)
    (syntax-case x ()
      [(% %f %e %s)
       (string? (syntax-object->datum (syntax %s)))
       (syntax
	 (check-output (lambda (x) (%f x %s)) %e))])))

(define-syntax check-if-error
  (syntax-rules (non-system)
    [(% (quote %from) %e)
     (mv-let ([(v out) (safely %e)])
       (record-case v
	 [values (v) (notify-bad-return '%e v)]
	 [error (who what . rest)
	   (or (eq? '%from who)
	       (notify-bad-error '%e v))]
	 [else
	   (notify-bad-error '%e v)]))]
    [(% non-system %e)
     (mv-let ([(v out) (safely %e)])
       (record-case v
	 [values (v) (notify-bad-return '%e v)]
	 [error (who what . rest)
	   (or who (notify-bad-error '%e v))]
	 [else (notify-bad-error '%e v)]))]
    [(% %e)
     (mv-let ([(v out) (safely %e)])
       (record-case v
	 [values (v) (notify-bad-return '%e v)]
	 [error (who what . rest) #t]
	 [else (notify-bad-error '%e v)]))]))

(define-syntax hint
  (syntax-rules ()
    [(_ test str)
     (let ([x test])
       (unless (and x (not (string=? str "")))
	 (printf "  Hint: ~a~n" str))
       x)]))

;;; ------------------------------
;;; compatability

(define-syntax define-output-test
  (syntax-rules ()
    [(% %name %fun)
     (define-syntax %name
       (syntax-rules ()
	 [(%% %%exp %%str)
	  (check-output-equiv %fun %%exp %%str)]))]))

(define-syntax define-equality-test
  (syntax-rules ()
    [(% %name %fun)
     (define-syntax %name
       (syntax-rules ()
	 [(%% %%exp (... ...))
	  (check %fun %%exp (... ...))]))]))

(define-syntax >>>
  (syntax-rules ()
    ((% %exp %str)
     (check-output-equiv string=? %exp %str))))

(define-syntax ==
  (syntax-rules ()
    [(% %exp ...)
     (check equal? %exp ...)]))

(define-syntax err
  (syntax-rules ()
    [(% %e)
     (check-if-error %e)]))

(define-syntax err-from
  (syntax-rules ()
    [(% %e %sym)
     (check-if-error '%sym %e)]))

;;; ------------------------------
;;; printing helpers

(define notify-bad-error
  (lambda (exp v)
    (when visible?
      (display "    ")
      (parameterize ([pretty-initial-indent 4])
	(pretty-print exp))
      (display " >> ")
      (display (error-message-from-safely v)))
    #f))

(define notify-bad-return
  (lambda (exp value)
    (when visible?
      (display "    ")
      (parameterize ([pretty-initial-indent 4])
	(pretty-print exp))
      (display " -> ")
      (parameterize ([pretty-initial-indent 4])
	(pretty-print value)))
    #f))

(define notify-bad-output
  (lambda (exp out)
    (when visible?
      (display "    ")
      (parameterize ([pretty-initial-indent 4])
	(pretty-print exp))
      (printf " >> ~s~n" out))
    #f))

;;; ------------------------------
;;; The pretty extension.

(define-syntax pretty-grade
  (let ([f (lambda (s)
	     (syntax-case s (==> >>> by error quote hint)
	       [(%exp ==> %val)
		(syntax (check equal? %exp '%val))]
	       [(%exp >>> (error))
		(syntax (check-if-error %exp))]
	       [(%exp >>> (error (quote %from)))
		(syntax (check-if-error '%from %exp))]
	       [(%exp >>> %str)
		(syntax (check-output-equiv equal? %exp %str))]

	       [(%exp ==> %val by %test)
		(syntax (check %test %exp '%val))]
	       [(%exp >>> %str by %test)
		(syntax (check-output-equiv %test %exp %str))]

	       [(%exp ==> %val hint %hint)
		(syntax (hint (check equal? %exp '%val) %hint))]
	       [(%exp ==> %val by %test hint %hint)
		(syntax (hint (check %test %exp '%val) %hint))]
	       [(%exp >>> (error) hint %hint)
		(syntax (hint (check-if-error %exp) %hint))]
	       [(%exp >>> (error (quote %from)) hint %hint)
		(syntax (hint (check-if-error '%from %exp) %hint))]

	       [(%exp >>> %str hint %hint)
		(syntax (hint (check-output-equiv equal? %exp %str) %hint))]
	       [(%exp >>> %str by %test hint %hint)
		(syntax (hint (check-output-equiv %test %exp %str) %hint))]))])
    (lambda (x)
      (syntax-case x ()
	[(% %c ...)
	 (with-syntax ([(%new-c ...) (map f (syntax (%c ...)))])
	   (syntax (and %new-c ...)))]))))

;;; ------------------------------
;;; safe evaluation

(define error-message-from-safely
  (lambda (v)
    (record-case v
      [error args (apply format-error args)]
      [warning (who . rest)
	(format "Warning~a: ~a.~n" 
	  (if who (format " in ~a" who) "")
	  (apply format rest))]
      [wrong-num-values args
	(format "You returned the wrong number of values: ~a~n"
	  (format-and-strip-parens args))]
      [interrupt ignored "There was a keyboard interrupt.~n"]
      [reset ignored "The procedure reset was called.~n"]
      [abort ignored "The procedure abort was called.~n"]
      [break ignored "The procedure break was called.~n"]
      [space-limit ignored
	(format "You ran out of memory, probably due to an infinite loop.~n")]
      [time-limit ignored
	(format "You ran out of time, probably due to an infinite loop.~n")]
      [else
	(error 'error-message-from-safely "This shouldn't happen: ~s~n" v)])))

;;; ------------------------------
;;; run-safely
;;; returns two values:
;;;   one of the following
;;;    (error sym f-string arg ...)
;;;    (warning sym f-string arg ...)
;;;    (x), where x is one of
;;;         interrupt, reset, abort, break, reset, space-limit, time-limit
;;;    (values v ...)
;;;   and a string, representing the output.

(define *ticks-used* 0)

(define run-safely
  (lambda (max-ticks max-bytes th)
    (let ([op (open-output-string)])
      (values
	(call/cc
	  (lambda (k)
	    (let ((make-recover
		    (lambda (engine-active? msg)
		      (let ((recover (if engine-active? engine-return k)))
			(lambda args
			  (set! *ticks-used* 0)
			  (recover (cons msg args)))))))
	      (parameterize
		  ([current-output-port op]
		   [error-handler   (make-recover #f 'error)]
		   [warning-handler (make-recover #t 'warning)]
		   [break-handler   (make-recover #t 'break)]
		   [reset-handler   (make-recover #t 'reset)]
		   [abort-handler   (make-recover #t 'abort)]
		   [keyboard-interrupt-handler (make-recover #f 'interrupt)]
		   [collect-request-handler
		     (let ((limit (+ (bytes-allocated) max-bytes))
			   (recover (make-recover #t 'space-limit)))
		       (lambda ()
			 ((if (> (bytes-allocated) limit)
			      recover
			      collect))))])
		((make-engine (lambda ()
				(call-with-values th
				  (lambda vals (cons 'values vals)))))
		 max-ticks
		 (lambda (remaining-ticks v)
		   (set! *ticks-used* (- max-ticks remaining-ticks))
		   v)
		 (make-recover #f 'time-limit))))))
	(get-output-string op)))))

(define run-safely-one
  (lambda (a b c)
    (call-with-values (lambda () (run-safely a b c))
      (lambda (v out)
	(record-case v
	  [values args
	    (if (or (null? args) (not (null? (cdr args))))
		(values (cons 'wrong-num-values args) out)
		(values v out))]
	  [else (values v out)])))))

(define format-error
  (lambda args
    (call/cc
      (lambda (k)
	(parameterize ([error-handler
			 (lambda ignored
			   (k (if (null? args)
				  (format "Error~n")
				  (format "Error: ~a~a.~n" (car args)
				    (apply string-append
				      (map-over (cdr args)
					(lambda (x) (format " ~s" x))))))))])
	  (let ([who (car args)]
		[msg (cadr args)]
		[args (cddr args)])
	    (format "Error~a: ~a.~n" 
	      (if who (format " in ~a" who) "")
	      (apply format msg args))))))))


;;; ------------------------------
;;; 

(define-syntax make-mat-checker
  (lambda (x)
    (syntax-case x ()
      ((% %filename)
       (string? (syntax-object->datum (syntax %filename)))
       (with-syntax ((%real-filename
		       (datum->syntax-object (syntax %)
			 (format "mats/~a.ms"
			   (syntax-object->datum (syntax %filename))))))
	 (syntax
	   (lambda ()
	     (include %real-filename))))))))
