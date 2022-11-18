(ns aoc2016.day3
 (:require [clojure.string :as str]))


(defn make-ints
  "Turn a string into a vector of ints"
  [s]
  (map #(Integer/parseInt %) (str/split s #"\s+")))

(defn main
  "https://adventofcode.com/2016/day/3
      lein run day3"
  [& args]
   (def s (slurp "src/aoc2016/input3.txt"))
   (let [triangles (map make-ints (map str/trim (str/split s #"\n")))]

    (def valid
      (for [tri triangles
        :let [stri (sort tri)
              x (> (+ (first stri) (second stri)) (nth stri 2))]
        :when (true? x)] tri))

      (println "PartA" (count valid) "of" (count triangles) "are valid")

      ; make a vector of the first, then second, then third column, and split
      ; into groups of three
      (let [columns (partition 3 (concat (map #(first %) triangles)
                                         (map #(second %) triangles)
                                         (map #(nth % 2) triangles)))]
        (def valid
          (for [tri columns
            :let [stri (sort tri)
                  x (> (+ (first stri) (second stri)) (nth stri 2))]
            :when (true? x)] tri)))
      (println "PartB" (count valid) "of" (count triangles) "are valid")
      ))


