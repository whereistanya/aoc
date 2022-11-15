(ns aoc2016.day1
  (:require [clojure.string :as str]))

(defn turn
  "orient in a direction"
  [current dir]
  ;(println "* turn" current dir)
  (let [turnvalue (if (= (str dir) "R") 1 
                    (if(= (str dir) "L") 3 (println "YIKES" dir "\n\n\n")))
        orientations {:north 0 :east 1 :south 2 :west 3 }
        reverse-orientations {0 :north 1 :east 2 :south 3 :west }
        current-value (get orientations current)
        turn-to (mod(+ turnvalue current-value) 4)
        ]
    ;(println "Moving to face ", (get wtf-orientations turn-to))
    (get reverse-orientations turn-to))
)

(defn takestep
  "Split a letter number pair, turn to L or R, move the number"
  [instruction location]
  ;(println "* takestep" instruction location)
  (let [letter (first instruction)
        number (Integer/parseInt (subs instruction 1))
        orientation (first location)
        face (turn orientation letter)
        x (nth location 1)
        y (nth location 2)
        newx (+ x (if (= face :east) number
                   (if (= face :west) (* number -1) 0)))
        newy (+ y (if (= face :north) number
                   (if (= face :south) (* number -1) 0)))
        ]
    ; return the direction we're now facing and the new x, y coords
    ; as well as all the spaces passed along the way
    [face newx newy]))

(defn line-segment [pos1 pos2]
  (let [[_ x1 y1] pos1
        [_ x2 y2] pos2
        dx (if (> x1 x2) -1 1)
        dy (if (> y1 y2) -1 1)]
    (for [x (range x1 (+ dx x2) dx)
          y (range y1 (+ dy y2) dy)]
      [x y])
    ))


(defn takesteps
  "Expects a sequence of two character directions like R2,L3,R5,.."
  [steps-to-take part]
  ; initialize remaining-steps to steps-to-take.
  ; final-route will hold the result, initially empty
  (loop [remaining-steps steps-to-take
         final-route [ [:north 0 0] ]
         seen (set []) ]
    (if (empty? remaining-steps)
      final-route ; finished! return it
      ; else... split into next-step and remaining-steps
      (let [[next-step & remaining] remaining-steps
            currentpos (last final-route)
            nextpos (takestep next-step currentpos)
            [face & pos] nextpos
            visited (line-segment currentpos nextpos)
            return-visit (some seen (rest visited)) ; 'rest' to remove the head
            ]
        ; if it's part b and we've already seen a place we visited this time...
        (if (and (= part :partb)(some? return-visit))
            return-visit ; return the place we saw
          ; else take a step, add it to the route, then recurse with the rest of the steps
           (recur remaining
             (conj final-route nextpos)
             (into seen visited))

           )))))


(defn main
  "https://adventofcode.com/2016/day/1"
  [& args]

  (def s (slurp "src/aoc2016/input1.txt"))
  (let [instructions (map str/trim (str/split s #","))]

    (println "Running instructions:" instructions "." )
    (let [locations (takesteps instructions :parta)
          destination (last locations)
          distance (+ (abs (nth destination 1))
                      (abs (nth destination 2)))]
      (println "PartA distance is" distance))

    (let [location (takesteps instructions :partb)
          distance (+ (abs (nth location 0))
                      (abs (nth location 1)))]
      (println "PartB distance is" distance)))
  (println "done"))

