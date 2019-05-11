(define (domain sokorobotto)
  (:requirements :typing)
  (:types shipment order location subject saleitem - object
  	  robot pallette - subject)
  (:predicates (ships ?s - shipment ?o - order)
            (orders ?o - order ?i - saleitem)
            (unstarted ?s - shipment)
            (packing-location ?p - location)
            (available ?p - location)
            (contains ?a - pallette ?i - saleitem)
            (free ?r - robot)
            (connected ?x - location ?y - location)
            (at ?b - subject ?l - location)
            (no-robot ?l - location)
            (no-pallette ?p - location)
            (includes ?s - shipment ?i - saleitem)
            (ready ?s - shipment)
            (atship ?i - saleitem ?s - shipment)
            (stillhaspatp ?l - location ?a - pallette)
            (aftercheckready ?s - shipment)
            
  )

  


  (:action take-pallette-to-next-location
             :parameters (?o - order ?i - saleitem ?l - location ?a - pallette ?r - robot ?b - location ?t - location)
             :precondition (and 
                            (packing-location ?l) (available ?l)
                            (not (at ?a ?l))
                            (at ?a ?b)
                            (no-robot ?t)
                            (no-pallette ?t)
                            ; (free ?r)
                            (at ?r ?b)
                            (orders ?o ?i)
                            (contains ?a ?i)
                            (connected ?b ?t)
                            )
             :effect (and (at ?r ?t)
                        ; (not (free ?r))
                        (at ?a ?t)
                        (not (no-pallette ?t))
                        (not (no-robot ?t))
                        (not (at ?a ?b))
                        (not (at ?r ?b))
                        (no-pallette ?b)
                        (no-robot ?b)
                        ))
                        
                        
                        
  (:action bring-pall-to-pack-through-path
              :parameters (?l - location ?a - pallette ?r - robot ?t - location ?n - location)
              :precondition (and (packing-location ?l) (available ?l)
                                (no-robot ?n)
                                (no-pallette ?n)
                                (not (at ?a ?l))
                                (at ?a ?t)
                                ; (not (free ?r))
                                (at ?r ?t)
                                (not (connected ?t ?l))
                                (connected ?t ?n)
                                )
                                
              :effect (and 
                            ; (not (free ?r))
                            (at ?a ?n)
                            (at ?r ?n)
                            (not (at ?a ?t))
                            (not (at ?r ?t))
                            (no-pallette ?t)
                            (no-robot ?t)
                            (not (no-pallette ?n))
                            (not (no-robot ?n))
                        ))
  
  (:action bring-pall-to-pack-directly
              :parameters (?l - location ?a - pallette ?r - robot ?t - location)
              :precondition (and (packing-location ?l) (available ?l)
                                (no-pallette ?l)
                                (no-robot ?l)
                                (not (at ?a ?l))
                                (at ?a ?t)
                                ; (not (free ?r))
                                (at ?r ?t)
                                (connected ?t ?l)
                                )

              :effect (and  
                            ; (free ?r)
                            (at ?a ?l)
                            (at ?r ?l)
                            (not (at ?a ?t))
                            (not (at ?r ?t))
                            (no-pallette ?t)
                            (no-robot ?t)
                            (not (no-pallette ?l))
                            (not (no-robot ?l)))
                        )
 
             
             
  (:action atpack
             :parameters (?s - shipment ?o - order ?i - saleitem ?l - location ?a - pallette ?r - robot)
             :precondition (and (packing-location ?l) 
                            ; (available ?l)
                            (at ?a ?l) 
                            (at ?r ?l)
                            ; (free ?r)
                            (contains ?a ?i)
                            (orders ?o ?i)
                            (unstarted ?s)
                            (ships ?s ?o)
                            )
             :effect (and (ready ?s)
                        (not (contains ?a ?i))
                        (atship ?i ?s))
                    )
             
  (:action check-ready
             :parameters (?s - shipment ?o - order ?i1 - saleitem ?i2 - saleitem ?a - pallette)
             :precondition (and 
                            (atship ?i1 ?s)
                            (ready ?s)
                            (orders ?o ?i1)
                            (ships ?s ?o)
                            (orders ?o ?i2)
                            (or (contains ?a ?i2) (not (atship ?i2 ?s))))
             :effect (and (not (ready ?s))
                        (aftercheckready ?s)))
             
  (:action if-still-has-p-forthisship
             :parameters (?l - location ?s - shipment ?o - order ?i1 - saleitem ?i2 - saleitem ?a - pallette ?)
             :precondition (and (packing-location ?l)
                                (at ?a ?l)
                                (atship ?i1 ?s)
                                (ships ?s ?o)
                                (orders ?o ?i2)
                                (contains ?a ?i2))
             :effect (stillhaspatp ?l ?a))
             
  (:action if-no-need-pall
             :parameters (?s - shipment ?o - order ?i - saleitem ?l - location ?a - pallette ?t - location ?r - robot)
             :precondition (and 
                                ; (aftercheckready ?s)
                                (packing-location ?l)
                                (not (stillhaspatp ?l ?a))
                                ; (not (contains ?a ?i))
                                ; (atship ?i ?s)
                                (at ?a ?l)
                                (connected ?l ?t)
                                (no-robot ?t)
                                (at ?r ?l)
                                (no-pallette ?t)
                                )
             :effect (and (at ?a ?t)
                        (at ?r ?t)
                        (not (no-pallette ?t))
                        (not (no-robot ?t))
                        (no-pallette ?l)
                        (no-robot ?l)
                        (not (at ?a ?l))
                        (not (at ?r ?l))
                        ))
                        
  (:action move-far-if-need
             :parameters (?a - pallette ?now - location ?target - location ?r - robot)
             :precondition (and 
                                (not (packing-location ?target))
                                (not (packing-location ?now))
                                (connected ?now ?target)
                                (at ?a ?now)
                                (at ?r ?now)
                                (no-pallette ?target)
                                (no-robot ?target)
                                )
             :effect (and (at ?a ?target)
                        (at ?r ?target)
                        (not (at ?a ?now))
                        (not (at ?r ?now))
                        (no-pallette ?now)
                        (no-robot ?now)
                        (not (no-pallette ?target))
                        (not (no-robot ?target))
                        )
                                )
                                
  (:action move-robot-if-need
             :parameters (?a - pallette ?now - location ?target - location ?r - robot)
             :precondition (and 
                                (connected ?now ?target)
                                (at ?a ?now)
                                (at ?r ?now)
                                (no-robot ?target)
                                )
             :effect (and (at ?a ?target)
                        (at ?r ?target)
                        (not (at ?a ?now))
                        (not (at ?r ?now))
                        (no-robot ?now)
                        (not (no-robot ?target))
                        )
                                )
             
             
  (:action readyship
             :parameters (?s - shipment ?o - order ?i - saleitem ?l - location)
             :precondition (and (ready ?s)
                            (packing-location ?l) ; how to check this is the packing location you want
                            ; (available ?l)
                            (atship ?i ?s))
             :effect (and (includes ?s ?i)
                        (not (unstarted ?s))
                        (not (atship ?i ?s))))
                        ; (available ?l)))
  
  

  
)