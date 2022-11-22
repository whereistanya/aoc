(ns aoc2016.core
 (:require aoc2016.day1
           aoc2016.day2
           aoc2016.day3
           aoc2016.day4
           aoc2016.day5
           aoc2016.day6
           aoc2016.day7
           [clojure.string :as str])

  (:gen-class))


(defn -main
  "Nifty day-chooser stolen from emauton
  https://github.com/emauton/aoc2020/blob/main/src/aoc2020/core.clj
  Run it like
    lein run day1 <args>
  "
  [day & args]
  (let [day-ns (symbol (clojure.string/join "." ["aoc2016" day]))
        day-main (ns-resolve day-ns 'main)]
    (day-main args)))
