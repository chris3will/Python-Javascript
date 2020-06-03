package work2;

import com.sun.org.apache.bcel.internal.generic.ANEWARRAY;
import org.omg.PortableInterceptor.SYSTEM_EXCEPTION;

import java.util.*;

/**
 * 2.编写程序，从键盘输入字符串，输出其中重复的字符、不重复的字符以及消除重复以后的字符列表。
 * 个人理解，只用读取一行输入，即只输入一次字符串，得到一个字符列表即可
 *
 * refer:
 * https://blog.csdn.net/lytwy123/article/details/80766858
 *
 */
public class Main {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("请您输入您的内容（输入空白以终止）");
        String str = scanner.nextLine();
        //System.out.println(str);
//        while(true){
//            if(!"".equals(str)){
//                System.out.println(str);
//                str = scanner.nextLine();
//            }else{
//                break;
//            }
//        }
//
        System.out.println("输出结束");
        //开始操作
        //https://stackoverflow.com/questions/10483139/cannot-use-arraylist-of-type-char-as-methods-argument
        //char 不能在这个类型说明里面直接用，要用wrapper type

        ArrayList<Character> outputList = new ArrayList<>();
        HashMap<Character,Integer> charMap = new HashMap<>();
        //思路，遍历String，然后放进一个字典中，再把出现次数大于1的放入字符列表中
        for(int i=0;i<str.length();i++){
            char ch = str.charAt(i);
            if(!outputList.contains(ch)){
                outputList.add(ch);
            }
            //先判断是否在字典中
            if(charMap.containsKey(ch)){
                Integer count = charMap.get(ch);
                charMap.put(ch,count+1);
            }else{
                charMap.put(ch,1);
            }
        }

        ArrayList<Character> oneList = new ArrayList<>();
        ArrayList<Character> moreList = new ArrayList<>();
        Set<Map.Entry<Character,Integer>> entrySet = charMap.entrySet();

        for(Map.Entry<Character,Integer> entry:entrySet){
            if(entry.getValue()>1){
                //这是重复的字符
                moreList.add(entry.getKey());
            }else{
                //这是只出现一次的字符
                oneList.add(entry.getKey());
            }
        }

        //先输出重复的
        System.out.println("输出重复的字符");
        Iterator iterator = moreList.iterator();
        while(iterator.hasNext()){
            System.out.print(iterator.next()+" ");
        }
        System.out.println();
        //输出不重复的
        System.out.println("输出不重复的字符");
        iterator = oneList.iterator();
        while(iterator.hasNext()){
            System.out.print(iterator.next()+" ");
        }
        System.out.println();
        //直接输出列表
        System.out.println("输出消除重复以后的字符串");
        System.out.println(outputList);


        scanner.close();

    }
}
