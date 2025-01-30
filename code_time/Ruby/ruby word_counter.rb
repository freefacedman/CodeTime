def tokenize(text)
  text.downcase.gsub(/[^a-z0-9\s]/, '').split
end

def count_words(words)
  words.group_by(&:itself).transform_values(&:count)
end

def process_file(filename)
  words = tokenize(File.read(filename))
  count_words(words)
end

if ARGV.length != 1
  puts "Usage: ruby word_counter.rb <filename>"
else
  word_counts = process_file(ARGV[0])
  word_counts.sort_by { |_word, count| -count }.each { |word, count| puts "#{word}: #{count}" }
end

Run with:
sh
ruby word_counter.rb example.txt
