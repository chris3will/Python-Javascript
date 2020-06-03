package work9;

public class Waiter {
    private int value;

    public Waiter(int v1,int v2){
        value = (v1>v2)?v1:v2;
    }

    public Waiter(int v1,int v2,int v3){
        value = v1*v2*v3;
    }

    public Waiter(String s1, String s2){
        value = (s1.equals(s2))?1:0;
    }

    public String toString(){
        return ""+value;
    }

}
