(ns aoc2016.day5
  (:require [clojure.string :as str]))

(defn md5 [s]
    (let [algo (java.security.MessageDigest/getInstance "MD5")
          raw (.digest algo (.getBytes s))]
        (format "%032x" (BigInteger. 1 raw))))


(defn pw [s]
  "Churn through md5s to generate matching hashes"
  (loop [i 0
         pw-so-far ""]
         (if (not (nil? (get pw-so-far 7)))
          pw-so-far ; long enough
           (let [md5sum (md5 (str s i))
                 pw-add (if (= (subs md5sum 0 5) "00000") (subs md5sum 5 6) nil)]
           (let [next-pw (if (not (nil? pw-add)) (str pw-so-far pw-add) pw-so-far)]
           (if (not (nil? pw-add)) (println i next-pw))
           (recur (inc i) next-pw)
           )))))

(defn pw2 [s]
  "Churn through md5s to generate matching hashes"
  (loop [i 0
         pw-so-far [0 0 0 0 0 0 0 0]
         found (set [])]
    (let [md5sum (md5 (str s i))
          change (if (= (subs md5sum 0 5) "00000") (subs md5sum 5 7) nil)
          pos (if (and (not (nil? change)) (re-find #"\d" (str(first change))))
                (Integer/parseInt(str(first change))) 999)
          next-found (if (< pos 8) (conj found pos) found)
          value (if (nil? change) nil (second change))
          next-pw (if (and (< pos 8) (not(contains? found pos)))
             (assoc pw-so-far pos value)
              pw-so-far)
          ]
          (if (not (nil? change))
             (println i next-pw))
          (if (= (count found) 8) ; we got all 8 digits
            (str/join pw-so-far)
            (recur (inc i) next-pw next-found)
           ))))



(defn main [&args]
  "https://adventofcode.com/2016/day/5"

  (def s "abbhdwsy")

  ; part a
  ; for loop version (but how to break out?)
  ; 1m38s
  ;(println(str (for [i (range 12850800)
  ;  :let [md5sum (md5 (str s i))]
  ;  :when (= (subs md5sum 0 5) "00000")]
  ;  (get md5sum 5)))

  ; recursive version
  ; 1m3s
  (println "Part A" (pw s))


  ; part b
  ; 3m10s
  (println "Part B" (pw2 s))
)

