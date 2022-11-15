(ns aoc2016.day2
 (:require [clojure.string :as str]))

(defn move
  "Find the next button"
  [startx starty line]
  ; 1 2 3     ; e.g., 1 0 is 2
  ; 4 5 6     ; and   0 2 is 7
  ; 7 8 9

  (let [grid [[1 2 3][4 5 6][7 8 9]]]
    (nth (nth grid starty) startx)))

(defn main
  "https://adventofcode.com/2016/day/2
      lein run day2"
  [& args]
   (def s (slurp "src/aoc2016/input2.txt"))
   (let [procedure (str/split s #"\n")]
    (println (move 1 0 ""))

    ))
