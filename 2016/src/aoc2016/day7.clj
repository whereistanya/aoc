(ns aoc2016.day7
 (:require [clojure.string :as str]))
 (use '[clojure.test :only [is]])

(defn check-has-abba [s]
  "Check if a string contains an abba sequence"
  (some true? (for [i (range (- (count s) 3))]
          (and
            (= (get s i) (get s (+ i 3)))
            (= (get s (+ i 1)) (get s (+ i 2)))
            (not(= (get s (+ i 2)) (get s (+ i 3))))
          )))
)

(defn check [s]
  "separate out pieces of a string and evaluate them"
  (let [groups (re-seq #"\[\w+\]" s)] ; everything in []s
    (if (some true? (for [g groups] (check-has-abba g)))
      false  ; an enclosed group matches so the pattern fails
      ; else
      (if (check-has-abba s)
        true ; the whole group succeeds
        false ; the whole group fails
      )))
  )

(defn main
  "https://adventofcode.com/2016/day/7
      lein run day7"
  [& args]
   (def s (slurp "src/aoc2016/input7.txt"))
   ; tests
   (is (true? (check "abba")))
   (is (false? (check "abcd[bddb]xyyx")))
   (is (true? (check "abbxyyxa")))
   (is (false? (check "abxyxa")))
   (is (true? (check "ioxxoj[asdfgh]zxcvbn")))
   (is (false? (check "aaaa[qwer]tyui")))
   (println "Tests passed")

  (def lines (map str/trim (str/split s #"\n")))
  (println "Part A" (count(remove false? (map check lines))))

)



