(ns aoc2016.day7
 (:require [clojure.string :as str]))
 (use '[clojure.test :only [is]])

(defn check-has-abba [s]
  "Check if a string contains an abba sequence"
  (some true? (for [i (range (- (count s) 3))]
          (and
            (= (get s i) (get s (+ i 3)))
            (= (get s (+ i 1)) (get s (+ i 2)))
            (not(= (get s (+ i 2)) (get s (+ i 3))))
          )))
)

(defn get-abas [s]
  "Return all aba sequences"
  (for [i (range (- (count s) 1))
    :when (and
            (= (get s i) (get s (+ i 2)))
            (not(= (get s i) (get s (+ i 1)))))
            ]
    (subs s i (+ i 3))))

(defn part-a [s]
  "Separate out pieces of a string and evaluate them"
  (let [groups (re-seq #"\[\w+\]" s)] ; everything in []s
    (if (some true? (for [g groups] (check-has-abba g)))
      false  ; an enclosed group matches so the pattern fails
      ; else
      (if (check-has-abba s)
        true ; the whole group succeeds
        false ; the whole group fails
      )))
  )
(defn remove-from-string [s x]
   (clojure.string/replace s x "--"))


(defn part-b [s]
  "Separate out pieces of a string and evaluate them"
  (let [groups (re-seq #"\[\w+\]" s)
        remainder (reduce #(remove-from-string %1 %2) s groups)
        abas (get-abas remainder)]
    ; for each aba, look for a bab in any group
    ;(println (for [aba abas
    ;           :let [bab (str (subs aba 1 3) (second aba))]]
    ;           (some #(str/includes? % bab) groups)))
    (if (some true? (for [aba abas
                     :let [bab (str (subs aba 1 3) (second aba))]]
                     (some #(str/includes? % bab) groups)))
        true
        false
    )
  )
)

(defn main
  "https://adventofcode.com/2016/day/7
      lein run day7"
  [& args]
  (def s (slurp "src/aoc2016/input7.txt"))
  (def lines (map str/trim (str/split s #"\n")))

  (is (true? (part-a "abba")))
  (is (false? (part-a "abcd[bddb]xyyx")))
  (is (true? (part-a "abbxyyxa")))
  (is (false? (part-a "abxyxa")))
  (is (true? (part-a "ioxxoj[asdfgh]zxcvbn")))
  (is (false? (part-a "aaaa[qwer]tyui")))
  (println "Part A tests passed")
  (println "Part A" (count(remove false? (map part-a lines))))

  (is (= (get-abas "abcbdb") ["bcb" "bdb"]))
  (is (= (get-abas "aababcb") ["aba" "bab" "bcb"]))
  (is (= (get-abas "ababcdcac") ["aba" "bab" "cdc" "cac"]))
  (is (= (true? (part-b "aba[bab]xyz"))))
  (is (= (false? (part-b "xyx[xyx]xyx"))))
  (is (= (true? (part-b "aaa[kek]eke"))))
  (is (= (true? (part-b "zazbz[bzb]cdb"))))
  (println "Part B tests passed")
  (println "Part B" (count(remove false? (map part-b lines))))
)



