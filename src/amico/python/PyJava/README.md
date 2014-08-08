
First, build the library `libAmiCoPyJava.so` by calling `make`. The built
library will be put in `./build/libAmiCoPyJava.so`.

To run an agent, call `run.sh` and provide the agent name

    ./run.sh -agent DemoForwardAgent.py

The script `run.sh` will copy all the agents, as well as `libAmiCoPyJava.so`
and some other libraries, to `$ROOT/bin/AmiCoBuild/PyJava`, where `$ROOT` is
the root directory of the project (i.e. where you cloned the GitHub repo to).


Troubleshooting
---------------

Problem: "undefined symbol: JNI_CreateJavaVM"
Solution: This means that `libAmiCoPyJava.so` is not linking with `libjvm.so`.
    It is up to `AmiCoRunner.sh` to set `LD_LIBRARY_PATH` to include
    `libjvm.so` and the other Java libraries. On Darwin (MacOS), this script
    is not run, so it may be necessary to manually add `libjvm.so` to the
    library path. Calling `ldd` on the library can help debug linking problems,
    but make sure you check *after* `LD_LIBRARY_PATH` is set.
