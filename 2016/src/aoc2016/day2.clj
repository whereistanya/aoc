(ns aoc2016.day2
 (:require [clojure.string :as str]))

(defn move
  "follow one instruction to move one step"
  [startx starty instruction]
  ;(println "move" startx starty instruction)

  (cond
   (= instruction \L)
    [(max 0 (- startx 1)) starty]
   (= instruction \R)
    [(min 2 (+ startx 1)) starty]
   (= instruction \U)
    [startx (max 0 (- starty 1))]
   (= instruction \D)
    [startx (min 2 (+ starty 1))]
    :else
    [-99 -99]
   ))

(defn grid-at
  "Return the number at the grid position"
  [x y]
  ;(println "grid-at" x y)
  (let [grid [[1 2 3]
              [4 5 6]
              [7 8 9]]]
   (nth (nth grid y) x)))



(defn move-line
  "Find the next button"
  [line startx starty]

  (loop [remaining-line line
         x startx
         y starty]
    ;(println remaining-line x y)
    (if (empty? remaining-line)
      [(grid-at x y) x y]
      ; else...
      (let [[instruction & remaining] remaining-line
            pos (move x y instruction)]
        (recur remaining (first pos) (second pos))))))

(defn generate-code
  "Work through all procedure lines"
  [procedure startx starty]
  (loop [remaining-lines procedure
         x startx
         y starty
         code []]
   (if (empty? remaining-lines)
    code
    (let [[line & remaining] remaining-lines
          moved-to (move-line line x y)
          digit (first moved-to)
          x (second moved-to)
          y (last moved-to)]
     (recur remaining
            x
            y
            (conj code digit))))))

(defn main
  "https://adventofcode.com/2016/day/2
      lein run day2"
  [& args]
   (def s (slurp "src/aoc2016/input2.txt"))
   (let [procedure (str/split s #"\n")
         startx 5
         starty 5]
    (println "PartA" (generate-code procedure startx starty))))
