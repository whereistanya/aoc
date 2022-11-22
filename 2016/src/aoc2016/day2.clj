(ns aoc2016.day2
 (:require [clojure.string :as str]))



(defn grid-at
  "Return the number at the grid position"
  [part x y]
  (println "grid-at" part x y)
  (let [grida [[1 2 3]
               [4 5 6]
               [7 8 9]]

        gridb [[nil nil \1  nil nil]
               [nil \2   \3  \4   nil]
               [\5   \6   \7  \8     \9]
               [nil \A   \B  \C   nil]
               [nil nil \D  nil nil]]
        grid (if (= part :parta) grida gridb)
        val (get (get grid y) x)]
        val
        ))



(defn move-parta
  "Use the part a keypad"
  [startx starty instruction]
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

(defn move-partb
  "Use the part b keypad"
  [startx starty instruction]
   (cond
    (= instruction \L)
     (if (grid-at :partb (- startx 1) starty)
      [(- startx 1) starty]
      [startx starty])
    (= instruction \R)
     (if (grid-at :partb (+ startx 1) starty)
      [(+ startx 1) starty]
      [startx starty])
    (= instruction \U)
     (if (grid-at :partb startx (- starty 1))
      [startx (- starty 1)]
      [startx starty])
    (= instruction \D)
     (if (grid-at :partb startx (+ starty 1))
      [startx (+ starty 1)]
      [startx starty])
    :else
      [-99 -99]))


(defn move
  "follow one instruction to move one step"
  [part startx starty instruction]
  ;(println "move" startx starty instruction)
  (if (= part :parta) (move-parta startx starty instruction)
                      (move-partb startx starty instruction)))


(defn move-line
  "Find the next button"
  [part line startx starty]

  (loop [remaining-line line
         x startx
         y starty]
    ;(println remaining-line x y)
    (if (empty? remaining-line)
      [(grid-at part x y) x y]
      ; else...
      (let [[instruction & remaining] remaining-line
            pos (move part x y instruction)]
        (recur remaining (first pos) (second pos))))))

(defn generate-code
  "Work through all procedure lines"
  [part procedure startx starty]
  (loop [remaining-lines procedure
         x startx
         y starty
         code []]
   (if (empty? remaining-lines)
    code
    (let [[line & remaining] remaining-lines
          moved-to (move-line part line x y)
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
   (def s (slurp "src/aoc2016/test2.txt"))
   (let [procedure (str/split s #"\n")
         startx 5
         starty 5]
    (println "PartA" (generate-code :parta procedure startx starty))
    (println "PartB" (generate-code :partb procedure startx starty))))
