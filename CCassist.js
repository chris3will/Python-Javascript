var firstlog=document.getElementById('ctl00_btnlogin');

firstlog.addEventListener("click",function(){
    //如果进入到这里则说明已经相应了第一步
    alert("I'm here.");
    try{
        var secondlog=document.getElementById('btnLogin');
        inputmsg();
        secondlog.addEventListener('click',function(){
            secondlog.click();
        });
    }
    catch(err)
    {
        console.log(err);
    }
});
function inputmsg(){
    var us=prompt('请输入你的账号','2017141051019');
    var ps=prompt('请输入你的密码','656053wcz');
    var username=document.getElementById('LoginName');
    var Password=document.getElementById('Password');
    username.value=us;
    Password.value=ps;
}
function findmsg(){
    var theflag;
    b=$('a.left')
    console.log(b)
    for (var i in b){
        var c=b[i].href
        if(c.match(/MySpace/i)){
            console.log(b[i].href);
            console.log(i);//找到了需要点击的元素
            theflag=i;
            break;
        }
    }//已经找到了需要加载的文字所在标签
    myname=b[theflag];
    myname.addEventListener('click',function(){
        window.location.href=myname.href;
    });

    logout=b[theflag+1];
    logout.addEventListener('click',function(){
        window.location.href=logout.href;
    });

}


findmsg()
