    assert isinstance(dbs_instance.memory, DB)
    assert isinstance(dbs_instance.logs, DB)
    assert isinstance(dbs_instance.preprompts, DB)
    assert isinstance(dbs_instance.input, DB)
    assert isinstance(dbs_instance.workspace, DB)


def test_invalid_path():
    with pytest.raises(PermissionError):
        # Test with a path that will raise a permission error
        DB("/root/test")


def test_large_files(tmp_path):
    db = DB(tmp_path)
    large_content = "a" * (10**6)  # 1MB of data

    # Test write large files
    db["large_file"] = large_content

    # Test read large files
    assert db["large_file"] == large_content


def test_concurrent_access(tmp_path):
    import threading

    db = DB(tmp_path)

    num_threads = 10
    num_writes = 1000

    def write_to_db(thread_id):
        for i in range(num_writes):
            key = f"thread{thread_id}_write{i}"
            db[key] = str(i)

    threads = []
    for thread_id in range(num_threads):
        t = threading.Thread(target=write_to_db, args=(thread_id,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    # Verify that all expected data was written
    for thread_id in range(num_threads):
        for i in range(num_writes):
            key = f"thread{thread_id}_write{i}"
            assert key in db  # using __contains__ now