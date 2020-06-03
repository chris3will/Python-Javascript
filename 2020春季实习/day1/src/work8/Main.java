package work8;

import org.omg.PortableInterceptor.SYSTEM_EXCEPTION;

/**
 *
 8. 获取两个字符串中最大相同子串。比如：str1 = "abcwerthelloyuiodef“;str2 = "cvhellobnm"

 */
public class Main {
    public static void main(String[] args) {
        String s1= "abcwerthelloyuiodef";
        String s2 = "cvhellobnm";
        System.out.println(getMaxSubString(s2,s1));
    }


    private static String getMaxSubString(String s1,String s2){
        String max = (s1.length()>s2.length()?s1:s2);//长字符串
        String min = (max.equals(s1))?s2:s1;//短字符串

        for (int i = 0; i < min.length(); i++) {
            //遍历每一种长度较短的子串，保证不漏即可
            for(int a = 0, b = min.length()-i; b!=min.length()+1; a++,b++) {
                String sub = min.substring(a,b);

                if(max.contains(sub))
                    return sub + " 即为所求最大相同子串";
            }
        }
        return null;
    }

}
