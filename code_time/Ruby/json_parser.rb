require 'json'

def parse_json_file(filename)
  JSON.parse(File.read(filename))
end

def print_json_keys(json_obj, prefix = '')
  json_obj.each do |key, value|
    new_prefix = prefix.empty? ? key : "#{prefix}.#{key}"
    if value.is_a?(Hash)
      print_json_keys(value, new_prefix)
    else
      puts "#{new_prefix}: #{value}"
    end
  end
end

if ARGV.length != 1
  puts "Usage: ruby json_parser.rb <file.json>"
else
  json_data = parse_json_file(ARGV[0])
  print_json_keys(json_data)
end

run with sh
ruby json_parser.rb data.json 
