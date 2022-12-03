(ns aoc2022.day1
  (:require [clojure.string :as str]))

(defn sum-int-strings [v]
  "Sum a vector of numbers in string form"
  ( ->> v
        (map #(Integer/parseInt %))
        (apply +)
  ))

(defn aggregate [s]
  "Parse the whole input, split into calories per-elf, sum, sort"
  ( ->> (str/split s #"\n\n")
        (map str/trim)
        (map #(str/split % #"\n"))
        (map #(sum-int-strings %))
        sort
        reverse
  )
)

(defn main
  [& args]

  (let [s (slurp "src/aoc2022/input1.txt")
        carried (aggregate s)]

   (println "Part 1" (apply str (take 1 carried)))
   (println "Part 2" (apply + (take 3 carried))))
)
