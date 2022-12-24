(ns aoc2022.core
 (:require aoc2022.day1
           aoc2022.day2
           aoc2022.day4
           aoc2022.day5
           aoc2022.day6
           aoc2022.day13
           [clojure.string :as str])

  (:gen-class))


(defn -main
  "Nifty day-chooser stolen from emauton
  https://github.com/emauton/aoc2020/blob/main/src/aoc2020/core.clj
  Run it like
    lein run day1 <args>
  "
  [day & args]
  (let [day-ns (symbol (clojure.string/join "." ["aoc2022" day]))
        day-main (ns-resolve day-ns 'main)]
    (day-main args)))
