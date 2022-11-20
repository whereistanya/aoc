(ns aoc2016.day6
 (:require [clojure.string :as str]))
 (use '[clojure.test :only [is]])


(defn most-freq [v]
  "Return the checksum for a string"
  (for [i (range 8)]
    ; change the "val >" to "val" for part b
    (first (sort-by val > (frequencies (map #(nth % i) v))
    )))
)

(defn main [&args]
  "https://adventofcode.com/2016/day/6
      lein run day6"
   (def s (slurp "src/aoc2016/input6.txt"))

   (println "Part A" (apply str(keys(most-freq (str/split s #"\n")))))

 )


