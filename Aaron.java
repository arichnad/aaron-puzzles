
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.CopyOnWriteArrayList;


public class Aaron {
	public interface Callback {
		void run(int wordNum);
	}
	private Board board = new Board();

	public class Board {
		private final Set<Integer> finishedBoards = new HashSet<Integer>();
		private static final int ALREADY_USED = -1000;
		private char[][] board = new char[4][4];
		private int[][] used = new int[4][4];
		private Collection<Position> allOpenPositions = new CopyOnWriteArrayList<Position>();
		private Map<Character,Collection<Position>> boardLetter = new HashMap<Character, Collection<Position>>(30);
		/*
		public char charAt(Position position) {
			return board[position.y][position.x];
		}
		*/
		public void setChar(Position position, char ch) {
			/*
			if(ch==0&&board[position.y][position.x]==0||ch!=0&&board[position.y][position.x]!=0) {
				throw new IllegalStateException();
			}
			*/
			board[position.y][position.x]=ch;
		}
		public Board() {
			for(char c='a';c<='z';c++) {
				boardLetter.put(c, new CopyOnWriteArrayList<Position>());
			}
			for(Position position : Position.getAllPositions()) {
				setUsed(position, -1);
			}
			allOpenPositions.addAll(Position.getAllPositions());
		}
		/*
		public int countPlacedWord(String word, int pos, Position last) {
			if(pos==word.length()) {
				return 1;
			}
			char letter=word.charAt(pos);
			Collection<Position> positionCollection = boardLetter.get(letter);

			int count=0;
			for(Position position : allOpenPositions) {
				if(!last.isConnected(position)) {
					continue;
				}
				allOpenPositions.remove(position);
				count+=countPlacedWord(word, pos+1, position);
				allOpenPositions.add(position);
			}
			for(Position position : positionCollection) {
				if(!last.isConnected(position)) {
					continue;
				}
				positionCollection.remove(position);
				count+=countPlacedWord(word, pos+1, position);
				positionCollection.add(position);
			}
			return count;
		}
		*/
		public int setUsed(Position position, int wordNum) {
			int old=used[position.y][position.x];
			if(old==wordNum) {
				return ALREADY_USED;
			}
			used[position.y][position.x]=wordNum;
			return old;
		}
		public boolean recurse(int wordNum, String word, int pos, Position last, boolean findOne) {
			//System.out.println(wordNum + ", " + pos);
			if(pos==word.length()) {
				callback.run(wordNum+1);
				return true;
			}
			char letter=word.charAt(pos);
			Collection<Position> positionCollection = boardLetter.get(letter);
			
			/*
			//check if we've already seen this one
			if(finishedBoards.size()>0 && finishedBoards.contains(hashCode())) {
			return true;
			}
			 */
			for(Position position : allOpenPositions) {
				if(findOne) {
					throw new IllegalStateException();
				}
				if(wordNum<=0) {System.out.println("###\n"+this);}
				if(last!=null&&!last.isConnected(position)) {
					continue;
				}
				int oldUsed = setUsed(position, wordNum);
				if(oldUsed==ALREADY_USED) {
					continue;
				}
				allOpenPositions.remove(position);
				setChar(position, letter);
				positionCollection.add(position);
				recurse(wordNum, word, pos+1, position, false);
				allOpenPositions.add(position);
				setChar(position, (char)0);
				positionCollection.remove(position);
				setUsed(position, oldUsed);
				//if(wordNum==0 && pos==0) {break;}
			}
			for(Position position : positionCollection) {
				if(last!=null&&!last.isConnected(position)) {
					continue;
				}
				int oldUsed = setUsed(position, wordNum);
				if(oldUsed==ALREADY_USED) {
					continue;
				}
				boolean found = recurse(wordNum, word, pos+1, position, findOne);
				/*
				if(found && findOne) {
					return true;
				}
				*/
				setUsed(position, oldUsed);
			}
			return false;
		}
		@Override
		public String toString() {
			String out="";
			for(int y=0;y<4;y++) {
				for(int x=0;x<4;x++) out+=board[y][x]==0?' ':board[y][x];
				out+='\n';
			}
			return out;
		}

		@Override
		public int hashCode() {
			int out=0;
			for(int y=0;y<4;y++) {
				for(int x=0;x<4;x++) {
					out=out*31+((int)(board[y][x]-'a'));
				}
			}
			return out;
		}
	}

	public static class Position implements Comparable<Position> {
		private int x, y;
		private static Collection<Position> allPositions = new HashSet<Position>(20);
		private static Position dummyPosition = new Position() {
			@Override
			public boolean isConnected(Position o) {return true;}
		};
		static {
			for(int y=0;y<4;y++) for(int x=0;x<4;x++) {
				Position position = new Position();
				position.x=x; position.y=y;
				allPositions.add(position);
			}
		}
		public static Collection<Position> getAllPositions() {
			return allPositions;
		}
		public static Position getDummyPosition() {
			return dummyPosition;
		}
		public boolean isConnected(Position o) {
			int dx=x-o.x,dy=y-o.y;
			return (dx==-1||dx==0||dx==1)&&(dy==-1||dy==0||dy==1);
		}
		@Override
		public int compareTo(Position o) {
			return y==o.y?x-o.x:y-o.y;
		}
		@Override
		public String toString() {
			return y + ", " + x;
		}
		//not needed, really just needed for repeatability
		@Override
		public int hashCode() {
			return y*4+(x+2)%4;
		}
	}
	private String[] words = new String[] { "assorters", "assessor", "assorter", "snorters", "sporters", "asserts", "assorts",
                                "porters", "possess", "possets", "posters", "rosters", "sardars", "sarsars", "serosas", "sirdars", "snorers",
                                "snorter", "sorters", "sporter", "arsons", "assais", "assert", "assess", "assets", "assort", "darers", "porter",
                                "posers", "posses", "posset", "poster", "rasers", "resort", "retros", "roster", "sardar", "sarsar", "sasses",
                                "serosa", "sirdar", "snorer", "snores", "snorts", "sonars", "sorest", "sorter", "spores", "sports", "stress",
                                "strops", "tronas", "tsores", "arses", "arson", "assai", "asses", "asset", "darer", "dares", "dress", "drest",
                                "nards", "naris", "noses", "ossia", "pores", "ports", "poser", "poses", "posse", "raser", "rases", "retro",
                                "roses", "roset", "sards", "saris", "snore", "snort", "sonar", "sorer", "sores", "sorts", "spore", "sport",
                                "strop", "tress", "trona", "airs", "ares", "arse", "dare", "eras", "eros", "erst", "nard", "nose", "ores",
                                "orts", "osar", "oses", "ossa", "pons", "pore", "port", "pose", "post", "psst", "rads", "rase", "rasp", "rest",
                                "rets", "rias", "rose", "sans", "sard", "sari", "sass", "sera", "sers", "sets", "sirs", "sons", "sops", "sore",
                                "sort", "sris", "trop", "ads", "air", "ais", "are", "ars", "asp", "ass", "era", "ers", "ess", "nor", "nos", "ons",
                                "ops", "ore", "ors", "ort", "ose", "rad", "ran", "ras", "res", "ret", "ria", "sad", "ser", "set", "sir", "son",
                                "sop", "sos", "sri", "ad", "ai", "an", "ar", "as", "er", "es", "et", "is", "na", "no", "on", "op", "or", "os",
                                "re", "si", "so" };
	/*
	private String[] words = new String[] {
		"reindeers", "beadiest", "bedstead", "breading", "debaters", "digester", "dingiest", "readiest", "rebaters", "redigest",
		"reindeer", "steadied", "beading", "beaters", "berates", "braided", "breaded", "dabster", "debased", "debaser",
		"debater", "debates", "deraign", "derates", "destain", "diaster", "diester", "dingies", "edgiest", "ideates",
		"ingesta", "readied", "readies", "reading", "rebater", "rebates", "redates", "reedier", "reeding", "sabeing",
		"sedater", "sedgier", "seedier", "seeding", "staider", "steaded", "treaded", "aiding", "badged", "badges",
		"baster", "beaded", "beater", "beiges", "berate", "braids", "breads", "breast", "bredes", "daters",
		"deader", "debase", "debate", "derate", "derats", "desert", "digest", "dinged", "dinges", "easter",
		"eaters", "edgier", "erased", "eraser", "geared", "ideate", "indies", "ingest", "raided", "raster",
		"raters", "rebate", "redate", "rediae", "redias", "reding", "resaid", "reseat", "reseda", "retain",
		"sabred", "seabed", "seared", "seater", "sedate", "seeder", "stadia", "stared", "teased", "aedes",
		"aided", "aider", "aides", "aster", "badge", "bared", "based", "baser", "baste", "bates",
		"beads", "beast", "beats", "beige", "being", "brads", "braes", "braid", "brain", "brats",
		"bread", "brede", "darbs", "dater", "dates", "deads", "debar", "debts", "deers", "deets",
		"deign", "derat", "didie", "didst", "dinge", "eared", "eased", "eater", "edged", "edges",
		"eider", "erase", "ester", "geest", "geste", "ideas", "indie", "nided", "nides", "raids",
		"rased", "raser", "rater", "rates", "reads", "reded", "redes", "redia", "redid", "reeds",
		"reest", "reign", "sabed", "saber", "sabre", "seder", "segni", "setae", "stade", "staid",
		"staig", "stain", "stare", "stead", "steed", "taber", "tared", "tease", "terse", "tread",
		"treed", "trees", "tsade", "tsadi", "abed", "aide", "aids", "arbs", "asea", "ates",
		"bade", "bads", "bare", "base", "bast", "bate", "bats", "bead", "bear", "beat",
		"beds", "brad", "brae", "bras", "brat", "bred", "dabs", "darb", "dare", "date",
		"dead", "dear", "debs", "debt", "deer", "dees", "deet", "died", "dies", "ding",
		"ease", "east", "eats", "edge", "eide", "eras", "erst", "etas", "gear", "geds",
		"gees", "gest", "gids", "gied", "gies", "idea", "ides", "nide", "nidi", "rads",
		"raid", "rain", "rase", "rate", "rats", "read", "rebs", "rede", "reds", "reed",
		"rees", "rein", "rest", "rets", "sabe", "sade", "sadi", "said", "sain", "sate",
		"sear", "seat", "seed", "seer", "seta", "stab", "star", "tabs", "tads", "tain",
		"tare", "teas", "teed", "tees", "tree", "tsar", "abs", "ads", "aid", "ain",
		"arb", "are", "ate", "bad", "bar", "bas", "bat", "bed", "bra", "dab",
		"deb", "dee", "did", "die", "dig", "din", "ear", "eat", "era", "ers",
		"eta", "ged", "gee", "gid", "gie", "gin", "ids", "rad", "ras", "rat",
		"reb", "red", "ree", "rei", "res", "ret", "sab", "sad", "sae", "sat",
		"sea", "see", "seg", "sei", "ser", "set", "tab", "tad", "tae", "tar",
		"tas", "tea", "tee", "ab", "ad", "ae", "ai", "ar", "as", "at",
		"ba", "be", "de", "ed", "er", "es", "et", "id", "in", "re",
		"ta"};
	*/


	private Callback callback = new Callback() {
		@Override
		public void run(int wordNum) {
			/*
			if(board.allOpenPositions.isEmpty()) {
				//stop recursing, just check the rest of the words
				board.recurse(wordNum, words[wordNum], 0, null, true);
			}
			*/
			if(wordNum==words.length) {
				board.finishedBoards.add(board.hashCode());
				System.out.println(board);
				System.out.println("----");
				System.exit(0);
				return;
			}
			board.recurse(wordNum, words[wordNum], 0, null, false);
		}
	};

	public static void main(String[] args) {
		Aaron aaron = new Aaron();
		aaron.callback.run(0);
	}
}

