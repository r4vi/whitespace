date: 2014-01-31 17:18:55.256927
title: Functional XML editing using zippers in Clojure
tags:
  - clojure
  - xml

Since the Clojure documentation for `clojure.zip` is so bad I thought
I'd walk through an example of editing some XML using a zipper.

First off you'll need to add a few dependencies to your `project.clj`:

```clojure
(defproject zipper-demo "0.1.0"
  :description "An example app to show how to edit XML in Clojure using Zippers"
  :url "https://github.com/r4vi/zipper-demo/"
  :license {:name "WTFPL – Do What the Fuck You Want to Public License"
            :url "http://www.wtfpl.net"}
  :dependencies [[org.clojure/clojure "1.5.1"]
                 [org.clojure/data.xml "0.0.7"]
                 [org.clojure/data.zip "0.1.1"]])

```

then open up `src/core.clj` and require them.

```clojure
(ns zipper-demo.core
  (:require
   [clojure.zip :as zip]
   [clojure.data.zip.xml :as zx]
   [clojure.data.xml :as xml]))
```
So what do they do?

* [clojure.zip][cz]
Allows you to create `zippers` for most of Clojure's collections, not
just XML.

```clojure
zipper-demo.core>
  (def nested-vecs
   [:foo
     [:bar :baz [:bork]]])
     
;; now let's make a zipper
zipper-demo.core> (def z
  (zip/vector-zip nested-vecs))


zipper-demo.core> (-> z
                      zip/down
                      zip/node)
;;=> :foo

;; move one step down from the head
;;  left side <-----------  | -------> right side
;; [:foo  *<-- we are here*  [:bar :baz [:bork]]]

zipper-demo.core> (-> z
                      zip/down
                      zip/right
                      zip/node) 
;; [:bar :baz [:bork]]
;; [:foo [:bar :baz [:bork]] *<-- we are here*]


;; lets move to the :bork leaf
zipper-demo.core> (-> z
                      zip/down
                      zip/right
                      zip/down
                      zip/right
                      zip/right
                      zip/down
                      zip/node) 
;; :bork

;; we can edit too
zipper-demo.core> (-> z
                      zip/down
                      zip/right
                      zip/down
                      zip/right
                      zip/right
                      zip/down
                     (zip/edit #(clojure.string/upper-case %))
                      zip/node) 
;; :BORK

;; to get the entire (edited) structure back we can do this

zipper-demo.core> (-> z
                      zip/down
                      zip/right
                      zip/down
                      zip/right
                      zip/right
                      zip/down
                     (zip/edit #(clojure.string/upper-case %))
                      zip/root) 
;; [:foo [:bar :baz [":BORK"]]]
```


* [clojure.data.xml][cdx]

I would recommend using `clojure.data.xml` to parse xml rather than
`clojure.xml` which seems like a toy library, because it doesn't
output to a stream but actually prints the xml to the console when
parsing so you need to wrap it `with-out-str`, when you output xml it
doesn't escape xml entities so you end up with invalid xml and it's
not lazy so huge xml files will make it choke.

If you wanted to load a file in your resources directory called
`pokemon.xml`, do the following:

```clojure
zipper-demo.core> (def pokemon
                    (-> "pokemon.xml"
                        clojure.java.io/resource
                        clojure.java.io/input-stream
                        xml/parse))

;; #'zipper-demo.core/pokemon
;; this returns an element tree, each element has a :tag, :attrs and
;; :content

zipper-demo.core> (keys pokemon)
;; (:tag :attrs :content)
;; we can explore the data like this
zipper-demo.core> (first (:content pokemon))
;;{:tag :pokemon,
;; :attrs {:id "1"},
;; :content
;; ({:tag :name, :attrs {}, :content ("BULBASAUR")}
;;  {:tag :type, :attrs {}, :content ("Grass")}
;;  {:tag :type, :attrs {}, :content ("Poison")}
;;  {:tag :ability, :attrs {}, :content ("Overgrow")}
;;  {:tag :exp, :attrs {}, :content ("1059860")}
;;  {:tag :stats,
;;   :attrs {},
;;   :content
;;   ({:tag :HP, :attrs {}, :content ("45")}
;;    {:tag :ATK, :attrs {}, :content ("49")}
;;    {:tag :DEF, :attrs {}, :content ("49")}
;;    {:tag :SPD, :attrs {}, :content ("45")}
;;    {:tag :SAT, :attrs {}, :content ("65")}
;;    {:tag :SDF, :attrs {}, :content ("65")})}
;;  {:tag :evolutions,
;;   :attrs {},
;;   :content
;;   ({:tag :evolution,
;;     :attrs {:id "1"},
;;     :content ({:tag :name, :attrs {}, :content ("Bulbasaur")})}
;;    {:tag :evolution,
;;     :attrs {:id "2"},
;;     :content
;;     ({:tag :name, :attrs {}, :content ("Ivysaur")}
;;      {:tag :lvl, :attrs {}, :content ("16")})}
;;    {:tag :evolution,
;;     :attrs {:id "3"},
;;     :content
;;     ({:tag :name, :attrs {}, :content ("Venusaur")}
;;      {:tag :lvl, :attrs {}, :content ("32")})})}
;;  {:tag :ratio,
;;   :attrs {},
;;   :content
;;   ({:tag :male, :attrs {}, :content ("87.5")}
;;    {:tag :female, :attrs {}, :content ("12.5")})}
;;  {:tag :egg-group, :attrs {}, :content ("Monster")}
;;  {:tag :egg-group, :attrs {}, :content ("Grass")}
;;  {:tag :species, :attrs {}, :content ("Seed Pokemon")}
;;  {:tag :height, :attrs {}, :content ("0.7")}
;;  {:tag :weight, :attrs {}, :content ("6.9")}
;;  {:tag :description,
;;   :attrs {},
;;   :content
;;   ("For some time after its birth, it grows by gaining nourishment from the seed on its back.")}
;;  {:tag :moves,
;;   :attrs {},
;;   :content
;;   ({:tag :move,
;;     :attrs {:type "level-up"},
;;     :content
;;     ({:tag :name, :attrs {}, :content ("Tackle")}
;;      {:tag :lvl, :attrs {}, :content ("1")})}
;;    {:tag :move,
;;     :attrs {:type "level-up"},
;;     :content
;;     ({:tag :name, :attrs {}, :content ("Growl")}
;;      {:tag :lvl, :attrs {}, :content ("3")})}
;;    {:tag :move,
;;     :attrs {:type "level-up"},
;;     :content
;;     ({:tag :name, :attrs {}, :content ("Leech Seed")}
;;      {:tag :lvl, :attrs {}, :content ("7")})}
;;    {:tag :move,
;;     :attrs {:type "level-up"},
;;     :content
;;     ({:tag :name, :attrs {}, :content ("Vine Whip")}
;;      {:tag :lvl, :attrs {}, :content ("9")})}
;;    {:tag :move,
;;     :attrs {:type "level-up"},
;;     :content
;;     ({:tag :name, :attrs {}, :content ("Poisonpowder")}
;;      {:tag :lvl, :attrs {}, :content ("13")})}
;;    {:tag :move,
;;     :attrs {:type "level-up"},
;;     :content
;;     ({:tag :name, :attrs {}, :content ("Sleep Powder")}
;;      {:tag :lvl, :attrs {}, :content ("13")})}
;;    {:tag :move,
;;     :attrs {:type "level-up"},
;;     :content
;;     ({:tag :name, :attrs {}, :content ("Take Down")}
;;      {:tag :lvl, :attrs {}, :content ("15")})}
;;    {:tag :move,
;;     :attrs {:type "level-up"},
;;     :content
;;     ({:tag :name, :attrs {}, :content ("Razor Leaf")}
;;      {:tag :lvl, :attrs {}, :content ("19")})}
;;    {:tag :move,
;;     :attrs {:type "level-up"},
;;     :content
;;     ({:tag :name, :attrs {}, :content ("Sweet Scent")}
;;      {:tag :lvl, :attrs {}, :content ("21")})}
;;    {:tag :move,
;;     :attrs {:type "level-up"},
;;     :content
;;     ({:tag :name, :attrs {}, :content ("Growth")}
;;      {:tag :lvl, :attrs {}, :content ("25")})}
;;    {:tag :move,
;;     :attrs {:type "level-up"},
;;     :content
;;     ({:tag :name, :attrs {}, :content ("Double-edge")}
;;      {:tag :lvl, :attrs {}, :content ("27")})}
;;    {:tag :move,
;;     :attrs {:type "level-up"},
;;     :content
;;     ({:tag :name, :attrs {}, :content ("Worry Seed")}
;;      {:tag :lvl, :attrs {}, :content ("31")})}
;;    {:tag :move,
;;     :attrs {:type "level-up"},
;;     :content
;;     ({:tag :name, :attrs {}, :content ("Synthesis")}
;;      {:tag :lvl, :attrs {}, :content ("33")})}
;;    {:tag :move,
;;     :attrs {:type "level-up"},
;;     :content
;;     ({:tag :name, :attrs {}, :content ("Seed Bomb")}
;;      {:tag :lvl, :attrs {}, :content ("37")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Toxic")}
;;      {:tag :lvl, :attrs {}, :content ("06")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Bullet Seed")}
;;      {:tag :lvl, :attrs {}, :content ("09")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Hidden Power")}
;;      {:tag :lvl, :attrs {}, :content ("10")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Sunny Day")}
;;      {:tag :lvl, :attrs {}, :content ("11")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Protect")}
;;      {:tag :lvl, :attrs {}, :content ("17")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Giga Drain")}
;;      {:tag :lvl, :attrs {}, :content ("19")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Frustration")}
;;      {:tag :lvl, :attrs {}, :content ("21")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Solarbeam")}
;;      {:tag :lvl, :attrs {}, :content ("22")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Return")}
;;      {:tag :lvl, :attrs {}, :content ("27")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Double Team")}
;;      {:tag :lvl, :attrs {}, :content ("32")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Sludge Bomb")}
;;      {:tag :lvl, :attrs {}, :content ("36")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Facade")}
;;      {:tag :lvl, :attrs {}, :content ("42")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Secret Power")}
;;      {:tag :lvl, :attrs {}, :content ("43")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Rest")}
;;      {:tag :lvl, :attrs {}, :content ("44")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Attract")}
;;      {:tag :lvl, :attrs {}, :content ("45")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Energy Ball")}
;;      {:tag :lvl, :attrs {}, :content ("53")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Endure")}
;;      {:tag :lvl, :attrs {}, :content ("58")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Flash")}
;;      {:tag :lvl, :attrs {}, :content ("70")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Swords Dance")}
;;      {:tag :lvl, :attrs {}, :content ("75")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Captivate")}
;;      {:tag :lvl, :attrs {}, :content ("78")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Sleep Talk")}
;;      {:tag :lvl, :attrs {}, :content ("82")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Natural Gift")}
;;      {:tag :lvl, :attrs {}, :content ("83")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Grass Knot")}
;;      {:tag :lvl, :attrs {}, :content ("86")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Swagger")}
;;      {:tag :lvl, :attrs {}, :content ("87")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("TM")}
;;      {:tag :name, :attrs {}, :content ("Substitute")}
;;      {:tag :lvl, :attrs {}, :content ("90")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("HM")}
;;      {:tag :name, :attrs {}, :content ("Cut")}
;;      {:tag :lvl, :attrs {}, :content ("1")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("HM")}
;;      {:tag :name, :attrs {}, :content ("Strength")}
;;      {:tag :lvl, :attrs {}, :content ("4")})}
;;    {:tag :move,
;;     :attrs {:type "TM/HM"},
;;     :content
;;     ({:tag :machine, :attrs {}, :content ("HM")}
;;      {:tag :name, :attrs {}, :content ("Rock Smash")}
;;      {:tag :lvl, :attrs {}, :content ("6")})}
;;    {:tag :move,
;;     :attrs {:type "egg"},
;;     :content ({:tag :name, :attrs {}, :content ("Amnesia")})}
;;    {:tag :move,
;;     :attrs {:type "egg"},
;;     :content ({:tag :name, :attrs {}, :content ("Charm")})}
;;    {:tag :move,
;;     :attrs {:type "egg"},
;;     :content ({:tag :name, :attrs {}, :content ("Curse")})}
;;    {:tag :move,
;;     :attrs {:type "egg"},
;;     :content ({:tag :name, :attrs {}, :content ("Grasswhistle")})}
;;    {:tag :move,
;;     :attrs {:type "egg"},
;;     :content ({:tag :name, :attrs {}, :content ("Ingrain")})}
;;    {:tag :move,
;;     :attrs {:type "egg"},
;;     :content ({:tag :name, :attrs {}, :content ("Leaf Storm")})}
;;    {:tag :move,
;;     :attrs {:type "egg"},
;;     :content ({:tag :name, :attrs {}, :content ("Light Screen")})}
;;    {:tag :move,
;;     :attrs {:type "egg"},
;;     :content ({:tag :name, :attrs {}, :content ("Magical Leaf")})}
;;    {:tag :move,
;;     :attrs {:type "egg"},
;;     :content ({:tag :name, :attrs {}, :content ("Nature Power")})}
;;    {:tag :move,
;;     :attrs {:type "egg"},
;;     :content ({:tag :name, :attrs {}, :content ("Petal Dance")})}
;;    {:tag :move,
;;     :attrs {:type "egg"},
;;     :content ({:tag :name, :attrs {}, :content ("Safeguard")})}
;;    {:tag :move,
;;     :attrs {:type "egg"},
;;     :content ({:tag :name, :attrs {}, :content ("Skull Bash")})})})}
```

This can get annoying as you get deeper in the structure, we can use
a zipper instead.

```clojure
zipper-demo.core> (def pokemon-zip (zip/xml-zip pokemon))
;; #'zipper-demo.core/pokemon-zip

zipper-demo.core> (-> pokemon-zip zip/down zip/right zip/node)

;;{:tag :pokemon,
;; :attrs {:id "1"},
;; :content
;; ({:tag :name, :attrs {}, :content ("BULBASAUR")}
;;  {:tag :type, :attrs {}, :content ("Grass")}
;;  {:tag :type, :attrs {}, :content ("Poison")}
;;  {:tag :ability, :attrs {}, :content ("Overgrow")}
;;  {:tag :exp, :attrs {}, :content ("1059860")}
;;  {:tag :stats,
;;   :attrs {},
;;   :content
;;   ({:tag :HP, :attrs {}, :content ("45")}
;;    {:tag :ATK, :attrs {}, :content ("49")}
;;    {:tag :DEF, :attrs {}, :content ("49")}
;;    {:tag :SPD, :attrs {}, :content ("45")}
;; ...
```

* [clojure.data.xml.zip][zx]

If you do any programming on the web you still find this convoluted
compared to `document.querySelector` or `document.querySelectorAll`
when working with the DOM. That's where `clojure.data.xml.zip` comes
in.

`xml->` is equivalent to `document.querySelectorAll` and `xml1->` is
equivalent to `document.querySelector` in that `xml->` will return all
elements that match a given predicate, `xml1->` will only return the
first one. The predicates can be chained and `clojure.data.xml.zip`
provides a few helpers for common things like tag names or attribute
values.

Say you wanted to get the name of the fist pokemon:

```clojure
(zip/node (zip/down
     (zx/xml1-> pokemon-zip :pokemon :name)))
;; "BULBASAUR"
```
This matches all &lt;name&gt; tags inside &lt;pokemon&gt; tags and returns the
first element. We use zip/down to move into the text-content location
instead of returning the actual element location, then we use zip/node
to turn the location we're at into a real value from the pokemon structure.

If you want the name of every pokemon you could do this:

```clojure
zipper-demo.core> (map zip/node
                    (map zip/down
                      (zx/xml-> pokemon-zip :pokemon :name)))

;;("BULBASAUR" "IVYSAUR" "VENUSAUR" "CHARMANDER" "CHARMELEON"
;;  "CHARIZARD" "SQUIRTLE" "WARTORTLE" "BLASTOISE" "CATERPIE" "METAPOD"
;;  "BUTTERFREE" "WEEDLE" "KAKUNA" "BEEDRILL" "PIDGEY" "PIDGEOTTO"
;;  "PIDGEOT" "RATTATA" "RATICATE" "SPEAROW" "FEAROW" "EKANS" "ARBOK"
;;  "PIKACHU" ";;RAICHU" "SANDSHREW" "SANDSLASH" "NIDORAN" "NIDORINA"
;;  "NIDOQUEEN" "NIDORAN" "NIDORINO" "NIDOKING" "CLEFAIRY" "CLEFABLE"
;;  "NOCTOWL" "LEDYBA" "LEDIAN" "SPINARAK" "ARIADOS" "CROBAT" "CHINCHOU"
;;  "LANTURN" "PICHU" "CLEFFA" "IGGLYBUFF" "TOGEPI" "TOGETIC" "NATU"
;;  "XATU" "MAREEP" "FLAAFFY" "AMPHAROS" "BELLOSSOM" "MARILL"
;;  "AZUMARILL" "SUDOWOODO" "POLITOED" "HOPPIP" "SKIPLOOM" "JUMPLUFF"
;;  "AIPOM" "HO" "SUNKERN" "SUNFLORA" "YANMA" "WOOPER" "QUAGSIRE"
;;  "ESPEON" "UMBREON" "MURKROW" "SLOWKING" "MISDREAVUS" "UNOWN"
;;  "WOBBUFFET" "GIRAFARIG" "PINECO" "FORRETRESS" "DUNSPARCE" "GLIGAR"
;;  "STEELIX" "SNUBBULL" "GRANBULL" "QWILFISH" "SCIZOR" "SHUCKLE"
;;  "HERACROSS" "SNEASEL" "TEDDIURSA" "URSARING" "SLUGMA" "MAGCARGO"
;; ...
;;  "CRESSELIA" "PHIONE" "MANAPHY" "DARKRAI" "SHAYMIN" "ARCEUS")
```

If you want to get the name of a pokemon by it's ID then you could do
this:

```clojure
(zip/node (zx/xml1-> pokemon-zip :pokemon (zx/attr= :id "2") :name))
;; #clojure.data.xml.Element{:tag :name, :attrs {}, :content ("IVYSAUR")}
```

### Round-tripping XML
Now to get to the point of this whole post, round-tripping some XML.
Suppose you have some XML containing an inventory of books that looks
like this:

```clojure
(def books
"
<?xml version=\"1.0\"?>
<catalog>
   <book id=\"bk101\">
      <author>Gambardella, Matthew</author>
      <title>XML Developer's Guide</title>
      <genre>Computer</genre>
      <publish_date>2000-10-01</publish_date>
      <description>An in-depth look at creating applications 
      with XML.</description>
   </book>
   <book id=\"bk102\">
      <author>Ralls, Kim</author>
      <title>Midnight Rain</title>
      <genre>Fantasy</genre>
      <publish_date>2000-12-16</publish_date>
      <description>A former architect battles corporate zombies, 
      an evil sorceress, and her own childhood to become queen 
      of the world.</description>
   </book>
   <book id=\"bk103\">
      <author>Corets, Eva</author>
      <title>Maeve Ascendant</title>
      <genre>Fantasy</genre>
      <publish_date>2000-11-17</publish_date>
      <description>After the collapse of a nanotechnology 
      society in England, the young survivors lay the 
      foundation for a new society.</description>
   </book>
   <book id=\"bk104\">
      <author>Corets, Eva</author>
      <title>Oberon's Legacy</title>
      <genre>Fantasy</genre>
      <publish_date>2001-03-10</publish_date>
      <description>In post-apocalypse England, the mysterious 
      agent known only as Oberon helps to create a new life 
      for the inhabitants of London. Sequel to Maeve 
      Ascendant.</description>
   </book>
   <book id=\"bk105\">
      <author>Corets, Eva</author>
      <title>The Sundered Grail</title>
      <genre>Fantasy</genre>
      <publish_date>2001-09-10</publish_date>
      <description>The two daughters of Maeve, half-sisters, 
      battle one another for control of England. Sequel to 
      Oberon's Legacy.</description>
   </book>
</catalog>
")
```
and you have a map of ids and prices:

```clojure
(def prices
  {:bk101 "44.95"
   :bk102 "12.50"
   :bk103 "24.20"
   :bk104 "4.20"
   :bk105 "45.00"})

```
You want to add a price tag to each book, with the price looked up
from `prices`.

Let's start by turning the XML into a zipper.

```clojure
(def books-as-elements (xml/parse-str books))
(def books-zipper (zip/xml-zip books-as-elements))
```

then we can use this tree edit function, it takes a zipper to edit, a
predicate to tell it which nodes need to be edited and a edit function
which takes a node and returns an edited node.

```clojure
(defn tree-edit
  "Take a zipper, a function that matches a pattern in the tree,
   and a function that edits the current location in the tree.  Examine the tree
   nodes in depth-first order, determine whether the matcher matches, and if so
   apply the editor."
  [zipper matcher editor]
  (loop [loc zipper]
    (if (zip/end? loc)
      (zip/root loc)
      (if-let [matcher-result (matcher loc)]
        (let [new-loc (zip/edit loc editor)]
          (if (not (= (zip/node new-loc) (zip/node loc)))
            (recur (zip/next new-loc))))
        (recur (zip/next loc))))))

;; match predicate, all book tags
(defn match-book? [loc]
  (let [tag (:tag (zip/node loc))]
    ;; true if tag is of type <path>
    (= :book tag)))

;; edit function
(defn editor [node]
  (let [id (-> node :attrs :id keyword)
        new-content (conj
                     (:content node)
                     (xml/element :price {} (get prices id "0.0")))]
    (assoc-in node [:content] new-content)))

(def edited (tree-edit books-zipper match-book? editor))  

(xml/indent-str
 edited)

;; <catalog>
;;<book id="bk101">
;;<price>44.95</price>
;;<author>Gambardella, Matthew</author>
;;<title>XML Developer's Guide</title>
;;<genre>Computer</genre>
;;<publish_date>2000-10-01</publish_date>
;;<description>
;;An in-depth look at creating applications with XML.
;;</description>
;;</book>


;; save it
(with-open [f (clojure.java.io/writer  "/tmp/books_with_prices.xml")]
  (xml/emit edited f))

```

If you want to play with this stuff yourself then the demo project is
on [github][gh]

[zx]: https://github.com/clojure/data.zip/blob/master/src/main/clojure/clojure/data/zip/xml.clj
[cdx]: https://github.com/clojure/data.xml
[cz]: http://richhickey.github.io/clojure/clojure.zip-api.html
[so]: http://stackoverflow.com/questions/11537923/searching-xml-in-clojure
[nak]: http://nakkaya.com/2009/12/07/zipping-xml-with-clojure/
[tbt]: http://techbehindtech.com/2010/06/25/parsing-xml-in-clojure/
[gh]: https://github.com/r4vi/zipper-demo

