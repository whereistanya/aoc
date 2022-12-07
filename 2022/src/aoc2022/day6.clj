(ns aoc2022.day6
  (:require [clojure.string :as str]))
  (use '[clojure.test :only [is]])

(defn part1 [s]
  "Parse the whole input, split into a vector of strings, do stuff"
  ( ->> (str/split s #"\n")
        (map str/trim)
  )
)

(defn part2 [s]
  "TODO"
  ( ->> (str/split s #"\n")
        (map str/trim)
  )
)

(defn main
  [& args]

  (let [s (slurp "src/aoc2022/input6.txt")
        part1-result (part1 s)
        part2-result (part2 s)
        ]

   (println "Part 1" part1-result)
   (println "Part 2" part2-result)
))
