package work1;

public class Book {
    private Integer id;
    private String name;
    private String author;
    private double price;

    public String toString(){
        return id + "\t" + name + "\t" + author + "\t" + price;
    }
//
//    public  Book(){
//        this.id=-1;
//        this.name="name";
//        this.author = "author";
//        this.price = -1;
//    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }

    public double getPrice() {
        return price;
    }

    public void setPrice(double price) {
        this.price = price;
    }
}
