#!/usr/bin/python3
import argparse
import os.path
import re

DEFAULT_INPUT_FILEPATH = 'main.rs'
###launch the argument parser for a proper cli experience
parser = argparse.ArgumentParser(description='A script for bundling small Rust projects into a single file, to upload to CodinGame, by resolving empty mod declarations')
parser.add_argument(
    '-i',
    '--input',
    help='A path to the file to start reading from (this should typically be the file containing your main() method). Defaults to \'main.cpp\' if omitted'
)
parser.add_argument(
    '-o',
    '--output',
    help='A path to the file to save the bundled code to. The bundler will print the code to standard output if this is omitted'
)

arguments = parser.parse_args()
inputFilePath = arguments.input or DEFAULT_INPUT_FILEPATH
outputFilePath = arguments.output

INDENT_STRING = '    '

#this is just a stub for now, needs TOML support to do properly, also the extern may not actually be mandatory in rust, need to check
def processLocalCrateUse(line, curIndent = ''):
    localCratePaths = {'phys2d': '/mnt/shared-drive/archy/git/coding-game/common/phys2d', 'cg_generic_traits': '/mnt/shared-drive/archy/git/coding-game/common/cg_generic_traits'}
    crateUse = re.search('^(\s*)?extern crate \w+;', line);
    result = ''
    if crateUse is not None:
        cwd = os.getcwd()
        modName = crateUse.group(0).split('extern crate ')[1].split(';')[0]
    
        cratePath = localCratePaths[modName]
        os.chdir('%s/src' % cratePath)
        with open('./lib.rs', 'r') as libFile:
            # for line in libFile.readlines():
            #     print(line)
            modContents = scan(libFile, curIndent+'\t')
    
        result += "%s%s mod %s {\n%s\n%s}" % (curIndent, 'pub', modName, modContents, curIndent)
    
        os.chdir(cwd)
        return result
    else:
        return None

def processMod(line, curIndent = ''):
    mod = re.search('^(\s*)?(pub )?mod \w+;', line)
    if mod is not None:
        publicity, modName = mod.group(0).split('mod ')
        publicity = publicity.strip()
        modName = modName.split(';')[0].strip()
        modContents = ''
        if os.path.isfile('./%s.rs' % modName):
            with open('./%s.rs' % modName, 'r') as subFile:
                modContents = scan(subFile, curIndent+INDENT_STRING)
        else:
            os.chdir('./%s' % modName);
            with open('./mod.rs', 'r') as subFile:
                modContents = scan(subFile, curIndent+INDENT_STRING)
            os.chdir('..')
        return "%s%s mod %s {\n%s\n%s}" % (curIndent, publicity, modName, modContents, curIndent)
    else:
        return None

def scan(file, curIndent = ''):
    result = ""
    for line in file.readlines():
        temp = processLocalCrateUse(line)
        if temp is not None:
            #do crate stuff, this will need to change when crates detection is implemented
            result += curIndent + temp
            continue

        temp = processMod(line, curIndent)
        if temp is not None:
            result += curIndent + temp
            continue
        result += curIndent + line
    return result

#process the initial input file path, moving to to the appropriate path if neccessary
oldWorkingDirectory = os.getcwd()
lastDirSepPos = inputFilePath.rfind('/')
if lastDirSepPos == -1:
    lastDirSepPos = inputFilePath.rfind('\\')
if lastDirSepPos != -1:
    inputPath, inputFileName = inputFilePath[0:lastDirSepPos], inputFilePath[lastDirSepPos+1:]
    os.chdir(inputPath)
else:
    inputFileName = inputFilePath
#now scan the file
with open(inputFileName, 'r') as inputFile:
    result = scan(inputFile)

#now jump back to the initial directory
os.chdir(oldWorkingDirectory)
if outputFilePath is not None:
    with open(outputFilePath, 'w') as outFile:
        outFile.write(result)
else:
    print(result)