package Work10;

import java.util.Scanner;

//Chongzhi Wang - 2020/6/3
public class Main {
    //版本1
    public static final int N = 100000 +10; //先定义一个长度
    public static int[] e =new int[N];   //值
    public static int[] l = new int[N];  //左指针
    public static int[] r = new int[N];  //右指针
    public static int idx;
    public int m;

    public void init(){
        l[1] = 0;  //左端点指向右端点
        r[0] =1;  //右端点指向左端点
        idx = 2;  //当前已经默认有两个节点
    }

    public static void add(int k, int x){  //把x值插在k位置
        e[idx] = x;
        r[idx] =r[k];
        l[idx] = k;
        l[r[k]] = idx;
        r[k] = idx++;  //给新加入的点分配一个新的节点编号
    }

    void remove(int k){
        //删除第k个插入的节点
        l[l[k]] = l[k];
        r[l[k]] = r[k];
    }

    public static void main(String[] args) {
        MyDoubleLinkList<String> list = new MyDoubleLinkList<String>();

        list.addTail("1");
        list.addTail("2");
        list.addTail("3");
        list.addTail("4");
        list.deleteByIndex(2);
        list.display();
        System.out.println(list);


        list.popTail();
        list.display();

        System.out.println(list.getLocFromHead("3"));

    }
}
