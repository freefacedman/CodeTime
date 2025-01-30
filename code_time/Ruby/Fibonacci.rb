def fibonacci(n, a = 0, b = 1)
  n == 0 ? [] : [a] + fibonacci(n - 1, b, a + b)
end

puts fibonacci(10).inspect
