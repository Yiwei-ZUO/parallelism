| Files | Version | Runs (s) | Mean (s) | Min (s) | Max (s) | Matches Baseline |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| 10 | sequential | 0.4935 / 0.4922 / 0.4950 | 0.4936 | 0.4922 | 0.4950 | - |
| 10 | threads | 0.4905 / 0.4991 / 0.4994 | 0.4963 | 0.4905 | 0.4994 | True |
| 10 | processes | 0.2838 / 0.2757 / 0.2829 | 0.2808 | 0.2757 | 0.2838 | True |
| 30 | sequential | 1.3958 / 1.4216 / 1.4330 | 1.4168 | 1.3958 | 1.4330 | - |
| 30 | threads | 1.4376 / 1.4465 / 1.4615 | 1.4485 | 1.4376 | 1.4615 | True |
| 30 | processes | 0.5205 / 0.5324 / 0.5334 | 0.5287 | 0.5205 | 0.5334 | True |
| 50 | sequential | 2.3885 / 2.5020 / 2.4899 | 2.4601 | 2.3885 | 2.5020 | - |
| 50 | threads | 2.4305 / 2.4424 / 2.4580 | 2.4436 | 2.4305 | 2.4580 | True |
| 50 | processes | 0.8394 / 0.8469 / 0.8345 | 0.8403 | 0.8345 | 0.8469 | True |

## Profiling Results (sequential, limit=50)
```text
         749129 function calls in 2.501 seconds

   Ordered by: cumulative time
   List reduced from 69 to 15 due to restriction <15>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    2.501    2.501 /Users/yiwei/CL_M1/CL_M1_S2/Professional Skills/LAB4/src/sequential.py:7(run_sequential)
       50    0.006    0.000    2.350    0.047 /Users/yiwei/CL_M1/CL_M1_S2/Professional Skills/LAB4/src/text_processing.py:61(count_file)
       50    0.083    0.002    2.220    0.044 /Users/yiwei/CL_M1/CL_M1_S2/Professional Skills/LAB4/src/text_processing.py:57(count_text)
       50    0.001    0.000    1.497    0.030 /Users/yiwei/CL_M1/CL_M1_S2/Professional Skills/LAB4/src/text_processing.py:53(tokenize)
       50    1.339    0.027    1.339    0.027 {method 'findall' of 're.Pattern' objects}
      101    0.079    0.001    0.790    0.008 /Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/collections/__init__.py:669(update)
       51    0.000    0.000    0.639    0.013 /Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/collections/__init__.py:595(__init__)
       50    0.639    0.013    0.639    0.013 {built-in method _collections._count_elements}
       50    0.157    0.003    0.157    0.003 {method 'lower' of 'str' objects}
        1    0.000    0.000    0.151    0.151 /Users/yiwei/CL_M1/CL_M1_S2/Professional Skills/LAB4/src/text_processing.py:65(merge_counts)
       50    0.000    0.000    0.084    0.002 /Users/yiwei/CL_M1/CL_M1_S2/Professional Skills/LAB4/src/text_processing.py:31(read_text)
       50    0.000    0.000    0.084    0.002 /Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/pathlib.py:1022(read_text)
       50    0.058    0.001    0.081    0.002 {method 'read' of '_io.TextIOWrapper' objects}
   744986    0.071    0.000    0.071    0.000 {method 'get' of 'dict' objects}
       50    0.026    0.001    0.040    0.001 /Users/yiwei/CL_M1/CL_M1_S2/Professional Skills/LAB4/src/text_processing.py:35(strip_gutenberg_boilerplate)
```
