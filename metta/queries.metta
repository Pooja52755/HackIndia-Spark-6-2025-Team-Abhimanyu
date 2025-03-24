; Base queries
(= (getHumans) (match &self (Inheritance $name human) $name))
(= (getMen ) (match &self (Inheritance  man) $name))
(= (getWomen ) (match &self (Inheritance $name woman) $name))
(= (getUgly ) (match &self (Inheritance $name ugly) $name))
(= (getSodaDrinkers) (match &self (Inheritance $name sodaDrinker) $name))

; Combined queries
(= (getUglyMen )
   (match &self 
    (, (Inheritance $name man)
             (Inheritance $name ugly)) $name))

(= (getUglyWomen)
   (match &self
   (, (Inheritance $name woman)
         (Inheritance $name ugly)) $name))

(= (getSodaDrinkingMen)
   (match &self
    (, (Inheritance $name man)
          (Inheritance $name sodaDrinker) ) $name))

(= (getSodaDrinkingWomen)
   (match &self
    (, (Inheritance $name woman)
           (Inheritance $name sodaDrinker)) $name))