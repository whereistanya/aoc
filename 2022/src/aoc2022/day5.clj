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
                how-many (Integer/parseInt (second groups))
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

(defn process-moves
  "Apply each move one at a time"
  [stacks moves part]
  (loop [stacks stacks
         moves moves
         part part]
    (let [[line & remaining-moves] moves
          move (parse-move line)
          real-from (real-index (get move :from))
          real-to (real-index (get move :to))
          how-many (get move :how-many)
          after-removal (subvec (get stacks real-from) how-many)
          to-add-p1 (vec (reverse (take how-many (get stacks real-from))))
          to-add-p2 (vec (take how-many (get stacks real-from)))
          to-add (if (= part :part1) to-add-p1 to-add-p2)
          after-add (into to-add (get stacks real-to))
          next-stacks (into stacks
                        { real-from after-removal
                          real-to after-add })
          ]
    (if (empty? remaining-moves)
      next-stacks
      (recur next-stacks remaining-moves part)
      )
    )
  )
)

(defn move-crates [stacks moves part]
  "Move crates around."
  (let [
    indexes
      (for [line stacks
           :let [found (get-indexes line)] ]
           found )
     columns (apply merge-with into indexes)
     final-stacks (process-moves columns moves part)
     ]
     (apply str (map first (vals(sort final-stacks))))
  )
)

(defn parse [s]
  "Split into lines, trim the lines"
  ( ->> (str/split s #"\n")
        ))


(defn main
  [& args]

  (let [s (slurp "src/aoc2022/input5.txt")
         [stacks moves] (map parse (str/split s #"\n\n"))
         part1-result (move-crates stacks moves :part1)
         part2-result (move-crates stacks moves :part2)
        ]

    (doseq [line stacks]
      (println "=:" line))
    (println "Part 1" part1-result)
    (println "Part 2" part2-result)
  )
)
