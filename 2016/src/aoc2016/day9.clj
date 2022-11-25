(ns aoc2016.day9
 (:require [clojure.string :as str]))
 (use '[clojure.test :only [is]])

(defn marker-replace [s]
  "Generate a string by consuming markers and recursing"
  (loop [remaining-string s
         so-far ""]
   ; make it a cond
   (if (empty? remaining-string)
    so-far
    ; if it doesn't start with (
      ; consume everything up to ( and recurse
    ; if it starts with a (
      ; consume everything to ), replace it, and recurse
    )
  
)

(defn main
  "https://adventofcode.com/2016/day/9
      lein run day9"
  [& args]
  (def s (slurp "src/aoc2016/input9.txt"))
  (def lines (map str/trim (str/split s #"\n")))

)



