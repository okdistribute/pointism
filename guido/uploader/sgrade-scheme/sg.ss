#!/l/ChezScheme-7.4d/bin/scheme --script

;;; first line was: #! /usr/bin/scheme --script

;;; sgrade.ss

;;; contains code to handle the automatic evaluation (via some test script)
;;; of scheme code.

;;; This is insane in meta-ness.

(optimize-level 2)
(suppress-greeting #t)


(define main
  (lambda (aname)
    (define sgrade-tics  5000000)
    (define sgrade-bytes 50000000)
    (define visible? #t)
    (define string-downcase
      (lambda (s)
        (list->string (map-over (string->list s) char-downcase))))
    (let ()
      (include "sgrade-scheme/disarm.ss")
      (include "sgrade-scheme/syntax.ss")
      (include "sgrade-scheme/mat.ss")  ; ick... i'm including this twice!
      (let ((pre (format "mats/~a.pre" aname)))
        (when (file-exists? pre)
          (parameterize ((optimize-level 0))
            (load pre))))
      (let* ((mat-checker
               (eval
                 `(lambda (sgrade-tics sgrade-bytes visible?)
                    (include "sgrade-scheme/syntax.ss")
                    (include "sgrade-scheme/mat.ss")
                    (include ,(format "mats/~a.ms" aname))
                    (values mat-score mat-total))))
             (inexps
               (parameterize ((error-handler
                                (lambda (who what . args)
                                  (printf "Error reading submission:~n")
                                  (apply printf what args)
                                  (newline)
                                  (exit 1))))
                 (let f ((x (read)))
                   (if (eof-object? x) 
                       '()
                       (cons x (f (read))))))))
        (disarm)
        (mv-let ([(v out)
                  (parameterize ((optimize-level 0))
                    (run-safely (* 100 sgrade-tics) sgrade-bytes
                      (lambda ()
                        (for-each eval inexps))))])
          (record-case v
            [values ignore
              ;; the submission successfully loaded
              (let ([op (open-output-string)])
                (mv-let (((mat-score mat-total)
                          (parameterize ([current-output-port op]
                                         [optimize-level 0])
                            (mat-checker (* 100 sgrade-tics) sgrade-bytes
                              visible?))))
                  (display (get-output-string op))
                  (newline op)))]
            [else
              ;; the submission didn't load, so we tell the student this.
              (printf "Error while loading assignment:~n~a"
                (error-message-from-safely v))]))
        (exit)))))

(unless (= (length (command-line)) 2)
  (printf "usage: ~a assignment-name < assignment" (car (command-line)))
  (exit 1))

(main (cadr (command-line)))
