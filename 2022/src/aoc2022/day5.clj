(ns aoc2022.day5
  (:require [clojure.string :as str]))
  (use '[clojure.test :only [is]])



(defn get-indexes [line]
  (let [m (map-indexed vector line)
        only-chars (filter #(Character/isUpperCase (second %)) m)
        kv (into {} (for [x only-chars] [(first x) [(second x)]]))
        ]
        kv
    )
  )

(defn parse-move [s]
  (let [groups (re-matches #"move (\d+) from (\d+) to (\d+)" s)
                how-many (second groups)
                move-from (Integer/parseInt (nth groups 2))
                move-to (Integer/parseInt (nth groups 3))]
    { :how-many how-many :from move-from :to move-to}
  )
)

(defn real-index [i]
  ; 1 => 1, 2 => 5, 3 => 9, 4 => 13
  ; 1 + ((i - 1) * 4)
  (inc (* 4 (- i 1)))
)

(defn part1 [stacks moves]
  "TODO"
  (doseq [line stacks]
    (println "LINE:" line))
  ;(get-indexes (first stacks))
  (let [
    indexes
      (for [line stacks
           :let [found (get-indexes line)] ]
           found )
     columns (apply merge-with into indexes)
   ]

    (doseq [line columns]
      (println "MUNGED:" line))
    ;(println (str/index-of keyline \3))
  (doseq [line moves]
    (let [move (parse-move line)
          real-from (real-index (get move :from))
          real-to (real-index (get move :to))
          how-much (get move :how-many)
          ]
      (println line)
      (println move "=>" how-much real-from real-to)

    )
   )
  )
)

(defn part2 [s]
  "TODO"
  ( ->> (str/split s #"\n")
        (map str/trim)
  )
)

(defn parse [s]
  "Split into lines, trim the lines"
  ( ->> (str/split s #"\n")
        ))


(defn main
  [& args]

  (let [s (slurp "src/aoc2022/test5.txt")
         [stacks moves] (map parse (str/split s #"\n\n"))
         part1-result (part1 stacks moves)
   ;     part2-result (part2 s)
        ]

   (println "Part 1" part1-result)
   ;(println "Part 2" part2-result)
   ;(println stacks)
   ;(println)
   ;(println (first moves))

   )
)
