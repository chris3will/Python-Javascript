package Work10;

public class MyDoubleLinkList<E> {
    public class Node{
        E data;
        Node next;
        Node prev;

        public Node(){
        }

        public Node(E data){
            this.data = data;
            this.next = null;
            this.prev = null;
        }

        public Node(E data, Node prev, Node next){
            this.data = data;
            this.prev = prev;
            this.next = next;
        }

    }

    public Node head;
    public Node tail;
    public int size ; //记录链表规模

    public MyDoubleLinkList(){
        head = new Node();
        tail = new Node();
        size = 0;
    }

    //初步实现功能，增删改查，打印，删除头部，删除尾部
    //要注意的就是头尾指针的处理

    //在尾部添加结点
    public void addTail(E elem){
        Node newNode = new Node(elem);
        if(size ==0){
            //目前还没有元素，头尾指针都指向空
            head.next = newNode;
            newNode.prev =head;
            newNode.next = tail;
            tail.prev = newNode;

        }else{
            //利用尾节点把它加到尾部
            Node last = tail.prev;
            //把新节点放到last后面
            last.next = newNode;
            newNode.prev  = last;
            newNode.next = tail;
            tail.prev = newNode;
        }
        size++;
    }

    //在头部插入结点
    public void addHead(E elem){
        Node newNode = new Node(elem);
        if(size ==0){
            head.next = newNode;
            newNode.prev =head;
            newNode.next = tail;
            tail.prev = newNode;
        }else{
            Node next = head.next;
            next.prev = newNode;
            newNode.next = next;
            newNode.prev = head;
            head.next = newNode;
        }
        size++;
    }

    //删除头部
    public void popHead(){
        if(size==0){
            System.out.println("链表为空，没有可以删除的元素");
        }else{
            //更新头结点和第二个节点的指针
            head.next.next.prev = head;
            head.next = head.next.next;
            size--;
        }
    }

    //删除尾部
    public void popTail(){
        if(size==0){
            System.out.println("链表为空，没有可以删除的元素");
        }else{
            tail.prev.prev.next = tail;
            tail.prev = tail.prev.prev;
            size --;
        }
    }

    //向某一个位置插入元素
    public void insertByIndex(int index, E elem){
        //先判断插入的下标是否越界，否则报错
        if(index < 0 || index > size){
            System.out.println("元素插入位置下标越界，无法插入");
        }else{
            //这里理应都是可以插入的位置
            if(index==0){
                //插入头部
                addHead(elem);
            }else if(index == size){
                addTail(elem);
            }else{
                //为了简便，直接从头找
                Node p = head;
                int loc=0;
                while(p.next!=null){
                    if(loc==index){
                        break;
                    }
                    loc++;
                    p=p.next;
                }
                //得到了对应的loc位置
                //此时p.next为该位置原来的节点
                Node temp = p.next;  //把这个数保存下来
                Node newNode =new Node(elem);

                newNode.next = temp;
                newNode.prev = temp.prev;
                temp.prev.next = newNode;
                temp.prev = newNode;
                size++;
            }
        }
    }

    //删除某一个位置的元素
    public void deleteByIndex(int index){
        if(index<0||index>size-1){
            System.out.println("数组下标越界，无法尝试删除操作");
        }else{
            if(index==0){
                popHead();
            }else if(index==size-1){
                popTail();
            }else{
                int loc=0;
                Node p = head;
                while(p.next!=null){
                    if(loc==index){
                        break;
                    }
                    loc++;
                    p=p.next;
                }
                //要删除的位置找到了，即p.next
                Node del = p.next;
                del.next.prev =del.prev;
                del.prev.next = del.next;

                size--;
            }
        }
    }

    //获取某一个位置的元素
    public Node getNodeByIndex(int index){
        if(index<0||index>size-1){
            System.out.println("下标越界，无法获取该位置的元素");
            return null;
        }else{
            if(size==0){
                System.out.println("链表为空，查询失败");
                return null;
            }else{
                int loc = 0;
                Node p = head.next;
                while(p.next!=null){
                    if(index==loc){
                        break;
                    }
                    loc++;
                    p=p.next;
                }
                return p.next;
            }
        }
    }

    //查询某一个元素在列表中从头结点开始第一次出现的下标位置
    public int getLocFromHead(E elem){
        if(size==0){
            System.out.println("链表为空，查询失败");
            return -1;
        }else{
            int loc=0;
            Node p = head;
            int gotIt = -1;
            while(p.next!=null&&loc<size){
                if(p.next.data.equals(elem)){
                    gotIt = 1;
                    break;
                }
                loc++;
                p=p.next;
            }
            if(gotIt==1)
            return loc;
            else return -1;
        }
    }

    //判断链表是否为空
    public boolean empty(){
        return size==0;
    }

    //清空链表
    public void clear(){
        size=0;
        head.next=null;
        tail.prev=null;
    }

    public String toString(){
        if(empty()){
            return "{}";
        }else{
            String result="{";
            int loc=0;
            Node p = head;
            while(p.next!=null&&loc<size){
                result = result + " " +p.next.data;
                p=p.next;
                loc++;
            }
            return result+" }";
        }
    }

    public void display(){
        Node p = head.next;
        int loc=0;
        while(p!=null&&loc<size){
            loc++;
            System.out.print(p.data+" ");
            p=p.next;
        }
        System.out.println("");
    }
}
