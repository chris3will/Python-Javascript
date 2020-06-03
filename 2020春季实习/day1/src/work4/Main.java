package work4;

/**
 * 4.使用数组实现ArrayList（至少包括添加元素，删除元素，查询元素）。
 */
public class Main {
    public static void main(String[] args) {
        MyArrayList<Integer> arrayList = new MyArrayList<>();

        arrayList.add(1);
        arrayList.showArray();
        arrayList.add(2);
        arrayList.add(4);
        if(arrayList.contain(4)){
            System.out.println("contain it!");
        }else System.out.println("doesn't contain");
        arrayList.removeByName(4);
        arrayList.showArray();

        if(arrayList.contain(4)){
            System.out.println("contain it!");
        }else System.out.println("doesn't contain");

        int pos = arrayList.indexOf(2);
        if(pos!=-1){
            System.out.println("the pos of the 2 is: "+pos);
        }else{
            System.out.println("2 doesn't exsit in the arrayList");
        }


    }
}
