def find_ruby_files(dir)
  Dir.glob("#{dir}/**/*.rb").sort
end

puts find_ruby_files('.')
