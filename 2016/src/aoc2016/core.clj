(ns aoc2016.core
 (:require aoc2016.day1
           aoc2016.day2
           [clojure.string :as str])

  (:gen-class))


(defn -main
  "Actual main!"
  [day & args]
  (let [day-ns (symbol (clojure.string/join "." ["aoc2016" day]))
        day-main (ns-resolve day-ns 'main)]
    (day-main args)))
