package work1;

/**
 * 1.定义图书类Book，具有属性账号id，书名name、作者author 和价格price，在创建图书对象时要求通过构造器进行创建，一次性将四个属性全部赋值，
 *
 * 要求账户属性是int型，名称是String型，作者是String型，价格是double,请合理进行封装。
 *
 * 1) 在Book类，添加toString方法，要求返回 图书信息字符串，使用\t隔开各信息 get
 *
 * 2) 要求定义一个图书馆Library类，在图书馆类中添加一个HashSet集合用于保存多本图书 get
 *
 * 3）在图书馆类中要求能够新增图书 get
 *
 * 4）在图书馆类中要求可以查看所有添加过的图书 get
 *
 * 5）不允许添加重复的图书（如果账号id和书名name相同，则认为两本书是相同的）  -> 在这一步，试图先将set化为Map，且以前两个元素作为key
 * https://blog.csdn.net/FX_SKY/article/details/10552827
 *
 * 6）可以根据id删除图书 get
 */
public class Main {
    public static void main(String[] args) {
        Library library = new Library();
        Book book1 = new Book();
        book1.setId(1);
        book1.setName("at");
        book1.setAuthor("ss");

        library.addNew(book1);
        library.showBooks();

        //library.deleteById(1);

        System.out.println("***");

        Book book2 = new Book();
        book2.setId(1);
        book2.setName("at");
        library.addNew(book2);
        library.showBooks();

    }
}
