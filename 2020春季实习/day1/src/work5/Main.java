package work5;

import java.util.*;

/**
 * 5.编写程序，从键盘输入字符串，输出每个字符出现的次数，字符根据自然排序进行排序，输出格式为 a:1 e:2 g:1 ....
 *
 * 注意，要排序的是这个字符，而不是出现的次数
 */
public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        String str = scanner.nextLine();
        scanner.close();

        HashMap<Character,Integer> charMap = new HashMap<>();  //注意，这个是会破坏输入的顺序的。
        for(int i=0;i<str.length();i++){
            char ch = str.charAt(i);
            if(charMap.containsKey(ch)){
                int oldNum = charMap.get(ch);
                charMap.put(ch,oldNum+1);
            }else{
                charMap.put(ch,1);
            }
        }

        TreeSet<Character> set = new TreeSet<Character>(charMap.keySet());
//        System.out.println(set);
        Iterator iterator = set.iterator();
        while(iterator.hasNext()){
            char ch = (char) iterator.next();
            System.out.print(ch+":"+charMap.get(ch)+" ");
        }


    }
}
