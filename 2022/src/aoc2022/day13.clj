(ns aoc2022.day13
  (:require [clojure.string :as str]))
  (use '[clojure.test :only [is]])

(defn consume-list
  "Remove a list from the start of a string. May contain sub-lists. Return the
  list and the remainder."
  [s]
  (println "parsing" s)
  ; assumes the string starts with "["
  (if (not= (first s) \[)
    (throw (Exception. "unexpected format")))
  (let [stack [ \]]  ; opening [ character
       ]
    (println "it has" (count s) " chars")
    (dotimes [i (dec(count s))]

      ; https://commandercoriander.net/blog/2015/01/17/testing-for-balanced-brackets-in-clojure/

      (println (inc i) (nth s (inc i)) stack)
        ; else
          (cond
            (= (nth s i) \[)
              (println "open")
              (conj stack (nth s i))
            (= (nth s i) \])
              (println "close")
              (pop stack)
          )
      (if empty? stack)
        [(subs s 0 i)] ; (subs s i)]
    ) ; dotimes

  ); let
)

(defn do-something
  "TODO"
  [[s1 s2]]
  (println "$------")
  (println (first s1))
  (println s2)
  (println "-------")

  (println "got" (consume-list s1))


)

(defn part1 [s]
  "Parse the whole input, split into a vector of strings, do stuff"
  ( ->> (str/split s #"\n\n")
        (map #(str/split % #"\n"))
        ; now we have pairs of strings
        (map #(do-something %))
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

  (let [s (slurp "src/aoc2022/test13.txt")
        ;part1-result (part1 s)
        ;part2-result (part2 s)
        ]

  (consume-list "[a[b]]")
  ; (println "Part 1" part1-result)
  ; (println "Part 2" part2-result)
))
