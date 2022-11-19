(ns aoc2016.day4
 (:require [clojure.string :as str]))
 (use '[clojure.test :only [is]])

(defn checksum [s]
  "Return the checksum for a string"
  ( ->> s
        frequencies
        (sort-by key)
        (sort-by val >)
        (take 5)
        (map first)
        (apply str)
        )
)

(defn rotate [s n]
  "Advance the characters in s n times"
  ( ->> s
        seq
        (map int)
        (map #(- % 97))
        (map #(+ (mod n 26) %))
        (map #(mod % 26))
        (map #(+ 97 %))
        (map char)
        (apply str)
  )
)

(defn check-valid
  "Check if a room name matches its checksum"
  [s]
  ; aaaaa-bbb-z-y-x-123[abxyz]
  (let [groups (re-matches #"^([a-z-]+)(\d+)\[(\w+)\]" s)
        room-name (second groups)
        id (Integer/parseInt (nth groups 2))
        given-checksum (nth groups 3)
        actual-checksum (checksum (re-seq #"[a-z]" room-name))
        decrypted (str/join " " (map #(rotate % id) (str/split room-name #"-")))
        ]
    (if (str/includes? decrypted "north") (do (println "Part B" decrypted "in room" id)))
    (if(= given-checksum actual-checksum) id 0)
   )
)

(defn main
  "https://adventofcode.com/2016/day/4
      lein run day4"
  [& args]
   (def s (slurp "src/aoc2016/input4.txt"))
   ; tests
   (is (= 987 (check-valid "a-b-c-d-e-f-g-h-987[abcde]")))
   (is (= 404 (check-valid "not-a-real-room-404[oarel]")))
   (is (= 0 (check-valid "totally-real-room-200[decoy]")))

   (println "Part A" (apply + (map check-valid (str/split s #"\n"))))

 )


