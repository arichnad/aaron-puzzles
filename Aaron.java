
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentSkipListSet;


public class Aaron {
	private Board board = new Board();

	public static class Board {
		private char[][] board = new char[4][4];
		private Set<Position> allOpenPositions = new ConcurrentSkipListSet<Position>();
		private Map<Character,Set<Position>> boardLetter = new HashMap<Character, Set<Position>>(30);
		public char charAt(Position position) {
			return board[position.y][position.x];
		}
		public Board() {
			for(char c='a';c<='z';c++) {
				boardLetter.put(c, new ConcurrentSkipListSet<Position>());
			}
			allOpenPositions.addAll(Position.getAllPositions());
		}
		public int countPlacedWord(String word, int pos) {
			if(pos==word.length()) {
				System.out.println(toString());
				return 1;
			}
			char letter=word.charAt(pos);
			int count=0;
			for(Position position : allOpenPositions) {
				allOpenPositions.remove(position);
				count+=countPlacedWord(word, pos+1);
				allOpenPositions.add(position);
			}
			Set<Position> positionSet = boardLetter.get(letter);
			for(Position position : positionSet) {
				positionSet.remove(position);
				count+=countPlacedWord(word, pos+1);
				positionSet.add(position);
			}
			return count;
		}
		@Override
		public String toString() {
			String out="";
			for(y=0;y<4;y++) {
				for(x=0;x<4;x++) {
					out+=board[y][x]==0?' ':board[y][x];
				}
				out+='\n';
			}
			return out;
		}
	}

	public static class PlacedWord {
		private String word;
		private Set<Position> positions;
		/*
		public boolean fitsBoard(Board board) {
			int i=0;
			for(Position position : positions) {
				if(board.charAt(position)!=word.charAt(i++)) {
					return false;
				}
			}
			return true;
		}
		*/
	}

	public static class Position implements Comparable<Position> {
		private int x, y;
		private static Set<Position> allPositions = new HashSet<Position>(20);
		static {
			for(int y=0;y<4;y++) for(int x=0;x<4;x++) {
				Position position = new Position();
				position.x=x; position.y=y;
				allPositions.add(position);
			}
		}
		public static Set<Position> getAllPositions() {
			return allPositions;
		}
		@Override
		public int compareTo(Position o) {
			return y==o.y?x-o.x:y-o.y;
		}
	}

	public static void main(String[] args) {
		Aaron aaron = new Aaron();
		System.out.println(aaron.board.countPlacedWord("test", 0));
		for(int i=0;i<10000;i++) {
			aaron.board.countPlacedWord("test", 0);
		}
	}
}

