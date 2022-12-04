(ns aoc2022.day2
  (:require [clojure.string :as str]))

(def move-name { 0 :rock 1 :paper 2 :scissors})

; score is for player 2
; (1 for Rock, 2 for Paper, and 3 for Scissors)
; +
; 0 if you lost, 3 if the round was a draw, and 6 if you won)
(def scores { [:rock :rock]         4
              [:rock :paper]        8
              [:rock :scissors]     3
              [:paper :rock]        1
              [:paper :paper]       5
              [:paper :scissors]    9
              [:scissors :rock]     7
              [:scissors :paper]    2
              [:scissors :scissors] 6})

(defn find-move [[p1 req]]
  "Return the name of p1's move and whatever p2 should do"
  (let [p1move (- (int (first p1)) 65)
        p1-move-name (get move-name p1move)]
    (cond
      (= req "X") ; need to lose
        [p1-move-name (get move-name (mod (dec p1move) 3))]
      (= req "Y") ; need to draw
        [p1-move-name p1-move-name]
      (= req "Z") ; need to win
        [p1-move-name (get move-name (mod (inc p1move) 3))]
    )
  )
)

(defn oh-man-this-is-a-hack [i]
  "Hack for scores using XYZ instead of ABC; convert to ABC"
  (if (> i 3) (- i 23) i))

(defn convert-to-move-names [s]
  "Change a string like 'A X' into ':rock :rock'"
  ( ->> (str/split s #" ") ; from "A X" to (A X)
        (map first) ; convert one char string to char
        (map int)
        (map #(- % 65 )) ; convert to 0, 1 or 2
        (map oh-man-this-is-a-hack) ; TODO: how to do this inline?
        (map #(get move-name %))))

(defn part1 [s]
  "Parse the whole input, do stuff"
  ( ->> (str/split s #"\n")
        (map str/trim)
        (map convert-to-move-names)
        (map scores)
        (apply +)))

(defn split-to-vector [s] ( ->> (str/split s #" ")))

(defn part2 [s]
  "Parse the whole input, do stuff"
  ( ->> (str/split s #"\n")
        (map str/trim)
        (map #(str/split % #" "))
        (map find-move)
        (map scores)
        (apply +)))

(defn main
  [& args]

  (let [s (slurp "src/aoc2022/input2.txt")
        part1-score (part1 s)
        part2-score (part2 s)
        ]
   (println "Part 1" part1-score)
   (println "Part 2" part2-score)
   )
)
