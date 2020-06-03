package work7;

import java.util.ArrayList;
import java.util.List;

/**
 * 7.定义类Student，包含三个属性：学号number(int)，年级state(int)，成绩score(int)。 创建20个学生对象，学号为1到20，年级和成绩都由随机数确定。
 * 问题一：打印出3年级(state值为3）的学生信息。
 * 问题二：使用冒泡排序按学生成绩排序，并遍历所有学生信息
 * 提示：
 * 1) 生成随机数：Math.random()，返回值类型double;
 * 2) 四舍五入取整：Math.round(double d)，返回值类型long。
 */
public class Main {
    public static void main(String[] args) {
        //先创建20个学生对象
//        List<Student> students = new ArrayList<Student>();
        Student[] students = new Student[20];

        for(int i=0;i<20;i++){
            int state = (int)Math.round(Math.random()*12)+1;
            int score = (int)Math.round(Math.random()*100)+1;
            students[i] = (new Student(i,state,score));
            //System.out.println(students.get(students.size()-1));
        }

        Student temp = new Student(); //临时变量
        int isChange;  //记录该次循环是否发生了置换
        for(int i=0;i<students.length-1;i++){
            isChange = 0;  //没比较一次就初始化为0

            //内层循环是当前需要比较的趟数
            for(int j=0;j<students.length- i -1;j++){
                //前一位与后一位比较，如果前一位比后一位要大，则发生必要的交换
                if(students[j].getScore()>students[j+1].getScore()){
                    temp = students[j];
                    students[j] = students[j+1];
                    students[j+1] = temp;

                    isChange = 1;
                }
            }
            //如果比较完一趟发现没有发生置换，则说明冒泡排序已经结束，不需要继续迭代了
            //冒泡排序每一次迭代至少调整一个数的位置
            if(isChange==0){
                break;
            }
        }
        for(int i=0;i<students.length;i++)
            System.out.println(students[i]);



    }
}
