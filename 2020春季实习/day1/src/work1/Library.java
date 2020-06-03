package work1;

import java.util.HashSet;
import java.util.Iterator;

public class Library {
    private HashSet<Book> shelf;  //定义一个hashset集合来保存书


    public Library(){//总之你要初始化这个HashSet，要不然就会报错
        shelf = new HashSet<Book>();
    }
    public Library(HashSet<Book> shelf) {
        this.shelf = shelf;
    }

    public void deleteById(Integer id){
        //方法还是迭代扫描的方法尝试，
        Iterator iterator = this.shelf.iterator();
        while(iterator.hasNext()){
            Book tempBook = (Book) iterator.next();
            if(tempBook.getId()==id){
                this.shelf.remove(tempBook);
                break;  //可以在这里删除成功则同时，否则不通知。后期加上
            }
        }
    }


    public void addNew(Book newBook){


        if(newBook!=null){
            Iterator iterator = shelf.iterator();
            boolean canInsert = true;
            while(iterator.hasNext()){
                Book tempBook = (Book) iterator.next();
                if(tempBook.getId().equals(newBook.getId()) && tempBook.getName().equals(newBook.getName())){  //提示有歧义，所以我先用与来表示
                    canInsert = false;
                    break;
                }
            }
            if(canInsert)
                this.shelf.add(newBook);
            else{
                System.out.println("the book exists in the shelf! Don't add it any more!");
            }
        }
    }

    public void showBooks(){
        /**
         * 打印图书馆中的书籍，需要用到遍历
         * 先不考虑排序
         */
        //利用迭代器进行迭代
        Iterator iterator = this.shelf.iterator();
        while(iterator.hasNext()){
            System.out.println(iterator.next());
        }
    }

}
