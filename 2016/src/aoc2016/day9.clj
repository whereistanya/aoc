(ns aoc2016.day9
 (:require [clojure.string :as str]))
 (use '[clojure.test :only [is]])

(defn unpack [s]
  (println s)
  ; TODO This could unpack the whole string, not just the ()s
  (let [groups (re-matches #"^(\w+)x(\d+)$" s)]
    (println "groups" groups)
    (drop 1 groups)))


(defn process [s]
  "remove the next piece of string and act on it"
  (if (= (first s) \()
    (let [end (str/index-of s \))
          [how-many how-much] (unpack (subs s 1 end))
           how-many (Integer/parseInt how-many)
           how-much (Integer/parseInt how-much)
           end2 (+ end how-many) ; how many characters
           to-add (apply str (repeat how-much (subs s (inc end) (inc end2))))
           remaining (subs s (+ end2 1))
          ]
          (println "how-many" how-many)
          (println "how-much" how-much)
          (println "end" end)
          (println "end2" end2)
         [remaining to-add]
          )))

(defn marker-replace [s]
  "Generate a string by consuming markers and recursing"
  (loop [remaining-string s
         so-far ""]
   (if (empty? remaining-string)
    so-far
    (let [[remaining-string to-add] (process remaining-string)
          ]
    (recur remaining-string to-add)
    )
  )
))

(defn main
  "https://adventofcode.com/2016/day/9
      lein run day9"
  [& args]
  (def s (slurp "src/aoc2016/test9.txt"))
  (def lines (map str/trim (str/split s #"\n")))

  (println (process "(3x3)XYZ"))

)



