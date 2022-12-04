(ns aoc2022.day4
  (:require [clojure.string :as str]))
  (use '[clojure.test :only [is]])

(defn fully-contains [[x y]]
  ;[x1 x2] [y1 y2]]
  "Accept two ranges like [x1 x2] [y1 y2]. Return true if x fully contains y or
  vice versa, false otherwise."
  (let [x1 (first x)
        x2 (second x)
        y1 (first y)
        y2 (second y)]
  (cond
    (and (<= x1 y1) (>= x2 y2)) true
    (and (<= y1 x1) (>= y2 x2)) true
   :else false)))

(defn partially-contains [[x y]]
  "Accept two ranges like [x1 x2] [y1 y2]. Return true if they overlap."
  (let [x1 (first x)
        x2 (second x)
        y1 (first y)
        y2 (second y)]
  (cond
    (and (<= x1 y1) (>= x2 y1)) true
    (and (<= x1 y2) (>= x2 y2)) true
    (and (<= y1 x1) (>= y2 x1)) true
    (and (<= y1 x2) (>= y2 x2)) true
   :else false)))

(defn parse-ranges
  "split by dashes and turn numbers to ints"
  [s]
  ( ->> (str/split s #"-")
        (map #(Integer/parseInt %))
   ))


(defn check-range-overlaps [s overlap-function]
  "Parse the whole input, split into a vector of strings, parse out the
  ranges, apply whatever function was passed in, return how many are true/false"
  ( ->> (str/split s #"\n")
        (map str/trim)
        (map #(str/split % #","))
        (map #(map parse-ranges %))
        (map #(overlap-function %))
        frequencies
  )
)

(defn main
  [& args]

  ; TODO: move line parsing to here
  (let [ f "src/aoc2022/input4.txt"
        ;f "src/aoc2022/test4.txt"
        s (slurp f)
        part1-result (check-range-overlaps s fully-contains)
        part2-result (check-range-overlaps s partially-contains)
        ]

   (println "Part 1" part1-result)
   (println "Part 2" part2-result)
))
