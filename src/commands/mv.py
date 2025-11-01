from shutil import Error as PathAlreadyExistsError
from argparse import ArgumentParser, ArgumentError
from src.commands.history import cmd_history
from src.errors import (
    path_doesnt_exist_message,
    missing_required_arguments_message,
    unknown_arguments_message,
    permission_denied_message,
    src_and_dst_are_the_same_message,
)


class Mv:
    "'mv' command to read file contents"

    def __init__(self) -> None:
        parser = ArgumentParser(
            prog="mv",
            description="Move file or folder from source to destination, rename file or folder",
            exit_on_error=False,
        )
        parser.add_argument(
            "src", help="Source of file or folder to move from or rename"
        )
        parser.add_argument(
            "dst", help="Destination of file or folder to move where or new name"
        )
        self.parser = parser

    def execute(self, cwd: str | None, _args: list[str]) -> None:
        """
        Execute 'mv' command from given directory with given args
        Args:
            cwd (str): directory to execute from
            _args (list[str]): args for 'mv' command
        """
        from src import remove, isabs, isdir, Path, move, copytree, rmtree

        try:
            args, unknown_args = self.parser.parse_known_args(args=_args)
        except ArgumentError as e:
            missing_args = e.message[e.message.index(":") + 2 :]
            missing_required_arguments_message(missing_args_str=missing_args)
            return

        if len(unknown_args) > 0:
            unknown_arguments_message(unknown_args=unknown_args)

        # if cwd is not None, command executed from Terminal3000 class
        # if cwd is None, command executed from Undo class, given path already absolute
        if cwd:
            srcpath = str(
                Path(args.src if isabs(args.src) else f"{cwd}/{args.src}").resolve()
            )
            dstpath = str(
                Path(args.dst if isabs(args.dst) else f"{cwd}/{args.dst}").resolve()
            )
        else:
            srcpath = str(Path(args.src))
            dstpath = str(Path(args.dst))
        if not Path(srcpath).exists():
            path_doesnt_exist_message(path=srcpath)
            return

        try:
            dstpath = move(src=srcpath, dst=dstpath)
            if cwd:
                cmd_history.write(cmd=f"mv {srcpath} {dstpath}")
        except PermissionError:
            permission_denied_message(srcpath, dstpath)
        except PathAlreadyExistsError:
            # Check is paths lead to the same file
            real_src_path = srcpath[: srcpath.rindex("\\")]
            real_dst_path = dstpath.rstrip("\\")
            if real_src_path == real_dst_path:
                src_and_dst_are_the_same_message(path=srcpath)
                return

            filename = srcpath.split("\\")[-1]
            dstpath = f"{dstpath}/{filename}"
            if isdir(dstpath):
                # Need cause of move() command can't move to directory already existing
                copytree(
                    src=srcpath,
                    dst=dstpath,
                    dirs_exist_ok=True,
                )
                rmtree(path=srcpath)
            else:
                # In selected dir this file already exists, replacing it
                remove(path=dstpath)
                move(src=srcpath, dst=dstpath)

            if cwd:
                cmd_history.write(cmd=f"mv {srcpath} {dstpath}")


cmd_mv = Mv()
