package work6;

import java.util.ArrayList;
import java.util.List;

/**
 *
 6.两个乒乓球队进行比赛，各出三人。甲队为a,b,c三人，乙队为x,y,z三人。已抽签决定比赛名单。有人向队员打听比赛的名单。a说他不和x比，c说他不和x,z比，请编程序找出三队赛手的名单
 */
public class Main {
    public static void main(String[] args) {
        //一共两支队伍，总共6个人
        //输出三组对阵名单
        List<String> a = new ArrayList<String>();
        List<String> b = new ArrayList<String>();
        List<String> c = new ArrayList<String>();

        a.add("y");
        a.add("z");
        b.add("x");
        b.add("y");
        b.add("z");
        c.add("y");

        a.removeAll(c);  //a不可能和一定确定下来的c有共同对手
        b.removeAll(c);  //b不可能和已经确定下来的c有共同对手
        b.removeAll(a);  //b同样不可能和已经确定下来的a有共同对手

        System.out.println("a的对手为:"+a.get(0));
        System.out.println("b的对手为:"+b.get(0));
        System.out.println("c的对手为:"+c.get(0));
    }
}
