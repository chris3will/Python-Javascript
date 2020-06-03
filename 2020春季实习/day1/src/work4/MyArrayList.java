package work4;

import org.omg.PortableInterceptor.SYSTEM_EXCEPTION;

import java.util.ArrayList;
import java.util.Arrays;

public class MyArrayList<E> {

    private transient  Object[] arrayList = null;  //存数据，万物皆为对象，把它也看做数组即可
    private int scale = 0;  //控制数组长度规模，但这个不代表Object的长度
    private static final int DEFAULT_CAPACITY = 20;  //定义一个默认大小

    public  MyArrayList(){
        this.arrayList = new Object[DEFAULT_CAPACITY];
    }
    public MyArrayList(int newCapacity){
        if(newCapacity<0){
            throw new IllegalArgumentException("集合容量不能小于0!,而你输入的容量是: "+newCapacity);
        }else{
            this.arrayList = new Object[newCapacity];
        }
    }

    public void showArray(){
        for(int i=0;i<arrayList.length && arrayList[i]!=null;i++) System.out.print(arrayList[i]+" ");
        System.out.println();
    }
    public boolean add(Object e){
        ensureCapacityInternal(-1,null); //先确保可以增加

        arrayList[scale++] = e;
        return true;
    }

    public boolean add(int index, Object object){
        if(index == scale){
            add(object);  //直接加到末尾
        }else{
            //先检查下标是否越界
            if(checkIndexOf(index)){
                if(scale < arrayList.length){
                    System.arraycopy(arrayList,index,arrayList,index+1,scale-index);
                    arrayList[index] = object;
                }else{
                    ensureCapacityInternal(-1,null);
                }
                scale++;
            }
        }

        return true;
    }

    private void ensureCapacityInternal(int index, Object obj){
        //兼顾插入和扩容的作用
        if(this.scale >= arrayList.length){
            //先创建一个新数组
            //确保之后的元素能加上去
            int oldCapacity = arrayList.length;
            int newCapacity = oldCapacity + (oldCapacity>>1);
            Object[] newArrayList = new Object[newCapacity];

            if(index  == -1 && obj ==null){
                arrayList = Arrays.copyOf(arrayList,newCapacity);
            }else{
                //这个相当于另一个功能，
                //将插入索引位置前面的对象 拷贝一下
                System.arraycopy(arrayList,index,newArrayList,index+1,scale - index);
            }

            arrayList = newArrayList;
            newArrayList = null;
        }
    }

    public int getScale(){
        return this.scale;
    }

    public int indexOf(Object o){
        //检索元素的操作
        if(o==null){
            for(int i=0;i<arrayList.length;i++){
                if(arrayList[i]==null){
                    return i;
                }
            }
        }else{
            for(int i=0;i<arrayList.length;i++){
                if(arrayList[i].equals(o))return i;
            }
        }
        return -1;
    }

    //判断给定数组是否越界
    public boolean checkIndexOf(int index){
        if(index>scale||index<0){
            throw new IllegalArgumentException("输入的数组下标越界: " +index);
        }else{
            return true;
        }
    }

    public Object get(int index){
        checkIndexOf(index);
        return arrayList[index];
    }

    //删除指定元素
    public  boolean removeByName(Object obj){
        for(int i=0;i<scale;i++){
            if(obj.equals(arrayList[i])){
                removeByIndex(i);
                return true;
            }
        }
        return false;
    }
    //根据索引删除元素
    public Object removeByIndex(int index){
        if(checkIndexOf(index)){
            //先将对象保存下来
            Object obj = arrayList[index];
            if(index == scale){
                arrayList[index] = null;
            }else{
                System.arraycopy(arrayList,index+1,arrayList,index,scale-index);
            }
            scale--;
            return obj;
        }
        return null;
    }

    //删除所有元素
    public void clear(){
        for(int i=0;i<arrayList.length;i++)arrayList[i]=null;
    }



    //查看元素是否在集合中
    public boolean contain(Object obj){
        for(int i=0;i<arrayList.length;i++){
            if(obj.equals(arrayList[i]))return true;
        }
        return  false;
    }


}
