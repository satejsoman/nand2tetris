#!/bin/bash 

set -e

echo "TESTING: ArrayTest/Main.jack"
python3 /Users/satej/Documents/workspace/classwork/compsys/n2trepo/project10/src/parser.py /Users/satej/Documents/workspace/classwork/compsys/nand2tetris/projects/10/ArrayTest/Main.jack 
/Users/satej/Documents/workspace/classwork/compsys/nand2tetris/tools/TextComparer.sh /Users/satej/Documents/workspace/classwork/compsys/nand2tetris/projects/10/ArrayTest/Main.xml /Users/satej/Documents/workspace/classwork/compsys/nand2tetris//projects/10/ArrayTest/Main.ref.xml


echo "TESTING: ExpressionLessSquare/Main.jack"
python3 /Users/satej/Documents/workspace/classwork/compsys/n2trepo/project10/src/parser.py /Users/satej/Documents/workspace/classwork/compsys/nand2tetris/projects/10/ExpressionLessSquare/Main.jack
/Users/satej/Documents/workspace/classwork/compsys/nand2tetris/tools/TextComparer.sh /Users/satej/Documents/workspace/classwork/compsys/nand2tetris/projects/10/ExpressionLessSquare/Main.xml /Users/satej/Documents/workspace/classwork/compsys/nand2tetris//projects/10/ExpressionLessSquare/Main.ref.xml

echo "TESTING: ExpressionLessSquare/Square.jack"
python3 /Users/satej/Documents/workspace/classwork/compsys/n2trepo/project10/src/parser.py /Users/satej/Documents/workspace/classwork/compsys/nand2tetris/projects/10/ExpressionLessSquare/Square.jack
/Users/satej/Documents/workspace/classwork/compsys/nand2tetris/tools/TextComparer.sh /Users/satej/Documents/workspace/classwork/compsys/nand2tetris/projects/10/ExpressionLessSquare/Square.xml /Users/satej/Documents/workspace/classwork/compsys/nand2tetris//projects/10/ExpressionLessSquare/Square.ref.xml

echo "TESTING: ExpressionLessSquare/SquareGame.jack"
python3 /Users/satej/Documents/workspace/classwork/compsys/n2trepo/project10/src/parser.py /Users/satej/Documents/workspace/classwork/compsys/nand2tetris/projects/10/ExpressionLessSquare/SquareGame.jack
/Users/satej/Documents/workspace/classwork/compsys/nand2tetris/tools/TextComparer.sh /Users/satej/Documents/workspace/classwork/compsys/nand2tetris/projects/10/ExpressionLessSquare/SquareGame.xml /Users/satej/Documents/workspace/classwork/compsys/nand2tetris//projects/10/ExpressionLessSquare/SquareGame.ref.xml


echo "TESTING: Square/Main.jack"
python3 /Users/satej/Documents/workspace/classwork/compsys/n2trepo/project10/src/parser.py /Users/satej/Documents/workspace/classwork/compsys/nand2tetris/projects/10/Square/Main.jack
/Users/satej/Documents/workspace/classwork/compsys/nand2tetris/tools/TextComparer.sh /Users/satej/Documents/workspace/classwork/compsys/nand2tetris/projects/10/Square/Main.xml /Users/satej/Documents/workspace/classwork/compsys/nand2tetris//projects/10/Square/Main.ref.xml

echo "TESTING: Square/Square.jack"
python3 /Users/satej/Documents/workspace/classwork/compsys/n2trepo/project10/src/parser.py /Users/satej/Documents/workspace/classwork/compsys/nand2tetris/projects/10/Square/Square.jack
/Users/satej/Documents/workspace/classwork/compsys/nand2tetris/tools/TextComparer.sh /Users/satej/Documents/workspace/classwork/compsys/nand2tetris/projects/10/Square/Square.xml /Users/satej/Documents/workspace/classwork/compsys/nand2tetris//projects/10/Square/Square.ref.xml

echo "TESTING: Square/SquareGame.jack"
python3 /Users/satej/Documents/workspace/classwork/compsys/n2trepo/project10/src/parser.py /Users/satej/Documents/workspace/classwork/compsys/nand2tetris/projects/10/Square/SquareGame.jack
/Users/satej/Documents/workspace/classwork/compsys/nand2tetris/tools/TextComparer.sh /Users/satej/Documents/workspace/classwork/compsys/nand2tetris/projects/10/Square/SquareGame.xml /Users/satej/Documents/workspace/classwork/compsys/nand2tetris//projects/10/Square/SquareGame.ref.xml