;;; syntax.ss

;; A fine place to put random macros that are used in the grader.

(define-syntax letcc
  (syntax-rules ()
    ((% %v %e %es ...)
     (call/cc (lambda (%v) %e %es ...)))))

(define-syntax map-over
  (syntax-rules ()
    ((% %ls %f)
     (map %f %ls))))

(define-syntax foreach
  (syntax-rules ()
    ((% %ls %f)
     (for-each %f %ls))))

(define-syntax mv-let
  (syntax-rules ()
    [(% () %b0 %b ...)
     (begin %b0 %b ...)]
    [(% ([%f %e] %d ...) %b0 %b ...)
     (mv-let (%d ...)
       (call-with-values (lambda () %e)
	 (lambda %f %b0 %b ...)))]))

(define-syntax displayln
  (syntax-rules ()
    [(% %x ...)
     (begin (display %x) ... (newline))]))

