def pipeline(data, *functions)
  functions.reduce(data) { |acc, func| func.call(acc) }
end

capitalize = ->(s) { s.split.map(&:capitalize).join(' ') }
reverse = ->(s) { s.reverse }
exclaim = ->(s) { s + '!!!' }

puts pipeline("hello world", capitalize, reverse, exclaim)
