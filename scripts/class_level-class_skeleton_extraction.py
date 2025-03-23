import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import os, ast, subprocess, re, autopep8, time
import numpy as np

path_to_data = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'data'))


def combine_understand_reports():
    report_file_list = []

    und_analysis_df = pd.read_csv(f"{path_to_data}/metadata_folder/file_mapping_with_analysis_status.csv") # read this df for filtering out the projects that exists on GitHub
    und_analysis_df = und_analysis_df[und_analysis_df['analysis_status'] == 'Successfull'] # keeping the ones that the "Successfull" status

    for idx, row in und_analysis_df.iterrows():
        tmp_df = pd.read_csv(f"{path_to_data}/Understand_analysis_reports/{row['expected_analysis_report_file']}",
                             low_memory=False)
        tmp_class_df = tmp_df[tmp_df['Kind'] == "Class"] # Keeping only the rows from the analysis report that represent a class
        tmp_class_df['report_file_name'] = [row['expected_analysis_report_file']] * tmp_class_df.shape[0]
        tmp_class_df['repo_name'] = [row['repo_name']] * tmp_class_df.shape[0]
        report_file_list.append(tmp_class_df)

    analysis_report_df = pd.concat(report_file_list, axis=0) # combining all_files class-level reports into one df

    print(f"Total number of classes to be processed is {analysis_report_df.shape[0]}")

    return analysis_report_df

def snippet_cleaning(raw_snippet):
    leading_spaces = len(raw_snippet) - len(raw_snippet.lstrip())
    if leading_spaces == 0:
        clean_snippet = raw_snippet
    else:
        clean_snippet = ""
        for line in raw_snippet.split("\n"):
            clean_snippet += line[leading_spaces:] + "\n"
    return clean_snippet


def extract_relevant_code_snippets(code, class_to_extract):
    tree = ast.parse(code)

    # adding parent info
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

    relevant_snippet_with_parent_list = []

    for node in ast.walk(tree):
        if type(node).__name__ == "ClassDef":
            if node.name == class_to_extract:
                try:
                    parent = node.parent.name
                except:
                    parent = None
                relevant_snippet_with_parent_list.append((ast.get_source_segment(code, node, padded=True), parent))

    if len(relevant_snippet_with_parent_list) == 1:
        return snippet_cleaning(relevant_snippet_with_parent_list[0][0])

    else:
        cleaned_snippet_parent_list = []
        for snippet_parent_pair in relevant_snippet_with_parent_list:
            snippet, parent = snippet_parent_pair
            cleaned_snippet_parent_list.append(
                (snippet_cleaning(snippet), parent)
            )
        return cleaned_snippet_parent_list


def extract_skeleton(class_code_snippet):
    class_signatures = [match.group() for matchNum, match in enumerate(
        re.finditer(r"^\s*class\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(*[\s\S]*?\)*[\s\S]*?:",
                    class_code_snippet, re.MULTILINE),
        start=1)]
    func_signatures = [match.group() for matchNum, match in enumerate(
        re.finditer(r"^\s*(?:async\s+)?def\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\([\s\S]*?\)[\s\S]*?:",
                    class_code_snippet, re.MULTILINE),
        start=1)]
    tree = ast.parse(class_code_snippet)
    skeleton_dict = {}
    for node in ast.walk(tree):
        if type(node).__name__ == "ClassDef":
            sub_skeleton = ""
            code_segment = [signature for signature in class_signatures if "class " + node.name in signature][0]
            leading_spaces = len(code_segment) - len(code_segment.lstrip(" "))
            sub_skeleton += code_segment + "\n"
            if ast.get_docstring(node, clean=False) is not None:
                docstring = "\t'''"
                docstring += ast.get_docstring(node, clean=False) + "'''"
                sub_skeleton += docstring
            sub_skeleton += "\n"
            skeleton_dict[node.lineno] = sub_skeleton
            if len(node.decorator_list) > 0:
                for dec in node.decorator_list:
                    skeleton_dict[dec.lineno] = (" " * leading_spaces) + "@" + ast.get_source_segment(
                        class_code_snippet, dec, padded=False)

        if type(node).__name__ == "FunctionDef" or type(node).__name__ == "AsyncFunctionDef":
            sub_skeleton = ""
            code_segment = [signature for signature in func_signatures if "def " + node.name in signature][0]
            leading_spaces = len(code_segment) - len(code_segment.lstrip(" "))
            sub_skeleton += code_segment + "\n"
            if ast.get_docstring(node, clean=False) is not None:
                docstring = "\t'''"
                docstring += ast.get_docstring(node, clean=False) + "'''"
                sub_skeleton += docstring + "\n\t"
            sub_skeleton += "pass\n"
            skeleton_dict[node.lineno] = sub_skeleton
            if len(node.decorator_list) > 0:
                for dec in node.decorator_list:
                    skeleton_dict[dec.lineno] = (" " * leading_spaces) + "@" + ast.get_source_segment(
                        class_code_snippet, dec, padded=False)

    skeleton = ""
    docstr_counter = 0
    for key, value in dict(sorted(skeleton_dict.items())).items():
        skeleton += value + "\n"
        if "\t'''" in value:
            docstr_counter += 1
    if len(skeleton_dict) == 1:
        skeleton += "\tpass"
    return skeleton, len(skeleton_dict), docstr_counter


def class_skeleton_extractor():
    full_class_df = combine_understand_reports()
    unique_projects = full_class_df['repo_name'].unique()
    full_data_list = []
    fail_counter = 0
    fail_log_dict = {}
    successful_process_logger = open(f"{path_to_data}/metadata_folder/skeleton_extraction_success.log", 'a')
    successful_process_logger.write("repo,number_classes,number_of_processed_classes\n")
    for repo in unique_projects:
        success_counter = 0
        proj_df = full_class_df[full_class_df["repo_name"] == repo]
        proj_df.drop_duplicates(keep='last', inplace=True)
        repo_folder = repo.replace("/", "_")
        subprocess.run(f"git clone https://github.com/{repo}.git {path_to_data}/git_repos_for_analysis/{repo_folder}",
                       shell=True)
        for idx, row in proj_df.iterrows():
            proj_data_list = [row['repo_name'], row['File'], row['Name'], row['RatioCommentToCode']]
            try:
                f = open(row['File'], 'r')
                code = autopep8.fix_code(f.read())
                f.close()
                relevant_code_snippets = extract_relevant_code_snippets(
                    code, class_to_extract=row['Name'].split(".")[-1])
                human_written_code = ""
                if isinstance(relevant_code_snippets, str):
                    human_written_code = relevant_code_snippets
                else:
                    for snippet_parent in relevant_code_snippets:
                        if snippet_parent[1] == row['Name'].split(".")[-2]:
                            human_written_code = snippet_parent[0]
                proj_data_list.append(human_written_code)
                skeleton, total_prog_units, total_docstr = (extract_skeleton(human_written_code))
                proj_data_list.append(skeleton)
                proj_data_list.append(total_prog_units)
                proj_data_list.append(total_docstr)
                success_counter += 1
                print(f"Class {row['Name']} -> Successful.")
            except Exception as e:
                print(f"Class {row['Name']} -> Unsuccessful.")
                fail_counter += 1
                fail_log_dict[fail_counter] = (row['repo_name'], row['File'], row['Name'], repr(e))

            if len(proj_data_list) == 8:
                full_data_list.append(proj_data_list)
        subprocess.run(f"rm -rf {path_to_data}/git_repos_for_analysis/{repo_folder}", shell=True)
        successful_process_logger.write(f"{repo},{full_class_df[full_class_df['repo_name'] == repo].shape[0]},{success_counter}\n")
        time.sleep(1)


    if len(fail_log_dict) > 0:
        error_file = open(f"{path_to_data}/metadata_folder/skeleton_extraction_failures.log", "a")
        for key, value in fail_log_dict.items():
            error_file.write(f"{key}: {value}\n")
        error_file.close()
    successful_process_logger.close()
    return pd.DataFrame(full_data_list, columns = ['repo_name', 'File', 'Name', 'RatioCommentToCode', 'human_written_code', 'code_skeleton',
                                     'total_program_units', 'total_doc_str']).drop_duplicates(subset=['human_written_code'], keep='last')


if __name__ == "__main__":
    """Main entry point for extracting and saving class skeletons."""
    skeleton_df = class_skeleton_extractor()
    print(skeleton_df.shape)
    print(skeleton_df.columns)

    for col in skeleton_df.columns:
        if skeleton_df[col].dtype == object:
            skeleton_df[col] = skeleton_df[col].apply(
                lambda x: np.nan if x == np.nan else str(x).encode('utf-8', 'replace').decode('utf-8'))
    skeleton_df.to_csv(f"{path_to_data}/metadata_folder/extracted_class_skeletons.csv", index=False)
