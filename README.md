#What Is It?
This is a script for bundling small Rust projects into a single file, to upload to CodinGame, by resolving empty mod declarations

#How Do I Use It?
Assuming you've got python3 installed correctly, you can just run the script (located at src/bundler.py in this repo), supplying a path to the source file containing your main method, a path to the file you want the bundled code to be saved into, and prefix for identifying include-guards as command line arguments.

I.e.:

```
python3 bundler.py -i/--input <main_file> -o/--output <output_file> -g/--guard-prefix <include_guard_prefix>
```
    
E.g.:

```
python3 bundler.py -i main.cpp -o bundled_code.cpp -g __INCLUDE_GUARD_
```

If you omit the input argument, it will print the bundled code to standard output.

If you omit the output, it will attempt to look for a `main.rs` file in the current directory, and, if found, will use that as the input file.

#What Isn't It?
This script is NOT a complete Rust parser, as such, there are some caveats:
- It doesn't (yet) support detecting conditional compilation flags to omit codeblocks when 'features' are not specified (This is a planned feature)
- It doesn't (yet) support reading the project's `Cargo.toml` to resolve crates you've written yourself. (This is a planned feature, but ONLY for crates with code stored locally on your computer)
- It only detects mod declarations that have ';' on the same line. For example, it detects `mod my_mod;` but not:
```
mod my_mod
;
```

#What Does It Actually Do, Though?
- Currently, it processes an input file, line my line, and looks for `mod <mod_name>;`/`pub mod <mod_name>;` declarations, then searches for the associated file in the same way that cargo/rustc does (either `<mod_name>.rs` or `<mod_name>/mod.rs`, searched in that order)
- When it finds a mod file, it recursively processes that file (and any mod declarations), then combines the contests of all discovered files into a single, bundled output.
- Tracks and preserves indentation, and auto-indents sub-mod contents for readability 

I haven't (yet) produced a proper set of tests for this script, but will do so soon, and include it into the repo to give more concrete examples of the way it behaves.

#TODO
This is a tentative to-do list of additional features I've considered, but have not yet implemented.

It is not intended to be a complete list. For a more concrete idea of future plans, see the issues section.
- Supply a build-script, and cargo-configuration detection support, so that bundling can be integrated into the build process for CG rust projects.
- Local crate detection, so that you can crate up and re-use common code snippets or DIY-libraries you use across multiple puzzles/games
- Conditional-compilation emulation (e.g. `#[cgf()]`/`--features`)
- More options, such as enabling/disabling crate detection
- Code minificiation (with varying levels of intensity)
- Optionally performing some preprocessing to improve code performance for games that require complex AI (and hopefully in doing so, bring rust's performance on CG closer to C++, as it should be)
- (Maybe) multi-line parsing to detect empty mod declarations that are language-compliant but currently missed by the script.
- (Maybe) Converting the script from Python3 into Rust, to integrate better with Rust's existing build-script tooling.

__Note:__ Some of these features may be conditional on CG giving the OK for them, particularly optimisations (I know that straight-up local compilation to achieve release-mode performance is forbidden, for example).

I'll implement these on an as-needed basis for my own use, or possibly if there are community requests for them.

Feel free to request additional features or report problems via the issues section of the repo. (or even implement changes yourself - pull-requests are welcome!)
