package work9;

import org.omg.PortableInterceptor.SYSTEM_EXCEPTION;

/**
 * 9.创建一个类 为该类定义三个构造函数 分别执行下列操作
 *  1、传递两个整数值并找出其中较大的一个值
 *  2、传递三个double值并求出其乘积
 *  3、传递两个字符串值并检查其是否相同
 * 在main方法中测试构造函数的调用
 */

public class Main {
    public static void main(String[] args) {
        Waiter waiter = new Waiter(123,4124);
        System.out.println(waiter);
        waiter = new Waiter(1,3,5);
        System.out.println(waiter);
        waiter = new Waiter("123","abc");
        System.out.println(waiter);
    }
}
