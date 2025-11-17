# OpenClassGen
A Large-Scale Dataset from Open-Source Projects for Class-Level Code Generation (Replication package)

### 📘 Data Dictionary for the Curated Class-level Dataset

| **Field** | **Description** |
|-----------|-----------------|
| `id` | A unique identifier for each data point, starting from 0. |
| `repository_name` | Name of the GitHub repository from which the class was extracted. |
| `file_path` | Full path to the file containing the class within the repository. |
| `class_name` | Name of the class defined in the corresponding file. |
| `human_written_code` | Full source code of the human-written class, including all docstrings. |
| `class_skeleton` | Extracted skeleton of the class, including class and method signatures along with associated docstrings (if present). |
| `total_program_units` | Total number of program units (i.e., classes and methods) within the class skeleton. |
| `total_doc_str` | Number of program units in the class skeleton that contain associated docstrings. |
| `AvgCountLine` | Average number of lines per class. |
| `AvgCountLineBlank` | Average number of blank lines per class. |
| `AvgCountLineCode` | Average number of code lines per class (excluding comments and blanks). |
| `AvgCountLineComment` | Average number of comment lines per class. |
| `AvgCyclomatic` | Average cyclomatic complexity across methods in the class. |
| `CommentToCodeRatio` | Ratio of comment lines to code lines in the class. |
| `CountClassBase` | Number of base classes (i.e., direct superclasses). |
| `CountClassCoupled` | Number of other classes referenced (coupled) by this class. |
| `CountClassCoupledModified` | Number of coupled classes after removing standard library dependencies. |
| `CountClassDerived` | Number of classes that inherit from this class. |
| `CountDeclInstanceMethod` | Number of instance methods declared in the class. |
| `CountDeclInstanceVariable` | Number of instance variables declared in the class. |
| `CountDeclMethod` | Number of methods declared in the class (excluding inherited ones). |
| `CountDeclMethodAll` | Total number of declared methods, including inherited ones. |
| `CountLine` | Total number of lines in the class. |
| `CountLineBlank` | Number of blank lines in the class. |
| `CountLineCode` | Number of executable code lines in the class. |
| `CountLineCodeDecl` | Number of declaration lines in the class. |
| `CountLineCodeExe` | Number of executable statement lines in the class. |
| `CountLineComment` | Number of comment lines in the class. |
| `CountStmt` | Total number of statements in the class. |
| `CountStmtDecl` | Number of declaration statements in the class. |
| `CountStmtExe` | Number of executable statements in the class. |
| `MaxCyclomatic` | Maximum cyclomatic complexity among all methods in the class. |
| `MaxInheritanceTree` | Maximum depth of the class in the inheritance hierarchy. |
| `MaxNesting` | Maximum level of nested control structures in the class. |
| `SumCyclomatic` | Sum of cyclomatic complexity across all methods in the class. |
