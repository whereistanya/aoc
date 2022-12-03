(ns aoc2022.core
 (:require aoc2022.day1
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
