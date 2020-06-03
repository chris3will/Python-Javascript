package work3;

import java.util.Random;

/**
 * 3.产生10个1~20之间的随机数，要求随机数不能重复 get
 */
public class Main {
    public static void main(String[] args) {

        int[] nums = new int[20];
        for(int i=0;i<nums.length;i++) nums[i] = i + 1;

        int[] radms = new int[10];
        Random random = new Random();
        for(int i=0;i<radms.length;i++){
            int index = random.nextInt(nums.length - i);  //不会读到这个位置，在0状态时即保证下标不会越界
            radms[i] = nums[index];
            nums[index] = nums[nums.length-i -1];  //用原始数字数组中还没有被利用的位置替代已经被使用过的数字的位置，可以理解为从后往前补齐
        }

        for(int i=0;i<radms.length;i++) System.out.println(radms[i]);

    }
}
