cd ..
py -m src.file_comparator.main --base_dir=%cd%/run_scripts/ --start_at=file_differences %*
cmd \k