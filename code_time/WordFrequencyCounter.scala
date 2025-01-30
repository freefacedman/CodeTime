import scala.io.Source

object WordFrequencyCounter {

  // Function to clean and tokenize input text
  def tokenize(text: String): List[String] = {
    text.toLowerCase.replaceAll("[^a-zA-Z0-9\\s]", "").split("\\s+").toList
  }

  // Function to count word frequencies
  def countWords(words: List[String]): Map[String, Int] = {
    words.groupBy(identity).view.mapValues(_.size).toMap
  }

  // Function to read file and process it
  def processFile(filename: String): Map[String, Int] = {
    val source = Source.fromFile(filename)
    val text = try source.getLines().mkString(" ") finally source.close()
    val words = tokenize(text)
    countWords(words)
  }

  // Main function
  def main(args: Array[String]): Unit = {
    if (args.length != 1) {
      println("Usage: scala WordFrequencyCounter.scala <filename>")
    } else {
      val filename = args(0)
      val wordCounts = processFile(filename)

      // Print results
      wordCounts.toList.sortBy(-_._2).foreach { case (word, count) =>
        println(s"$word: $count")
      }
    }
  }
}

How It Works
Tokenization (tokenize): Cleans text and splits it into words.
Word Counting (countWords): Uses groupBy and mapValues to count word occurrences.
File Handling (processFile): Reads the input file, processes it, and returns word frequencies.
Functional Programming Paradigm: The entire program uses pure functions and avoids mutable state.


scalac WordFrequencyCounter.scala
Run:
sh
scala WordFrequencyCounter example.txt
(Replace example.txt with the file you want to analyze.)
This implementation follows a fully functional programming style, making it efficient, readable, and easy to reason about. 
