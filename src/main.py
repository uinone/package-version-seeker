import argparse
from .info import RequiredModules

def parse_arguments():
    parser = argparse.ArgumentParser(description="Get required modules safe versions!")
    parser.add_argument('project_name', help='target project name.       ex) mmdet3d')
    parser.add_argument('project_version', help='target project version. ex) 0.17.0')
    parser.add_argument('req_path', help='target requirement.txt path.   ex) ./new_reqirement.txt')
    parser.add_argument('--show-output', action='store_true', help='If {--show-output} is exist, pvs just print output.')
    parser.add_argument('--export-path', help='export pretty requirement.txt to {export_path}. Default path is same with {req_path}')

    return parser.parse_args()

def main():
    args = parse_arguments()

    req_modules = RequiredModules.get_requirement_text(
        path=args.req_path,
        target_project=args.project_name,
        target_project_version=args.project_version
    )

    if args.show_output == False:
        args.export_path = args.export_path if args.export_path is not None else args.req_path

        req_modules.export(args.export_path)
        outp = f"Export pretty requirement.txt to '{args.export_path}' successfully  "
        print("\n[SUCCESS]")
        print("="*len(outp))
        print(outp)
        print("="*len(outp))
    else:
        print("\n[OUTPUT]")
        info_width = max([len(info) for info in req_modules.__repr__().split("\n")]) + 2
        print("="*info_width)
        print(req_modules)
        print("="*info_width)
