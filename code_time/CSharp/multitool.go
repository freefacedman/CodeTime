package main

import (
    "bufio"
    "encoding/json"
    "fmt"
    "io/fs"
    "io/ioutil"
    "os"
    "path/filepath"
    "regexp"
    "strings"
)

// ====================================
// 1. WORD FREQUENCY SUBCOMMAND
// ====================================
func wordFrequencyCommand(args []string) {
    if len(args) < 1 {
        fmt.Println("Usage: go run multitool.go wordfreq <filename>")
        return
    }
    filename := args[0]

    // Read file contents
    content, err := ioutil.ReadFile(filename)
    if err != nil {
        fmt.Printf("Error reading file: %v\n", err)
        return
    }

    // Tokenize text (lowercase, remove punctuation, split by whitespace)
    text := strings.ToLower(string(content))
    re := regexp.MustCompile(`[^a-z0-9\s]+`)
    cleanText := re.ReplaceAllString(text, "")
    words := strings.Fields(cleanText)

    // Count frequencies
    freqMap := make(map[string]int)
    for _, w := range words {
        freqMap[w]++
    }

    // Sort and print
    type kv struct {
        Key   string
        Value int
    }
    var freqSlice []kv
    for k, v := range freqMap {
        freqSlice = append(freqSlice, kv{k, v})
    }

    // Sort by highest frequency
    // If equal, sort alphabetically
    sortByFreq := func(i, j int) bool {
        if freqSlice[i].Value == freqSlice[j].Value {
            return freqSlice[i].Key < freqSlice[j].Key
        }
        return freqSlice[i].Value > freqSlice[j].Value
    }

    // Implement insertion sort manually (for demonstration),
    // but you could also use "sort.Slice" from the standard library.
    for i := 1; i < len(freqSlice); i++ {
        j := i
        for j > 0 && sortByFreq(j, j-1) {
            freqSlice[j], freqSlice[j-1] = freqSlice[j-1], freqSlice[j]
            j--
        }
    }

    for _, pair := range freqSlice {
        fmt.Printf("%s: %d\n", pair.Key, pair.Value)
    }
}

// ====================================
// 2. FIBONACCI SUBCOMMAND
// ====================================
func fibonacciCommand(args []string) {
    if len(args) < 1 {
        fmt.Println("Usage: go run multitool.go fibonacci <n>")
        return
    }

    // Convert argument to integer
    n, err := parseInt(args[0])
    if err != nil {
        fmt.Println("Invalid number:", args[0])
        return
    }

    // Generate the first n Fibonacci numbers
    fibs := fibonacci(n)
    fmt.Println(fibs)
}

// fibonacci is a simple function returning the first n Fibonacci numbers.
func fibonacci(n int) []int {
    if n <= 0 {
        return []int{}
    }
    if n == 1 {
        return []int{0}
    }

    result := make([]int, n)
    result[0] = 0
    if n > 1 {
        result[1] = 1
    }
    for i := 2; i < n; i++ {
        result[i] = result[i-1] + result[i-2]
    }
    return result
}

// parseInt is a small helper that safely converts a string to int.
func parseInt(s string) (int, error) {
    var x int
    _, err := fmt.Sscan(s, &x)
    return x, err
}

// ====================================
// 3. JSON PARSER SUBCOMMAND
// ====================================
func jsonParseCommand(args []string) {
    if len(args) < 1 {
        fmt.Println("Usage: go run multitool.go jsonparse <file.json>")
        return
    }
    filename := args[0]

    data, err := ioutil.ReadFile(filename)
    if err != nil {
        fmt.Printf("Error reading JSON file: %v\n", err)
        return
    }

    // Decode the JSON into a map
    var jsonObj interface{}
    err = json.Unmarshal(data, &jsonObj)
    if err != nil {
        fmt.Printf("Error parsing JSON: %v\n", err)
        return
    }

    // Recursively print keys
    printJSON(jsonObj, "")
}

// printJSON recursively walks through the JSON object and prints each key-value pair.
func printJSON(obj interface{}, prefix string) {
    switch val := obj.(type) {
    case map[string]interface{}:
        for k, v := range val {
            newPrefix := k
            if prefix != "" {
                newPrefix = prefix + "." + k
            }
            printJSON(v, newPrefix)
        }
    case []interface{}:
        for i, v := range val {
            newPrefix := fmt.Sprintf("%s[%d]", prefix, i)
            printJSON(v, newPrefix)
        }
    default:
        // val is a string, float64, bool, nil, etc.
        fmt.Printf("%s: %v\n", prefix, val)
    }
}

// ====================================
// 4. PIPELINE SUBCOMMAND
// ====================================
func pipelineCommand(args []string) {
    if len(args) < 1 {
        fmt.Println("Usage: go run multitool.go pipeline \"some text\"")
        return
    }
    input := strings.Join(args, " ")

    // A small pipeline of transformations (capitalize, reverse, exclaim)
    transform := pipeline(capitalize, reverse, exclaim)
    result := transform(input)

    fmt.Println(result)
}

// pipeline composes multiple functions into one.
func pipeline(funcs ...func(string) string) func(string) string {
    return func(input string) string {
        output := input
        for _, f := range funcs {
            output = f(output)
        }
        return output
    }
}

// Helper transformations
func capitalize(s string) string {
    scanner := bufio.NewScanner(strings.NewReader(s))
    scanner.Split(bufio.ScanWords)
    var words []string
    for scanner.Scan() {
        word := scanner.Text()
        if len(word) > 0 {
            words = append(words, strings.ToUpper(string(word[0]))+word[1:])
        } else {
            words = append(words, word)
        }
    }
    return strings.Join(words, " ")
}

func reverse(s string) string {
    runes := []rune(s)
    for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
        runes[i], runes[j] = runes[j], runes[i]
    }
    return string(runes)
}

func exclaim(s string) string {
    return s + "!!!"
}

// ====================================
// 5. FINDER SUBCOMMAND (FIND ALL .go FILES)
// ====================================
func finderCommand(args []string) {
    if len(args) < 1 {
        fmt.Println("Usage: go run multitool.go finder <directory>")
        return
    }
    dir := args[0]

    // Recursively find all .go files
    files, err := findGoFiles(dir)
    if err != nil {
        fmt.Printf("Error while walking directory: %v\n", err)
        return
    }

    for _, file := range files {
        fmt.Println(file)
    }
}

// findGoFiles returns a slice of all .go files under a specified directory.
func findGoFiles(root string) ([]string, error) {
    var goFiles []string
    err := filepath.Walk(root, func(path string, info fs.FileInfo, err error) error {
        if err != nil {
            return err
        }
        if !info.IsDir() && strings.HasSuffix(info.Name(), ".go") {
            goFiles = append(goFiles, path)
        }
        return nil
    })
    return goFiles, err
}

// ====================================
// MAIN
// ====================================
func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: go run multitool.go <subcommand> [args...]")
        fmt.Println("Available subcommands: wordfreq, fibonacci, jsonparse, pipeline, finder")
        return
    }

    subcommand := os.Args[1]
    args := os.Args[2:]

    switch subcommand {
    case "wordfreq":
        wordFrequencyCommand(args)
    case "fibonacci":
        fibonacciCommand(args)
    case "jsonparse":
        jsonParseCommand(args)
    case "pipeline":
        pipelineCommand(args)
    case "finder":
        finderCommand(args)
    default:
        fmt.Printf("Unknown subcommand: %s\n", subcommand)
    }
}
