import glob
import os 
import radon.metrics as m
import radon.complexity as c
import radon.raw as r

  
def py2str(py_file):   
    #read input file
    fin = open(py_file, "rt")
    
    #read file contents to string
    data = fin.read()
    
    #close the input file
    fin.close()
    
    return data

def analyze_code(code):
    analysis = r.analyze(code)
    hal_vol, cc, lloc, comment_percentage = m.mi_parameters(code)
    cc_rank = c.cc_rank(cc)
    cc_rank_dict = {'A': "low - simple block",
                    'B': "low - well structured and stable block",
                    'C': "moderate - slightly complex block",
                    'D': "more than moderate - more complex block",
                    'E': "high - complex block, alarming",
                    'F': "very high - error-prone, unstable block"}
    
    cc_results = c.sorted_results(c.cc_visit(code))
    mi_score = m.mi_visit(code, 4)
    mi_rank = m.mi_rank(mi_score)
    mi_rank_dict = {'A': "Very high, good to go",
                   'B': "Medium, acceptable",
                   'C': "Extremely low, unacceptable"}
    
    
    #printing results
    print("======================================================================")
    print("[Overall Code Analysis]")
    print(analysis)
    print("Halsted Volume: " + str(hal_vol)) 
    print("Code Cyclomatic Complexity: " + str(cc))
    print("Code Cyclomatic Complexity Grade: " + cc_rank)
    print("Logical lines of code: " + str(lloc))
    print("Percentage of lines " + "of comment: " + 
          str(round(comment_percentage,2)) + "%.")
    print("======================================================================")
    print("[Cyclomatic Complexity Analysis]")
    print(cc_results)
    print("======================================================================")
    print("[Maintainability Analysis]")
    print("Maintainability Index Score: " + str(round(mi_score,2)))
    print("Maintainability Index Grade: " + mi_rank)
    print("======================================================================")
    print("[Analysis Result]")
    print("Overall level of Maintainability: " + mi_rank_dict.get(mi_rank))
    print("Overall level of Cyclomatic Complexity: " + cc_rank_dict.get(cc_rank))


def main():
    print("Getting all python files in currect working directory: " + os.getcwd())
    pyFiles = glob.glob('*.py')
    for file in pyFiles:
        try:
            print()
            print("Running analysis on file: " + file)
            code = py2str(file)
            analyze_code(code)
        except:
            raise RuntimeError("Something went wrong when analyzing: " + file)

if __name__ == "__main__":
    main()