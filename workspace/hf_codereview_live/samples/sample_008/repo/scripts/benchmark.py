                    bench_folder,
                    "--steps",
                    "benchmark",
                ],
                stdout=log_file,
                stderr=log_file,
                bufsize=0,
            )
            benchmarks.append((bench_folder, process, log_file))

            print("You can stream the log file by running:")
            print(f"tail -f {log_path}")
            print()

    for bench_folder, process, file in benchmarks:
        process.wait()
        file.close()

        print("process", bench_folder.name, "finished with code", process.returncode)
        print("Running it. Original benchmark prompt:")
        print()
        with open(bench_folder / "main_prompt") as f:
            print(f.read())
        print()

        with contextlib.suppress(KeyboardInterrupt):
            subprocess.run(
                [
                    "python",
                    "-m",
                    "gpt_engineer.main",
                    bench_folder,
                    "--steps",
                    "execute_only",
                ],
            )


if __name__ == "__main__":
    run(main)
