package work7;

public class Student {
    private int number;
    private int state;
    private int score;

    public String toString(){
        return "number: "+this.number  +
                " state: "+this.state+
                " score: "+this.score;
    }
    public int getNumber() {
        return number;
    }

    public void setNumber(int number) {
        this.number = number;
    }

    public int getState() {
        return state;
    }

    public void setState(int state) {
        this.state = state;
    }

    public int getScore() {
        return score;
    }

    public void setScore(int score) {
        this.score = score;
    }

    public Student(){
        number = -1;
        state = -1;
        score = -1;
    }
    public Student(int number,int state,int score){
        this.number = number;
        this.state = state;
        this.score = score;
    }
}
